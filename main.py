import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Oure1234!%'
    )
    if connection.is_connected():
        print("Connected to MySQL successfully!")
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        print("Databases:")
        for db in cursor:
            print(db)
except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
