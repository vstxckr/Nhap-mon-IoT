# run.py
import eventlet
eventlet.monkey_patch()  # MUST be the first import
from app import create_app
from app.controllers.mqtt_handler import socketio, init_mqtt_socketio

app = create_app()
init_mqtt_socketio(app)  # Initialize MQTT and SocketIO with the app

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=False, use_reloader=False)
