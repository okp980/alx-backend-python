# seed.py Implementation

This script sets up a MySQL database, creates a table, populates it with data from a CSV file, and provides a generator to stream rows one by one.

## Features

- **Database Setup:** Creates a database `ALX_prodev` and a table `user_data` if they do not exist.
- **Table Schema:**
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- **CSV Data Import:** Reads from `user_data.csv` and inserts data, skipping duplicates.
- **Row Streaming:** Provides a generator to yield rows from the table one by one.

## Functions

- `connect_db()`: Connects to the MySQL server (no database specified).
- `create_database(connection)`: Creates the `ALX_prodev` database if it does not exist.
- `connect_to_prodev()`: Connects to the `ALX_prodev` database.
- `create_table(connection)`: Creates the `user_data` table with the required schema if it does not exist.
- `insert_data(connection, data)`: Inserts data from a list of dictionaries into the table, skipping duplicates based on name and email.
- `stream_rows(connection)`: Generator that yields each row from the `user_data` table as a dictionary.
- `read_csv_data(filename)`: Reads data from a CSV file and returns it as a list of dictionaries.

## Usage

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
2. **Configure MySQL credentials:**
   - Edit `seed.py` and set your MySQL `user` and `password` if different from the defaults.
3. **Run the script:**
   ```
   python3 seed.py
   ```
   - This will:
     - Create the database and table if needed
     - Insert data from `user_data.csv`
     - Print each row from the table using the generator

## Notes

- Ensure MySQL server is running and accessible.
- The script skips inserting duplicate users (same name and email).
- The generator can be reused in other scripts to process large datasets efficiently.
