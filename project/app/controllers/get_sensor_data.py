import json
from pathlib import Path
from flask import jsonify
from app.models.database import Database
from sqlalchemy import create_engine, text

db = Database

def handle_get_sensor_data(isrt, isrv):
    # Lấy 100 bản ghi mới nhất từ bảng `sensor_data`
    if (isrt == "0"):
        with open('C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log.json', 'r') as f:
            if (isrv == "0"):
                return f.read()
            elif (isrv == "1"):
                temp = json.load(f)
                temp.reverse()
                return temp 
    elif (isrt == "1"):
        with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log_realtime.json", "r") as f:
            if (isrv == "0"):
                return f.read()
            elif (isrv == "1"):
                temp = json.load(f)
                temp.reverse()
                return temp 