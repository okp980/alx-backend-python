import mysql.connector

def stream_users():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Set your MySQL root password here
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_data')
        for row in cursor:
            yield row
    finally:
        cursor.close()
        conn.close()

# Example usage (uncomment to test):
# for user in stream_users():
#     print(user)
