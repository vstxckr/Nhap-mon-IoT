# mqtt_handler.py
from datetime import datetime
import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from pathlib import Path
from app.models.database import Database  # Import lớp Database
import threading

# Tạo một đối tượng Lock
file_lock = threading.Lock()


# Initialize MQTT and SocketIO instances without the app initially
mqtt_handler = Mqtt()
socketio = SocketIO(cors_allowed_origins="*")

last_time = ""

# Khởi tạo đối tượng database
db = Database()
# biến chứa data thời gian thực
sensor_data = {}

# biến chứa log
log = ""
# biến chứa giá trị thời gian hiện tại
current_time = ""

# mảng chứa biến giá trị theo phút để tính giá trị trung bình.
Light = []
Humid = []
Temp = []

# lấy dữ liệu từ bảng chartdata từ trong db và lưu vào file sensor_log.json
with file_lock: 
    with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log.json", "w") as f:
        data = db.get_data("chartdata")
        if (len(data) > 0):
            json.dump(data, f, indent=4)

# lấy giá trị thời gian cuối cùng để làm thời gian trước đó cho chương trình.
with file_lock: 
    if (Path("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log.json").exists()):
        with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log.json", "r") as f:
            last_time = json.load(f)[-1]["timestamp"]


def init_mqtt_socketio(app):
    """Initialize MQTT and SocketIO with the Flask app."""
    mqtt_handler.init_app(app)
    socketio.init_app(app)  # Ensuure socketio is initialized with the app



@mqtt_handler.on_message()
def handle_mqtt_message(client, userdata, msg):
    global current_time, sensor_data, last_time, log

    # chuyển về code
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_time_m = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = eval(msg.payload.decode('utf-8'))

    # assign cho biến cục bộ những giá trị thời gian thực
    cur_light = temp.get('light_level')
    cur_humid = temp.get('humidity')
    cur_temp = temp.get('temperature')

    # hàm chứa những giá trị theo từng phút
    Light.append(cur_light)
    Humid.append(cur_humid)
    Temp.append(cur_temp)
    
    # insert data vào bảng realtimedata
    db.insert_data("realtimedata", current_time_m, cur_light, cur_humid, cur_temp)

    # log check
    print(last_time + " and " + current_time)

    # nếu thời gian theo phút thay đổi
    if last_time != current_time:
        # thực hiện tính giá trị trung bình
        avg_light = round(sum(Light)/len(Light) if len(Light) > 0 else 0, 2)
        avg_humidity = round(sum(Humid)/len(Humid) if len(Humid) > 0 else 0, 2)
        avg_temperature = round(sum(Temp)/len(Temp) if len(Temp) > 0 else 0, 2)

        # thực hiện tạo dict
        data = {
            "timestamp": current_time,
            "light_level": avg_light,
            "humidity":  avg_humidity,
            "temperature": avg_temperature
        }

        # đẩy lên chartdata là bảng chứa bản ghi theo phút
        db.insert_data("chartdata", current_time, avg_light, avg_humidity, avg_temperature)

        # xóa list để thực hiện cho phút kế tiếp
        Light.clear()
        Humid.clear()
        Temp.clear()

        # mở file và ghi vào sensor_log
        with file_lock:
            cache = db.get_data("chartdata")
            with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log.json", "w") as f:
                json.dump(cache, f, indent=4)
        # khởi tạo lại last_time
        last_time = current_time

    rt_data = db.get_data("realtimedata", 200)
    with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\app\\data\\sensor_log_realtime.json", "w") as f:
        json.dump(rt_data, f, indent=4)

    # update sensor_data để emit lên socket
    sensor_data.update(temp)
    
    try:
        # print(f"Updated sensor data: {sensor_data}")

        # socket emit
        socketio.emit('sensor_data', sensor_data)
    except Exception as e:
        print(f"Error processing message: {e}")

@mqtt_handler.on_connect()
def handle_connect(client, userdata, flags, rc):
    topic = "home/sensors"
    if rc == 0:
        client.subscribe(topic)
    else:
        print(f"Failed to connect, return code {rc}")
