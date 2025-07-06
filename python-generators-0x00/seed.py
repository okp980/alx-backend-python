import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE = 'user_data.csv'

# 1. Connect to MySQL server (no DB specified)
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=''  # Set your MySQL root password here
    )

# 2. Create database if not exists
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    finally:
        cursor.close()

# 3. Connect to ALX_prodev DB
def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Set your MySQL root password here
        database=DB_NAME
    )

# 4. Create user_data table if not exists
def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        ''')
    finally:
        cursor.close()

# 5. Insert data if not exists
def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        for row in data:
            # Check if user already exists by name and email
            cursor.execute(f"SELECT user_id FROM {TABLE_NAME} WHERE name=%s AND email=%s", (row['name'], row['email']))
            if cursor.fetchone():
                continue  # Skip duplicates
            user_id = str(uuid.uuid4())
            cursor.execute(f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                           (user_id, row['name'], row['email'], row['age']))
        connection.commit()
    finally:
        cursor.close()

# 6. Generator to stream rows one by one
def stream_rows(connection):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        for row in cursor:
            yield row
    finally:
        cursor.close()

# 7. Read CSV data
def read_csv_data(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

if __name__ == '__main__':
    # 1. Connect to MySQL server
    conn = connect_db()
    create_database(conn)
    conn.close()

    # 2. Connect to ALX_prodev
    conn = connect_to_prodev()
    create_table(conn)

    # 3. Read CSV and insert data
    data = read_csv_data(CSV_FILE)
    insert_data(conn, data)

    # 4. Stream rows one by one
    print('Streaming rows:')
    for row in stream_rows(conn):
        print(row)
    conn.close()
