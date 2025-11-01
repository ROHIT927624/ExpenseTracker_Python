import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1341"
    )
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")