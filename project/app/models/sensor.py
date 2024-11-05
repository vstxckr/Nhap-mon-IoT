# app/models/sensor.py

import json
import os

class SensorData:
    # FILE_PATH = "sensor_data.json"
    data = {"temperature": None, "humidity": None, "light_level": None}

    @staticmethod
    def update(data):
        """Update data and save to file."""
        SensorData.data.update(data)
        return SensorData.data

    @staticmethod
    def get_data_realtime():
        """Retrieve the current data."""
        return SensorData.data