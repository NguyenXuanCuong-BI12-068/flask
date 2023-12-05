import mysql.connector
from mysql.connector import Error
def initialize_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='123456',
            database='Account'
        )
        print("connect success")
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
initialize_database()