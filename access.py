import sqlite3
from auth import hash_password
from constants import db_file_path

def query_data(username):
    """
    Query data from the database with access control based on the user group.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Retrieve the user group for the given username
    cursor.execute('SELECT user_group FROM users WHERE username = ?', (username,))
    user_group = cursor.fetchone()

    if user_group:
        # Determine the fields to return based on user group
        if user_group[0] == 'H':
            query = 'SELECT * FROM healthcare'
        else:  # Group R
            query = 'SELECT age, weight, height, health_history FROM healthcare'

        # Execute query and fetch results
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
        return data
    else:
        conn.close()
        return "User not found."

def add_data(username, data_item):
    """
    Add new data item to the database with a hash for integrity, restricted to users from group H.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Check if user is in group H
    cursor.execute('SELECT user_group FROM users WHERE username = ?', (username,))
    user_group = cursor.fetchone()

    if user_group and user_group[0] == 'H':
        # Concatenate data fields and compute the hash
        data_string = ''.join(map(str, data_item))
        data_hash = hash_password(data_string)  # Reusing the hash function from user authentication

        # Append the hash to the data item
        data_item_with_hash = data_item + (data_hash,)

        # Insert new data item with hash into healthcare table
        try:
            cursor.execute('INSERT INTO healthcare (first_name, last_name, gender, age, weight, height, health_history, data_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                           data_item_with_hash)
            conn.commit()
            result = "Data item added successfully with integrity hash."
        except Exception as e:
            result = str(e)
    else:
        result = "Only users from group H can add new data items."

    conn.close()
    return result

