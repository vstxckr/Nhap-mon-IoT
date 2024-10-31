# app/controllers/main_controller.py
from flask import Blueprint, render_template, request, jsonify
from app.models.sensor import SensorData#, MQTTHandler
from flask_socketio import SocketIO, emit
from app.controllers.mqtt_handler import init_mqtt_socketio, sensor_data  # Import từ mqtt_handler.py
from .get_sensor_data import handle_get_sensor_data
from .get_device_status import handle_get_device_status
from .control_device import handle_control_device 
from .query_sensor_data import handle_query_sensor_data 

# Khởi tạo SocketIO
main_controller = Blueprint('main_controller', __name__)

@main_controller.route('/api/v1/sensor/pulldata', methods=['GET'])
def get_sensor_data():
    """API để lấy dữ liệu cảm biến gần nhất."""
    isrt = request.args.get('realtime')
    # print(isrt)
    if (isrt == None):
        isrt = "0"
    return handle_get_sensor_data(isrt) 

@main_controller.route('/api/v1/device/status', methods=['POST'])
def get_device_status():
    """API lấy dữ liệu."""
    return handle_get_device_status() 

@main_controller.route('/api/v1/device/control', methods=['POST'])
def control_device():
    """API để điều khiển thiết bị."""
    command = request.get_json().get('cmd', None)
    print(command)
    return handle_control_device(command) 

@main_controller.route('/api/v1/sensor/querydata', methods=['POST'])
def query_sensor_data():
    """API để lấy dữ liệu sensor."""
    return handle_query_sensor_data() 

@main_controller.route('/')
def one():
    return render_template('base.html')

@main_controller.route('/home')
def home():
    return render_template('home.html')

@main_controller.route('/data_sensor')
def data_sensor():
    # page = request.args.get('page', 1, type=int)
    # logs = SensorData.load_logs("sensor_log.json")
    # per_page = 15
    # total = len(logs)
    # start = (page - 1) * per_page
    # end = start + per_page
    # logs_paginated = logs[start:end]

    return render_template('data_sensor.html')#, logs=logs_paginated, page=page, total=total, per_page=per_page)

@main_controller.route('/action_history')
def action_history():
    # page = request.args.get('page', 1, type=int)
    # logs = SensorData.load_logs("action_log.json")
    # per_page = 15
    # total = len(logs)
    # start = (page - 1) * per_page
    # end = start + per_page
    # logs_paginated = logs[start:end]

    return render_template('action_history.html')#, logs=logs_paginated, page=page, total=total, per_page=per_page)

@main_controller.route('/profile')
def profile():
    return render_template('profile.html')

# @main_controller.route('/data/sensor_log.json')
# def serve_data():