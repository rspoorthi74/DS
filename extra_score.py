import sqlite3
from pyope.ope import OPE, OutOfRangeError
from constants import db_file_path

# Initialize the OPE cipher with a secret key
cipher = OPE(b'secret_key')

def encrypt_weights():
    """
    Encrypts the 'Weight' column in the database using OPE.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Select all weights from the database
    cursor.execute('SELECT rowid, weight FROM healthcare')
    weights = cursor.fetchall()

    # Encrypt each weight and update the record
    for rowid, weight in weights:
        encrypted_weight = cipher.encrypt(int(weight * 100))  # Multiply by 100 to handle decimal values
        cursor.execute('UPDATE healthcare SET weight = ? WHERE rowid = ?', (encrypted_weight, rowid))

    # Commit the changes
    conn.commit()
    conn.close()

def range_query_encrypted_weight(min_weight, max_weight):
    """
    Perform a range query on the encrypted 'Weight' attribute.
    """
    encrypted_min = cipher.encrypt(int(min_weight * 100))
    encrypted_max = cipher.encrypt(int(max_weight * 100))

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Query the database for encrypted weights within the encrypted range
    cursor.execute('SELECT * FROM healthcare WHERE weight BETWEEN ? AND ?', (encrypted_min, encrypted_max))
    results = cursor.fetchall()

    conn.close()
    return results

try:
# Encrypt the weights in the database
    encrypt_weights()
    print("Weights encrypted successfully.")
except OutOfRangeError:
    print("Weights already encrypted.")
    pass

# Example usage of the range query
results = range_query_encrypted_weight(50, 60)  # Query for weights between 60 and 70
print(results)
