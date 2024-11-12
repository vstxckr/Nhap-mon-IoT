
from simple import MQTTClient
import random
import network
import time
import dht
from machine import Pin, ADC
# ssid = "BlueCyber"
# password = "Tu@n201088"
# ssid = 'HieuManh'
# password = '19992912'
ssid = "Yesyes"
password = "09090909"
# ssid = "Haind"
# password = "zzzzzzzz"
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

# MQTT_SERVER = "192.168.0.52"
MQTT_SERVER = "172.20.10.8"
#MQTT_SERVER = "172.20.10.10"
MQTT_PORT = 8668
CLIENT_ID = 'ManhDX_esp8266'
TOPIC_PUB = 'home/sensors'
TOPIC_Light = 'home/light'
TOPIC_Fan = 'home/fan'
TOPIC_Air = 'home/aircondition'
TOPIC_ALL = 'home/all'

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

# Define built-in LED (GPIO 2)
#led = Pin(2, Pin.OUT)

#led.value(1)

Fan = Pin(2, Pin.OUT)
Light_bulb = Pin(5, Pin.OUT)
Air_Condition = Pin(4, Pin.OUT)

Fan.value(0)
Light_bulb.value(0)
Air_Condition.value(0)


def connect_mqtt():
    try:
        client.connect()
        print('Connected to %s MQTT broker' % MQTT_SERVER)
    except Exception as e:
        print('Could not connect to MQTT broker:', e)

# Callback for receiving MQTT messages
def on_message(topic, msg):
    print('Received message:', topic, msg)
    if topic == b'home/light':
        if msg == b'ON':
            Light_bulb.value(1)  
            print('Light is ON')
        elif msg == b'OFF':
            Light_bulb.value(0) 
            print('Light is OFF')
        client.publish('check/light', str("yes"))
    elif topic == b'home/fan':
        if msg == b'ON':
            Fan.value(1)  
            print('Fan is ON')
        elif msg == b'OFF':
            Fan.value(0)  
            print('Fan is OFF')
        client.publish('check/fan', str("yes"))
    elif topic == b'home/aircondition':
        if msg == b'ON':
            Air_Condition.value(1)  
            print('Air Condition is ON')
        elif msg == b'OFF':
            Air_Condition.value(0)  
            print('Air Condition is OFF')
        client.publish('check/air', str("yes"))
    elif topic == b'home/all':
        if msg == b'ON':
            Fan.value(1)
            Light_bulb.value(1)
            Air_Condition.value(1)
        elif msg == b'OFF':
            Fan.value(0)
            Light_bulb.value(0)
            Air_Condition.value(0)
        client.publish('check/all', str("yes"))

def random1(a, b):
    return a + random.getrandbits(7) % (b - a + 1)

# Publish sensor data
def publish_data(temperature, humidity, light_level, wind_speed):
    try:
        if (Fan.value() == 1 and Light_bulb.value() == 1 and Air_Condition.value() == 1):
            all_dev = 1
        else:
            all_dev = 0
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

# Setup DHT22 sensor
Pin(0).value(0)
dht_sensor = dht.DHT22(Pin(0))  # Assuming GPIO 16 for DHT22 data pin

# Setup CDS-NVZ1 (LDR) sensor
light_sensor = ADC(0)  # A0 pin for analog input

# Connect to MQTT broker and subscribe to 'home/light'
connect_mqtt()
client.set_callback(on_message)
client.subscribe(TOPIC_Light)
client.subscribe(TOPIC_Air)
client.subscribe(TOPIC_Fan)
client.subscribe(TOPIC_ALL)

# Main loop
#client.loop_start()
while True:
    try:

        # Read data from DHT22
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
# 
        # Read data from CDS-NVZ1 (LDR)
        light_level = light_sensor.read()  # Analog output (0-1023)

        # Publish the sensor data
        # temperature =  random1(20, 25)
        # humidity =  random1(70,75)
        # light_level =  random1(100, 150)
        wind_speed = random1(50, 150)
        publish_data(temperature, humidity, light_level, wind_speed)
        # Wait for MQTT messages to control the light
        client.check_msg()

        time.sleep(2)  # Adjust the interval as needed
    except Exception as e:
        print('Error:', e)
        client.disconnect()
        connect_mqtt()
        time.sleep(5)
