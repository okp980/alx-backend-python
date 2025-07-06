import mysql.connector

def stream_user_ages():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Set your MySQL root password here
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT age FROM user_data')
        for (age,) in cursor:
            yield float(age)
    finally:
        cursor.close()
        conn.close()

def print_average_age():
    total = 0.0
    count = 0
    for age in stream_user_ages():  # 1 loop
        total += age
        count += 1
    average = total / count if count else 0
    print(f"Average age of users: {average}")

if __name__ == '__main__':
    print_average_age()
