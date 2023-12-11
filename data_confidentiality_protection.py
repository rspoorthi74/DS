from cryptography.fernet import Fernet
from auth import *
from constants import *


# Generate a key for encryption and decryption (In a real application, store this key securely)
with open("encryption_key.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)


def encrypt_data(data):
    """Encrypt sensitive data."""
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt sensitive data."""
    # print(data)
    return cipher_suite.decrypt(data.encode()).decode()

def add_data_with_hash_and_encryption(username, data_item):
    """
    Add new data item to the database with encrypted sensitive fields and a hash for integrity.
    """
    encrypted_gender = encrypt_data(str(data_item[2]))  # Ensure gender is treated as a string
    encrypted_age = encrypt_data(str(data_item[3]))    # Ensure age is treated as a string
    encrypted_data_item = data_item[:2] + (encrypted_gender, encrypted_age) + data_item[4:]

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Check if user is in group H
    cursor.execute('SELECT user_group FROM users WHERE username = ?', (username,))
    user_group = cursor.fetchone()

    if user_group and user_group[0] == 'H':
        # Concatenate data fields and compute the hash
        data_string = ''.join(map(str, encrypted_data_item))
        data_hash = hash_password(data_string)  # Reusing the hash function from user authentication

        # Append the hash to the data item
        data_item_with_hash = encrypted_data_item + (data_hash,)

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



def query_data_with_completeness_check_and_decryption(username, query):
    """
    Query data and decrypt sensitive fields, also check for completeness.
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
        cursor.execute('SELECT * FROM healthcare WHERE first_name = ?', (query,))
    else:  # Group R
        cursor.execute('SELECT age, weight, height, health_history FROM healthcare WHERE first_name = ?', (query,))

    data = cursor.fetchall()
    actual_count = len(data)

    # Get the expected count of data items
    if user_group[0] == 'H':
        cursor.execute('SELECT COUNT(*) FROM healthcare WHERE first_name = ?', (query,))
    else:  # Group R
        cursor.execute('SELECT COUNT(*) FROM healthcare WHERE first_name = ?', (query,)) 

    expected_count = cursor.fetchone()[0]

    conn.close()

    completeness_message = ""
    # Check for completeness
    if actual_count == expected_count:
        completeness_message = "Data completeness verified."
    else:
        completeness_message = "Data completeness might be compromised."
        
    decrypted_data = []
    for item in data:
        # Data item structure: (first_name, last_name, encrypted_gender, encrypted_age, weight, height, health_history, data_hash)
        decrypted_gender = decrypt_data(str(item[2]) ) # item[2] should be an encrypted string
        decrypted_age = decrypt_data(item[3])     # item[3] should be an encrypted string
        decrypted_item = item[:2] + (decrypted_gender, decrypted_age) + item[4:-1]  # Exclude hash from display
        decrypted_data.append(decrypted_item)

    return decrypted_data, completeness_message


