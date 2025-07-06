import mysql.connector

def paginate_users(page_size, offset):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Set your MySQL root password here
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_data LIMIT %s OFFSET %s', (page_size, offset))
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage (uncomment to test):
# for page in lazy_paginate(10):
#     print(page)
