import json
from pathlib import Path
from flask import jsonify
from app.models.database import Database
from sqlalchemy import create_engine, text

db = Database

def handle_get_sensor_data():
    # Lấy 100 bản ghi mới nhất từ bảng `sensor_data`

    with open('C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log.json', 'r') as f:
        return f.read()