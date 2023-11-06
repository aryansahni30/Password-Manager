from cryptography.fernet import Fernet
import os

# Check if the master password file exists
if os.path.exists("master_password.txt"):
    # Load the master password from the file
    with open("master_password.txt", "r") as password_file:
        expected_master_password = password_file.read().strip()
else:
    # Ask the user to set the master password
    expected_master_password = input("Set the master password: ")

    # Save the master password to the file
    with open("master_password.txt", "w") as password_file:
        password_file.write(expected_master_password)

master_password=input("Enter the master password: ")

while(master_password != expected_master_password):
    print("Incorrect password!")
    master_password = input("Enter the master password: ")

def generate_encryption_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_encryption_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
        return key
    else:
        generate_encryption_key()
        print("An encryption key has been generated. Please run the program again.")
        exit()


# Load the encryption key
encryption_key = load_encryption_key()
cipher_suite = Fernet(encryption_key)


def view_passwords():
    with open('passwords.txt', 'r') as file:
        for line in file.readlines():
            data = line.rstrip()
            if "|" in data:
                username, encrypted_password = data.split("|")
                try:
                    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                    print("Username:", username, "| Password:", decrypted_password)
                except Exception as e:
                    print(f"Error decrypting password for '{username}': {str(e)}")


def add_password():
    account_name = input('Account Name: ')
    password = input("Password: ")
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()

    with open('passwords.txt', 'a') as file:
        file.write(account_name + "|" + encrypted_password + "\n")


while True:
    choice = input("Do you want to view existing passwords or add a new one (view, add), or press 'q' to quit? ").lower()

    if choice == "q":
        break
    elif choice == "view":
        view_passwords()
    elif choice == "add":
        add_password()
    else:
        print("Invalid choice. Please try again.")
