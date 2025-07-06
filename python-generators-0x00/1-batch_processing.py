import mysql.connector

def stream_users_in_batches(batch_size):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Set your MySQL root password here
        database='ALX_prodev'
    )
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_data')
        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
    finally:
        cursor.close()
        conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        filtered = [user for user in batch if float(user['age']) > 25]  # 2nd loop (list comp)
        yield filtered

# Example usage (uncomment to test):
# for batch in batch_processing(10):
#     print(batch)
