import subprocess
import time
import json
import threading
import random

# Define the MQTT broker settings
BROKER_HOST = "localhost"
BROKER_PORT = "8668"
MQTT_USER = "ManhDX"
MQTT_PASSWORD = "B21DCAT124"

# Initialize fields
fields = {
    "temperature": random.randint(20, 30),
    "humidity": random.randint(70, 90),
    "light_level": random.randint(50, 150),
    "wind_speed": random.randint(50, 150),
    "timestamp": "",
    "light": 0,
    "fan": 0,
    "air": 0,
    "all": 0
}

# Define a function to publish the updated data
def publish_data():
    data = json.dumps(fields)
    subprocess.run([
        "mosquitto_pub",
        "-h", BROKER_HOST,
        "-t", "home/sensors",
        "-m", data,
        "-u", MQTT_USER,
        "-P", MQTT_PASSWORD,
        "-p", BROKER_PORT
    ])
    print("Published data:", data)

# Define a function to handle messages
def on_message(topic, message):
    if topic == "home/light":
        fields["light"] = 1 if message == "ON" else 0
        subprocess.run([
            "mosquitto_pub",
            "-h", BROKER_HOST,
            "-t", "check/light",
            "-m", "yes",
            "-u", MQTT_USER,
            "-P", MQTT_PASSWORD,
            "-p", BROKER_PORT
        ])
    elif topic == "home/fan":
        fields["fan"] = 1 if message == "ON" else 0
        subprocess.run([
            "mosquitto_pub",
            "-h", BROKER_HOST,
            "-t", "check/fan",
            "-m", "yes",
            "-u", MQTT_USER,
            "-P", MQTT_PASSWORD,
            "-p", BROKER_PORT
        ])
    elif topic == "home/aircondition":
        fields["air"] = 1 if message == "ON" else 0
        subprocess.run([
            "mosquitto_pub",
            "-h", BROKER_HOST,
            "-t", "check/air",
            "-m", "yes",
            "-u", MQTT_USER,
            "-P", MQTT_PASSWORD,
            "-p", BROKER_PORT
        ])
    elif topic == "home/all":
        value = 1 if message == "ON" else 0
        fields["light"] = fields["fan"] = fields["air"] = fields["all"] = value
        subprocess.run([
            "mosquitto_pub",
            "-h", BROKER_HOST,
            "-t", "check/all",
            "-m", "yes",
            "-u", MQTT_USER,
            "-P", MQTT_PASSWORD,
            "-p", BROKER_PORT
        ])

# Define a function to subscribe to a specific topic
def subscribe_to_topic(topic):
    process = subprocess.Popen([
        "mosquitto_sub",
        "-h", BROKER_HOST,
        "-t", topic,
        "-u", MQTT_USER,
        "-P", MQTT_PASSWORD,
        "-p", BROKER_PORT
    ], stdout=subprocess.PIPE, text=True)

    # Process incoming messages
    for message in process.stdout:
        message = message.strip()
        print(f"Received message on {topic}: {message}")
        on_message(topic, message)

# Function to publish sensor data every 2 seconds
def periodic_publisher():
    while True:
        # Update the time field
        fields["timestamp"] = time.strftime("%H:%M:%S %m-%d-%Y", time.localtime())
        # Update random values for temperature, humidity, and light_level
        fields["temperature"] = random.randint(20, 30)
        fields["humidity"] = random.randint(70, 90)
        fields["light_level"] = random.randint(50, 150)
        fields["wind_speed"] = random.randint(50, 150)
        
        # Publish updated data
        publish_data()
        time.sleep(2)

# Start threads to subscribe to each topic
topics = ["home/light", "home/fan", "home/aircondition", "home/all"]
threads = []

for topic in topics:
    thread = threading.Thread(target=subscribe_to_topic, args=(topic,))
    thread.start()
    threads.append(thread)

# Start the periodic publisher in a separate thread
publisher_thread = threading.Thread(target=periodic_publisher)
publisher_thread.start()

# Keep the main thread alive to allow subscriptions and publishing to continue
try:
    for thread in threads:
        thread.join()
    publisher_thread.join()
except KeyboardInterrupt:
    print("Stopping subscriptions and publisher.")
