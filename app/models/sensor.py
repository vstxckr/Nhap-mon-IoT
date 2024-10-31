# app/models/sensor.py
import json
from datetime import datetime

class SensorData:
    data = {"temperature": None, "humidity": None, "light_level": None}

    @staticmethod
    def update(data):
        SensorData.data.update(data)
        return SensorData.data

    # @staticmethod
    # def load_logs(log_file):
    #     try:
    #         with open(log_file, "r") as f:
    #             return json.load(f)
    #     except (FileNotFoundError, json.JSONDecodeError):
    #         return []

    # @staticmethod
    # def save_log(data, log_file="sensor_log.json"):
    #     with open(log_file, "a") as f:
    #         json.dump(data, f, indent=4)
    #         f.write(',')

# class MQTTClient:
#     def __init__(self, app):
#         self.client = Mqtt(app)
#         self.socketio = ""

#     def getClient(self):
#         return self.client
    
#     def assignSocket(self, socket):
#         self.socketio = socket
