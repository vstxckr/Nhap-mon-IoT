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
time_lim = 3

# mảng chứa biến giá trị theo phút để tính giá trị trung bình.
Light = []
Humid = []
Temp = []

run_once = False

cnt_light = 0
cnt_air = 0
cnt_fan = 0
cnt_all = 0

chk_light = False
chk_fan = False
chk_air = False
chk_all = False

val_light = False
val_fan = False
val_air = False
val_all = False

fan_dbs = light_dbs = air_dbs = all_dbs = None


# lấy dữ liệu từ bảng chartdata từ trong db và lưu vào file sensor_log.json
with file_lock: 
    with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\project\\app\\data\\sensor_log.json", "w") as f:
        data = db.get_data("chartdata")
        if (len(data) > 0):
            json.dump(data, f, indent=4)

# lấy giá trị thời gian cuối cùng để làm thời gian trước đó cho chương trình.
with file_lock: 
    if (Path("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\project\\app\\data\\sensor_log.json").exists()):
        with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\project\\app\\data\\sensor_log.json", "r") as f:
            last_time = json.load(f)[-1]["timestamp"]


def init_mqtt_socketio(app):
    """Initialize MQTT and SocketIO with the Flask app."""
    mqtt_handler.init_app(app)
    socketio.init_app(app)  # Ensuure socketio is initialized with the app



@mqtt_handler.on_message()
def handle_mqtt_message(client, userdata, msg):
    global current_time, sensor_data, last_time, log, run_once, time_lim
    global cnt_light, cnt_air, cnt_fan, cnt_all
    global chk_light, chk_air, chk_fan, chk_all
    global val_light, val_air, val_fan, val_all
    global fan_dbs, light_dbs, air_dbs, all_dbs

    # chuyển về code
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    current_time_m = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    topic = msg.topic

    if (topic == "home/sensors"):
        

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
        db.insert_wind_speed(current_time_m, temp.get("wind_speed"))

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
                with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\project\\app\\data\\sensor_log.json", "w") as f:
                    json.dump(cache, f, indent=4)
            # khởi tạo lại last_time
            last_time = current_time

        rt_data = db.get_data("realtimedata", limit=200)
        with open("C:\\Users\\vstxckr\\Desktop\\Tren_truong\\IoT_MVC\\project\\app\\data\\sensor_log_realtime.json", "w") as f:
            json.dump(rt_data, f, indent=4)
        
        temp["timestamp"] = current_time_m

        # update sensor_data để emit lên socket
        sensor_data.update(temp)
        
        try: # print(f"Updated sensor data: {sensor_data}") # socket emit
            socketio.emit('sensor_data', sensor_data)
        except Exception as e:
            print(f"Error processing message: {e}")


        if (run_once == False):
            run_once = True

            fan_temp = "ON" if temp.get('fan') == 1 else "OFF"
            light_temp = "ON" if temp.get('light') == 1 else "OFF"
            air_temp = "ON" if temp.get('air') == 1 else "OFF"
            all_temp = "ON" if temp.get('all') == 1 else "OFF"

            # if ()
            print(f"fan_temp = {fan_temp}, light_temp = {light_temp}, air_temp = {air_temp}, all_temp = {all_temp}")

            if (all_temp != all_dbs):
                val_all = True if all_temp == "ON" else False
                db.insert_device_history(current_time_m, "all", all_temp, "Update")
            else:
                if (fan_temp != fan_dbs):
                    val_fan = True if fan_temp == "ON" else False
                    db.insert_device_history(current_time_m, "fan", fan_temp, "Update")
                if (light_temp != light_dbs):
                    val_light = True if light_temp == "ON" else False
                    db.insert_device_history(current_time_m, "light", light_temp, "Update")
                if (air_temp != air_dbs):
                    val_air = True if air_temp == "ON" else False
                    db.insert_device_history(current_time_m, "air", air_temp, "Update")

        # print()
        # print()
        # print(f'chk_fan = {chk_fan}, val_fan = {val_fan}, real = {temp.get('fan')}')
        # print(f'chk_air = {chk_air}, val_air = {val_air}, real = {temp.get('air')}')
        # print(f'chk_light = {chk_light}, val_light = {val_light}, real = {temp.get('light')}')
        # print(f'chk_all = {chk_all}, val_all = {val_all}, real = {temp.get('all')}')
        if (temp.get('all') == 1 and chk_all == False):
            val_all = True
        elif (temp.get('all') == 0 and chk_all == False):
            val_all = False
        if (temp.get('light') == 1 and chk_light == False):
            val_light = True
        if (temp.get('air') == 1 and chk_air == False):
            val_air = True
        if (temp.get('fan') == 1 and chk_fan == False):
            val_fan = True
            

        if (chk_fan == True):
            cnt_fan += 1

        if (chk_light == True):
            cnt_light += 1

        if (chk_air == True):
            cnt_air += 1

        if (chk_all == True):
            cnt_all += 1

        if (chk_fan == True):
            if (cnt_fan > time_lim and val_fan == False and temp.get('fan') == 0):
                chk_fan = False
                db.insert_device_history(current_time_m, "FAN", "ON", "Failed")
                print("Fan on failed")
                cnt_fan = 0
            elif (val_fan == False and temp.get('fan') == 1):
                chk_fan = False 
                val_fan = True 
                db.insert_device_history(current_time_m, "FAN", "ON", "Successfull")
                print("Fan on successfull")
                cnt_fan = 0
            elif (cnt_fan > time_lim and val_fan == True and temp.get('fan') == 1):
                chk_fan = False 
                db.insert_device_history(current_time_m, "FAN", "OFF", "Failed")
                print("Fan off failed")
                cnt_fan = 0
            elif (val_fan == True and temp.get('fan') == 0):
                chk_fan = False 
                val_fan = False
                db.insert_device_history(current_time_m, "FAN", "OFF", "Successfull")
                print("Fan on successfull")
                cnt_fan = 0
        if (chk_light == True):
            if (cnt_light > time_lim and val_light == False and temp.get('light') == 0):
                chk_light = False
                db.insert_device_history(current_time_m, "LIGHT", "ON", "Failed")
                print("Light on Failed")
                cnt_light = 0
            elif (val_light == False and temp.get('light') == 1):
                chk_light= False 
                val_light = True 
                db.insert_device_history(current_time_m, "LIGHT", "ON", "Successfull")
                print("Light on successfull")
                cnt_light = 0
            elif (cnt_light > time_lim and val_light == True and temp.get('light') == 1):
                chk_light = False 
                db.insert_device_history(current_time_m, 'LIGHT', "OFF", "Failed")
                print("Light off Failed")
                cnt_light = 0
            elif (val_light == True and temp.get('light') == 0):
                chk_light = False 
                val_light = False
                db.insert_device_history(current_time_m, "LIGHT", "OFF", "Successfull")
                print("Light off successfull")
                cnt_light = 0

        if (chk_air == True):
            if (cnt_air > time_lim and val_air == False and temp.get('air') == 0):
                chk_air = False
                db.insert_device_history(current_time_m, "AIR", "ON", "Failed")
                print("Air on Failed")
                cnt_air = 0
            elif (val_air == False and temp.get('air') == 1):
                chk_air = False 
                val_air = True 
                db.insert_device_history(current_time_m, 'AIR', "ON", "Successfull")
                print("Air on successfull")
                cnt_air = 0
            elif (cnt_air > time_lim and val_air == True and temp.get('air') == 1):
                chk_air = False 
                db.insert_device_history(current_time_m, 'AIR', "OFF", "Failed")
                cnt_air = 0
                print("Air off Failed ")

            elif (val_air == True and temp.get('air') == 0):
                chk_air = False 
                val_air = False
                db.insert_device_history(current_time_m, 'AIR', "OFF", "Successfull")
                print("Air off successfull")
                cnt_air = 0

        if (chk_all == True):
            if (cnt_all > time_lim and val_all == False and temp.get('all') == 0):
                chk_all = False
                db.insert_device_history(current_time_m, 'ALL', "ON", "Failed")
                print("All on Failed ")
                cnt_all = 0
            elif (val_all == False and temp.get('all') == 1):
                chk_all = False 
                val_all = True 
                val_air = False
                val_light = False
                val_fan = False
                db.insert_device_history(current_time_m, 'ALL', "ON", "Successfull")
                print("All on successfull")
                cnt_all = 0
            elif (cnt_all > time_lim and val_all == True and temp.get('all') == 1):
                chk_all = False 
                db.insert_device_history(current_time_m, 'ALL', "OFF", "Failed")
                print("All off Failed ")
                cnt_all = 0

            elif (val_all == True and temp.get('all') == 0):
                chk_all = False 
                val_all = False
                val_air = False
                val_light = False
                val_fan = False
                db.insert_device_history(current_time_m, 'ALL', "OFF", "Successfull")
                print("All off successfull")
                cnt_all = 0

    elif (topic == "check/light"):
        chk_light = True
    elif (topic == "check/fan"):
        chk_fan = True
    elif (topic == "check/air"):
        chk_air = True
    elif (topic == "check/all"):
        print("check/all topic recevied")
        chk_all = True

@mqtt_handler.on_connect()
def handle_connect(client, userdata, flags, rc):
    global fan_dbs, air_dbs, all_dbs, light_dbs
    topic = "home/sensors"
    check_light = "check/light"
    check_fan = "check/fan"
    check_air = "check/air"
    check_all = "check/all"


    fan_dbs = db.get_status_device('fan')
    if (len(fan_dbs) > 0):
        time_fan = fan_dbs[0]["timestamp"]
        fan_dbs = fan_dbs[0]["command"]

    light_dbs = db.get_status_device('light')
    if (len(light_dbs) > 0):
        time_light = light_dbs[0]["timestamp"]
        light_dbs = light_dbs[0]['command']

    air_dbs = db.get_status_device('air')
    if (len(air_dbs) > 0):
        time_air = air_dbs[0]["timestamp"]
        air_dbs = air_dbs[0]["command"]

    all_dbs = db.get_status_device('all')
    if (len(all_dbs) > 0):
        time_all = all_dbs[0]["timestamp"]
        all_dbs = all_dbs[0]["command"]

    print(f"air_dbs = {air_dbs}, light_dbs = {light_dbs}, fan_dbs = {fan_dbs}, all_dbs = {all_dbs}")

    if (time_light != None):
        time_light = datetime.strptime(time_light, "%Y-%m-%d %H:%M:%S")
    if (time_fan != None):
        time_fan = datetime.strptime(time_fan, "%Y-%m-%d %H:%M:%S")
    if (time_air != None):
        time_air = datetime.strptime(time_air, "%Y-%m-%d %H:%M:%S")
    if (time_all != None):
        time_all = datetime.strptime(time_all, "%Y-%m-%d %H:%M:%S")

    print(f"air_dbs = {time_air}, light_dbs = {time_light}, fan_dbs = {time_fan}, all_dbs = {time_all}")
    
    if (all_dbs != None and time_all > time_air):
        air_dbs = all_dbs
    if (all_dbs != None and time_all > time_light):
        light_dbs = all_dbs
    if (all_dbs != None and time_all > time_fan):
        fan_dbs = all_dbs

    print(f"air_dbs = {air_dbs}, light_dbs = {light_dbs}, fan_dbs = {fan_dbs}, all_dbs = {all_dbs}")
    
    if rc == 0:
        client.subscribe(topic)
        client.subscribe(check_fan)
        client.subscribe(check_air)
        client.subscribe(check_light)
        client.subscribe(check_all)
    else:
        print(f"Failed to connect, return code {rc}")

