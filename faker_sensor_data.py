import subprocess
import time
import random
import json

while True:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S %m-%d-%Y", t)
    data = json.dumps({
        "temperature": 28,
        "humidity": random.randint(83, 85),
        "light_level": random.randint(40, 42),
        "time": current_time,
        "light": 0,
        "air": 0,
        "fan": 0,
        "all": 0
    })

    # Use subprocess.run to execute the command
    subprocess.run([
        "mosquitto_pub",
        "-h", "localhost",
        "-t", "home/sensors",
        "-m", data,
        "-u", "ManhDX",
        "-P", "B21DCAT124",
        "-p", "8668"
    ])
    print("publish data: %s" % data)
    time.sleep(2)
