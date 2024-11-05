from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    
    TEMPLATES_AUTO_RELOAD = True
    
    MQTT_BROKER_URL = os.getenv('MQTT_BROKER_URL') 
    MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT'))
    MQTT_USERNAME = os.getenv('MQTT_USERNAME')
    MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
    MQTT_KEEPALIVE = int(os.getenv('MQTT_KEEPALIVE'))
    MQTT_TLS_ENABLED = os.getenv('MQTT_TLS_ENABLED') == 'True'
