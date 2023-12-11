import sqlite3
import hashlib
from constants import db_file_path

def hash_password(password):
    """
    Hash a password using SHA-256.
    """
    # Create a new sha256 hash object
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

# Example usage:
# register_user('new_user', 'password123', 'H') # For group H
# register_user('another_user', 'password123', 'R') # For group R
def register_user(username, password, user_group):
    """
    Register a new user with a hashed password and user group.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Hash the password
    password_hash = hash_password(password)

    # Insert new user into the users table
    try:
        cursor.execute('INSERT INTO users (username, password_hash, user_group) VALUES (?, ?, ?)', 
                       (username, password_hash, user_group))
        conn.commit()
        result = "User registered successfully."
    except sqlite3.IntegrityError:
        result = "User already exists."
    finally:
        conn.close()
    
    return result



# Example usage: authenticate_user('existing_user', 'password123')
# Replace 'existing_user' and 'password123' with actual username and password for authentication.
def authenticate_user(username, password):
    """
    Authenticate a user by comparing the hashed password.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Hash the provided password
    password_hash = hash_password(password)

    # Retrieve the stored password hash for the given username
    cursor.execute('SELECT password_hash,user_group FROM users WHERE username = ?', (username,))
    stored_password_hash = cursor.fetchone()

    conn.close()

    # Compare the stored hash with the provided hash
    if stored_password_hash and stored_password_hash[0] == password_hash:
        return "User authenticated successfully.",stored_password_hash[1]
    else:
        return "Authentication failed.",None