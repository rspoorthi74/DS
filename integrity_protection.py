import sqlite3
from auth import hash_password
from constants import dataset_file_path, db_file_path

def verify_data_integrity(data_item, stored_hash):
    """
    Verify the integrity of a data item by comparing the computed hash with the stored hash.
    """
    # Concatenate data fields and compute the hash
    data_string = ''.join(map(str, data_item))
    computed_hash = hash_password(data_string)

    # Compare the computed hash with the stored hash
    return computed_hash == stored_hash


def retrieve_data(criterion):
    """
    Retrieve a data item and its hash from the database based on a given criterion.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # SQL query to retrieve data and its hash
    query = 'SELECT first_name, last_name, gender, age, weight, height, health_history, data_hash FROM healthcare WHERE first_name = ? OR last_name = ?'
    
    # Execute the query
    cursor.execute(query, (criterion, criterion))
    result = cursor.fetchone()

    conn.close()
    return result

def get_expected_count(username):
    """
    Get the expected count of data items the user should be able to access.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Check user group
    cursor.execute('SELECT user_group FROM users WHERE username = ?', (username,))
    user_group = cursor.fetchone()

    if user_group:
        if user_group[0] == 'H':
            cursor.execute('SELECT COUNT(*) FROM healthcare')
        else:  # Group R
            cursor.execute('SELECT COUNT(*) FROM healthcare')  # Same count, but different access

        expected_count = cursor.fetchone()[0]
        conn.close()
        return expected_count
    else:
        conn.close()
        return None

def query_data_with_completeness_check(username):
    """
    Query data and check for completeness based on the user group.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Check user group
    cursor.execute('SELECT user_group FROM users WHERE username = ?', (username,))
    user_group = cursor.fetchone()

    if not user_group:
        conn.close()
        return None, "User not found."

    # Perform the query
    if user_group[0] == 'H':
        cursor.execute('SELECT * FROM healthcare')
    else:  # Group R
        cursor.execute('SELECT age, weight, height, health_history FROM healthcare')

    data = cursor.fetchall()
    actual_count = len(data)

    # Get the expected count of data items
    if user_group[0] == 'H':
        cursor.execute('SELECT COUNT(*) FROM healthcare')
    else:  # Group R
        cursor.execute('SELECT COUNT(*) FROM healthcare')  # Same count, but different access

    expected_count = cursor.fetchone()[0]

    conn.close()

    # Check for completeness
    if actual_count == expected_count:
        return data, "Data completeness verified."
    else:
        return data, "Data completeness might be compromised."


