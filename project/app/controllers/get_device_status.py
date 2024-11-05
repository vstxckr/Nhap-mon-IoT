from app.models.database import Database
from flask import jsonify
def handle_get_device_status():
    db = Database()
    data =db.get_device_log(200)
    db.close_connection()
    return data