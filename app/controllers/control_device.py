import subprocess
from flask import jsonify
from app.models.database import Database

db = Database()

def handle_control_device(command):
    # Giả sử thực hiện lệnh điều khiển thành công
    result = {"status": "success", "command": command}
    topic_light = "home/light"
    topic_fan = "home/fan"
    topic_air = "home/aircondition"
    topic_all = "home/all"
    # Trả về phản hồi JSON
    a = command.split()
    topic = ''
    if ('fan' in a[0]):
        topic = topic_fan
    elif ('light' in a[0]):
        topic = topic_light
    elif ('air' in a[0]):
        topic = topic_air
    elif ('all' in a[0]):
        topic = topic_all
    else:
        print("invalid!")
        pass 
    subprocess.run([
        "mosquitto_pub",
        "-h", "localhost",
        "-t", topic,
        "-m", a[1].upper(),
        "-u", "ManhDX",
        "-P", "B21DCAT124",
        "-p", "8668"
    ])
    # db.insert('device_history', '' 'command')
    # db.insert_device_history()
    print("publish data: %s" % command)
    return jsonify(result)