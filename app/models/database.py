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
        """Chèn dữ liệu cảm biến vào bảng chỉ định."""
        if not self.connection:
            print("Not connected to database.")
            return
        try:
            cursor = self.connection.cursor()
            query = f"""
            INSERT INTO {table} (timestamp, light_level, humidity, temperature)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (timestamp, light_level, humidity, temperature))
            self.connection.commit()
        except Error as e:
            print(f"Error inserting data: {e}")

    def insert_device_history(self, timestamp, topic, command, status):
        """Chèn lịch sử thao tác của thiết bị."""
        if not self.connection:
            print("Not connected to database.")
            return
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO actionhistory (timestamp, topic, command, status)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (timestamp, topic.upper(), command, status))
            self.connection.commit()
        except Error as e:
            print(f"Error inserting device history: {e}")
    def search_data(self, table, search_term):
        """Tìm kiếm chuỗi trong các trường của bảng."""
        if not self.connection:
            print("Not connected to database.")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"""
            SELECT * FROM {table}
            WHERE timestamp LIKE %s
               OR light_level LIKE %s
               OR humidity LIKE %s
               OR temperature LIKE %s
            """
            like_term = f"%{search_term}%"
            cursor.execute(query, (like_term, like_term, like_term, like_term))
            rows = cursor.fetchall()
            return rows 
        except Error as e:
            print(f"Error searching data: {e}")
            return []

    def get_data(self, table, reverse=True, limit=100):
        """Lấy dữ liệu từ bảng với số lượng bản ghi giới hạn."""
        if not self.connection:
            print("Not connected to database.")
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"SELECT * FROM {table} ORDER BY id {'DESC' if reverse else 'ASC'} LIMIT %s"
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            rows.reverse()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []
    def get_status_device(self, device, limit=1):
        """Lấy dữ liệu từ bảng với số lượng bản ghi giới hạn."""
        if not self.connection:
            print("Not connected to database.")
            return []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM actionhistory WHERE topic=%s and status='Successfull' ORDER BY timestamp DESC LIMIT %s;"
            cursor.execute(query, (device.upper(), limit))
            rows = cursor.fetchall()
            rows.reverse()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []



    def close_connection(self):
        """Đóng kết nối database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
