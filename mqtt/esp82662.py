from simple import MQTTClient
import random
import network
import time
import dht
from machine import Pin, ADC

# Wi-Fi configuration
# ssid = 'HieuManh'
# password = '19992912'
ssid = 'Yesyes'
password = '09090909'

# Connect to Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait for Wi-Fi connection
while not station.isconnected():
    print('Connecting to Wi-Fi...')
    time.sleep(1)

print('Connected to WiFi')
print('Network config:', station.ifconfig())

# MQTT configuration
# MQTT_SERVER = "192.168.1.4"
MQTT_SERVER = "172.20.10.8"
MQTT_PORT = 8668
CLIENT_ID = 'ManhDX_esp8266'
TOPIC_PUB = 'home/sensors'
TOPIC_Light = 'home/light'
TOPIC_Fan = 'home/fan'
TOPIC_Air = 'home/aircondition'
TOPIC_ALL = 'home/all'
TOPIC_ALERT = 'home/alert'

# MQTT credentials
MQTT_USERNAME = 'ManhDX'
MQTT_PASSWORD = 'B21DCAT124'

# Initialize MQTT client with authentication
client = MQTTClient(
    CLIENT_ID,  
    MQTT_SERVER, 
    port=MQTT_PORT, 
    user=MQTT_USERNAME, 
    password=MQTT_PASSWORD, 
    keepalive=60
)

# Initialize devices and LED
Fan = Pin(2, Pin.OUT)
Light_bulb = Pin(5, Pin.OUT)
Air_Condition = Pin(4, Pin.OUT)
alert_led = Pin(14, Pin.OUT)  # Using D5 (GPIO14) for alert LED

Fan.value(0)
Light_bulb.value(0)
Air_Condition.value(0)
alert_led.value(0)  # Ensure alert LED is off initially

# Variables for LED blink control
blink_active = False
blink_count = 0
last_blink_time = 0

# Connect to MQTT
def connect_mqtt():
    try:
        client.connect()
        print('Connected to %s MQTT broker' % MQTT_SERVER)
    except Exception as e:
        print('Could not connect to MQTT broker:', e)

# Callback for receiving MQTT messages
def on_message(topic, msg):
    global blink_active, blink_count, last_blink_time
    print('Received message:', topic, msg)
    if topic == b'home/light':
        if msg == b'ON':
            Light_bulb.value(1)
            print('Light is ON')
        elif msg == b'OFF':
            Light_bulb.value(0)
            print('Light is OFF')
        client.publish('check/light', "yes")
    elif topic == b'home/fan':
        if msg == b'ON':
            Fan.value(1)
            print('Fan is ON')
        elif msg == b'OFF':
            Fan.value(0)
            print('Fan is OFF')
        client.publish('check/fan', "yes")
    elif topic == b'home/aircondition':
        if msg == b'ON':
            Air_Condition.value(1)
            print('Air Condition is ON')
        elif msg == b'OFF':
            Air_Condition.value(0)
            print('Air Condition is OFF')
        client.publish('check/air', "yes")
    elif topic == b'home/all':
        if msg == b'ON':
            Fan.value(1)
            Light_bulb.value(1)
            Air_Condition.value(1)
        elif msg == b'OFF':
            Fan.value(0)
            Light_bulb.value(0)
            Air_Condition.value(0)
        client.publish('check/all', "yes")
    elif topic == b'home/alert':
        if msg == b'YES':
            # Activate LED blinking
            blink_active = True
            blink_count = 0
            last_blink_time = time.ticks_ms()

def random1(a, b):
    return a + random.getrandbits(7) % (b - a + 1)

# Publish sensor data
def publish_data(temperature, humidity, light_level, wind_speed):
    try:
        all_dev = 1 if (Fan.value() == 1 and Light_bulb.value() == 1 and Air_Condition.value() == 1) else 0
        message = {
            "temperature": temperature,
            "humidity": humidity,
            "light_level": light_level,
            "wind_speed": wind_speed,
            "fan": Fan.value(),
            "light": Light_bulb.value(),
            "air": Air_Condition.value(),
            "all": all_dev
        }
        client.publish(TOPIC_PUB, str(message))
        print('Data published:', message)
    except Exception as e:
        print('Failed to publish message:', e)

# Setup DHT22 and light sensor
Pin(0).value(0)
dht_sensor = dht.DHT22(Pin(0))  # Assuming GPIO 16 for DHT22 data pin
light_sensor = ADC(0)  # A0 pin for analog input

# Connect to MQTT broker and subscribe to topics
connect_mqtt()
client.set_callback(on_message)
client.subscribe(TOPIC_Light)
client.subscribe(TOPIC_Air)
client.subscribe(TOPIC_Fan)
client.subscribe(TOPIC_ALL)
client.subscribe(TOPIC_ALERT)

# Main loop
while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        light_level = light_sensor.read()
        wind_speed = random1(50, 150)
        publish_data(temperature, humidity, light_level, wind_speed)
        client.check_msg()
        
        # Handle LED blinking if activated
        if blink_active:
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, last_blink_time) > 500:  # 500ms interval
                alert_led.value(not alert_led.value())  # Toggle LED
                last_blink_time = current_time
                blink_count += 1
                if blink_count >= 6:  # 3 full blinks
                    blink_active = False
                    alert_led.value(0)  # Turn off LED after blinking

        time.sleep(2)
    except Exception as e:
        print('Error:', e)
        client.disconnect()
        connect_mqtt()
        time.sleep(5)
