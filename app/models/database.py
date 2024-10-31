# database.py
import mysql.connector
from mysql.connector import Error
import json

class Database:
    def __init__(self, host="localhost", user="root", password="", database="manhdx"):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None

    def insert_data(self, table, timestamp, light_level, humidity, temperature):
        if not self.connection:
            print("Not connected to database.")
            return
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO """+table+""" (timestamp, light_level, humidity, temperature)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (timestamp, light_level, humidity, temperature))
            self.connection.commit()
            # print("Data inserted successfully.")
        except Error as e:
            print(f"Error inserting data: {e}")

    #def insert_device_history(self, topic, command):
        

    def get_data(self, table, limit=100):
        """Lấy dữ liệu từ bảng realtimedata với số lượng bản ghi giới hạn."""
        if not self.connection:
            print("Not connected to database.")
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM "+table+" ORDER BY id DESC LIMIT %s"
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            rows.reverse()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
