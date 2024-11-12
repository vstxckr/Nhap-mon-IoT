import json
from app.models.database import Database

db = Database()

def get_wind_speed(thres):
    return db.get_data(table='bai5',reverse=True, limit=int(thres))