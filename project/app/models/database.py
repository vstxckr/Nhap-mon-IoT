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
                # print("Connected to MySQL database")
                pass
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None

    def insert_wind_speed(self, timestamp, wind_speed):
        """Chèn dữ liệu tốc độ gió vào bảng bai5."""
        if not self.connection:
            print("Not connected to database.")
            return
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO bai5 (timestamp, wind_speed)
            VALUES (%s, %s)
            """
            cursor.execute(query, (timestamp, wind_speed))
            self.connection.commit()
        except Error as e:
            print(f"Error inserting wind speed data: {e}")

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
    def get_device_log(self, limit=100):
        """Lấy dữ liệu từ bảng action history"""
        if not self.connection:
            print("Not connected to database.")
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM actionhistory  ORDER BY id DESC LIMIT %s;"
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def query_logs(self, table, start_date=None, end_date=None, filters={}, sort='latest', limit=100):
        """Query logs with specific filters, date range, sort order, and limit."""
        if not self.connection:
            print("Not connected to database.")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"SELECT * FROM {table} WHERE 1=1"
            params = []

            # Apply date range filtering
            if start_date:
                query += " AND timestamp >= %s"
                params.append(start_date)
            if end_date:
                query += " AND timestamp <= %s"
                params.append(end_date)

            # Apply column filters
            for field, value in filters.items():
                if value:
                    query += f" AND {field} LIKE %s"
                    params.append(f"%{value}%")

            # Apply sorting
            order = 'DESC' if sort == 'latest' else 'ASC'
            query += f" ORDER BY timestamp {order} LIMIT %s"
            params.append(limit)
            print(query, params)

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error querying logs: {e}")
            return []

    def query_device_history(self, start_date=None, end_date=None, filters={}, sort='latest', limit=100):
        """Query device action history with filters, date range, sort order, and limit."""
        return self.query_logs('actionhistory', start_date, end_date, filters, sort, limit)


    def convert_to_json(self, data):
        """Convert MySQL data result to JSON format."""
        return json.dumps(data, default=str)

    def close_connection(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            # print("Database connection closed.")
# bai 5
    def count_wind_speed_above(self, speed_threshold):
        """Đếm số bản ghi có wind_speed lớn hơn giá trị speed_threshold."""
        if not self.connection:
            print("Not connected to database.")
            return 0
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM bai5 WHERE wind_speed > %s"
            cursor.execute(query, (speed_threshold,))
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Error counting wind speed records: {e}")
            return 0