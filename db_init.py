import sqlite3
import pandas as pd
from constants import dataset_file_path, db_file_path


# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_file_path)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# SQL query to create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS healthcare (
    first_name TEXT,
    last_name TEXT,
    gender BOOLEAN,
    age INTEGER,
    weight REAL,
    height REAL,
    health_history TEXT
);
'''

# Execute the SQL command to create the table
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("SQLite database and healthcare table created successfully.")

# Reconnect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Load the CSV file into a pandas DataFrame
data = pd.read_csv(dataset_file_path)

# Insert data from DataFrame to the SQLite table
data.to_sql('healthcare', conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data from the CSV file has been successfully imported into the healthcare table.")

# Reconnect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# SQL query to create a user table
create_user_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT
);
'''

# Execute the SQL command to create the user table
cursor.execute(create_user_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("User table created successfully in the SQLite database.")


# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# SQL query to add a group column to the users table
alter_table_query = '''
ALTER TABLE users
ADD COLUMN user_group CHAR(1) DEFAULT 'R';
'''

# Execute the SQL command to alter the table
try:
    cursor.execute(alter_table_query)
    result = "User table altered successfully, added user_group column."
except sqlite3.OperationalError as e:
    result = str(e)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(result)


# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# SQL query to add a hash column to the healthcare table
alter_healthcare_table_query = '''
ALTER TABLE healthcare
ADD COLUMN data_hash TEXT;
'''

# Execute the SQL command to alter the table
try:
    cursor.execute(alter_healthcare_table_query)
    result = "Healthcare table altered successfully, added data_hash column."
except sqlite3.OperationalError as e:
    result = str(e)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(result)
