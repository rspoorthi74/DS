from auth import *
from access import *
from integrity_protection import *
from data_confidentiality_protection import *
import getpass
import sys  # Import the sys module

# User Registration
register_user_choice = input("Do you want to register? (yes/no): ")
if register_user_choice == "yes":
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    user_group = input("Enter the usergroup: ")
    print(register_user(username, password, user_group))  # Should register successfully

elif register_user_choice == "no":
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
else:
    print("Invalid choice. Please enter 'yes' or 'no'.")
    sys.exit()  # Exit the script if the choice is neither 'yes' nor 'no'

# Authenticate the user
authentication_result, user_group = authenticate_user(username, password)
print(authentication_result)

# If authentication is successful, proceed to access data
if "authenticated" in authentication_result.lower():
    # Display data based on user group
    print(f"Data viewed by user in Group {user_group} ({username}):")
    print(query_data(username))

    # Check if user is in group H before allowing data addition
    if user_group == 'H':
        # Ask the user if they want to add a new data item
        add_data_choice = input("Do you want to add a new data item? (yes/no): ").lower()

        if add_data_choice == 'yes':
            new_data = (
                input("Enter first name: "),
                input("Enter last name: "),
                input("Enter gender: "),
                int(input("Enter age: ")),
                float(input("Enter weight:")),
                float(input("Enter height:")),
                input("Enter health history: ")
            )

            print("Adding data by user in Group H:")
            print(add_data(username, new_data))  # Should be successful for user in Group H
        elif add_data_choice == 'no':
            print("No new data item added.")
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
    else:
        print("Data addition is restricted. Only users from group H can add new data items.")

    # Basic query integrity protection
    print("Basic Query Integrity Protection:")
    # Single data item integrity
    if user_group == 'H':
        new_data_int = (
                input("Enter first name: "),
                input("Enter last name: "),
                input("Enter gender: "),
                int(input("Enter age: ")),
                float(input("Enter weight:")),
                float(input("Enter height:")),
                input("Enter health history: ")
            )
        print("Attempting to add data with integrity hash by user in Group H:")
        print(add_data(username, new_data_int))  # Adding data using a user from group H
        user_to_retrieve = input("Enter the first name of the new data which you have entered in order to retrieve data: ")
        *retrieved_data, retrieved_hash = retrieve_data(user_to_retrieve)
        ## when given an user to retrive vale the excution will take place accordingly as given below 
        ##*retrieved_data, retrieved_hash = retrieve_data('Alice')

        print("Attempting to verify the integrity of the retrieved data:")
        result = verify_data_integrity(retrieved_data, retrieved_hash)
        print("Data integrity verified." if result else "Data integrity compromised.")  
    elif user_group == 'R':
        print("Data addition is restricted. Only users from group H can add new data items or modify")
    else:
         print("Invalid user group.")

    # Basic data confidentiality protection (5 pts)
    print("Basic data confidentiality protection : ")
    # Add new data with encryption and integrity protection
    new_data_conf = (
        input("Enter first name: "),
        input("Enter last name: "),
        input("Enter gender: "),
        int(input("Enter age: ")),
        float(input("Enter weight:")),
        float(input("Enter height:")),
        input("Enter health history: ")
    )

    # Add new data and print result
    result_add = add_data_with_hash_and_encryption(username, new_data_conf)
    print(result_add)

    # Query data with completeness check and decryption
    x = input("Enter first name of the new data to check for confidentiality: ")
    result, message = query_data_with_completeness_check_and_decryption(username, x)
    print("Decrypted result:", result)

    # Print the encrypted result
    encrypted_data = encrypt_data(str(new_data_conf[2]))  # Encrypt gender
    encrypted_data += ", " + encrypt_data(str(new_data_conf[3]))  # Encrypt age
    encrypted_result = new_data_conf[:2] + (encrypted_data,) + new_data_conf[4:]
    print("Encrypted result:", encrypted_result)

else:
    print("Access denied. Authentication failed.")
    sys.exit()  # Exit the script if authentication fails