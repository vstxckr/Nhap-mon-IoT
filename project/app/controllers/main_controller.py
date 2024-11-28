# app/controllers/main_controller.py
from flask import Blueprint, render_template, request, jsonify
from app.models.sensor import SensorData#, MQTTHandler
from flask_socketio import SocketIO, emit
from app.controllers.mqtt_handler import init_mqtt_socketio, sensor_data  # Import từ mqtt_handler.py
from .get_sensor_data import handle_get_sensor_data
from .get_device_status import handle_get_device_status
from .control_device import handle_control_device 
from .wind_speed import get_wind_speed
# from .query_sensor_data import handle_query_sensor_data 
from app.models.database import Database


# Khởi tạo SocketIO
main_controller = Blueprint('main_controller', __name__)

@main_controller.route('/api/v1/sensor/pulldata', methods=['GET'])
def get_sensor_data():
    """API để lấy dữ liệu cảm biến gần nhất."""
    #      ---------------  bai 5 ------------                  #
    sync = request.args.get('wind_speed')
    # print(sync)
    if (sync != None):
        return get_wind_speed(request.args.get('thres'))
    #      ---------------  bai 5 ------------                  #
    isrt = request.args.get('realtime')
    isrv = request.args.get('reverse')
    if (isrt == None):
        isrt = "0"
    if (isrv == None):
        isrv = "0"
    return handle_get_sensor_data(isrt, isrv) 

@main_controller.route('/api/v1/device/status', methods=['GET'])
def get_device_status():
    """API lấy dữ liệu."""
    return handle_get_device_status() 

@main_controller.route('/api/v1/device/control', methods=['POST'])
def control_device():
    """API để điều khiển thiết bị."""
    command = request.get_json().get('cmd', None)
    # print(command)
    return handle_control_device(command) 

@main_controller.route('/api/v1/log/query', methods=['POST'])
def query_sensor_data():
    """API để lấy dữ liệu sensor."""
    db = Database()
    data = request.json
    log_type = data.get('type', 'sensorLog')  # Default to 'sensorLog' if type is not provided



    #      ---------------  bai 5 ------------                  #
    if (log_type == 'statistic'):
        logs = db.count_wind_speed_above(data.get('thres'))
        return jsonify(logs) 
    #      ---------------  bai 5 ------------                  #



    start_date = data.get('startDate')
    end_date = data.get('endDate')
    sort = data.get('sort', 'latest')
    limit = data.get('numberOfRecords', 100)
    filters = data.get('filters', {})

    # Determine which table to query based on type
    if log_type == 'actionLog':
        table = 'actionhistory'
    elif log_type == 'sensorLog':
        table = 'realtimedata'
    else:
        return jsonify({"error": "Invalid log type specified"}), 400

    print(f"table: {table}, start:{start_date}, end: {end_date}, filters: {filters}, sort:{sort}, limit: {limit}")

    # Fetch data using the query_logs method
    logs = db.query_logs(table=table, start_date=start_date, end_date=end_date, filters=filters, sort=sort, limit=limit)
    # print(logs)
    
    return jsonify(logs)

@main_controller.route('/')
def one():
    return render_template('base.html')

@main_controller.route('/home')
def home():
    return render_template('home.html')

@main_controller.route('/data_sensor')
def data_sensor():

    return render_template('data_sensor.html')#, logs=logs_paginated, page=page, total=total, per_page=per_page)

@main_controller.route('/action_history')
def action_history():

    return render_template('action_history.html')#, logs=logs_paginated, page=page, total=total, per_page=per_page)

@main_controller.route('/profile')
def profile():
    return render_template('profile.html')

#      ---------------  bai 5 ------------                  #
@main_controller.route('/bai5')
def bai5():
    return render_template('bai5.html')
#      ---------------  bai 5 ------------                  #