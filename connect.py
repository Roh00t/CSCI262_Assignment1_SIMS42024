
import sys
import os
import re
import time
import random
""" Create/Read in Passwords.txt """
PASSWORD_FILE = "Passwords.txt"

""" This function checks and ensure users conform to the password complexity standards """
def password_complexity_check(password):
    if (len(password) >= 8 and
        re.search(r"[A-Za-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*()_+-=]", password)):
        return True
    return False

def save_user(username, password):
    with open(PASSWORD_FILE, "a") as file:
        file.write(f"{username}:{password}\n")

def load_users():
    users = {}
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            for line in file:
                if ":" in line:
                    uname, pwd = line.strip().split(":", 1)
                    users[uname] = pwd
    return users
""" This Function is to genrate the pin. it also ensures that it is synced with device.py. """
def generate_pin(username, password, interval=15, offset=0):
    current_time = int(time.time() // interval) + offset
    random.seed(f"{username}{password}{current_time}")
    pin = random.randint(100000, 999999)
    return f"{pin:06d}"
""" Checks for existing users, creates new users and enforces password requirements during registration """
def register_user(username):
    users = load_users()
    if username in users:
        print("Error: Username already exists.")
        return

    password = input("Enter a new password: ")
    confirm_password = input("Confirm your password: ")
    
    if password != confirm_password:
        print("Error: Passwords do not match.")
        return
    if not password_complexity_check(password):
        print("Error: Password must be at least 8 characters, include letters, numbers, and symbols.")
        return

    # Save the new user
    save_user(username, password)
    print("User registered successfully.")
    # Registration complete, no authentication attempt here

""" Check for existing users, and authenticates them properly """
def authenticate_user(username, password, pin):
    users = load_users()
    
    if username not in users or users[username] != password:
        print("Error: Invalid username or password.")
        return
    
    # Generate the expected PIN based on the current time window
    expected_pin = generate_pin(username, password)
    # Generate the previous window's PIN for tolerance
    previous_pin = generate_pin(username, password, offset=-1)
    
    if pin == expected_pin or pin == previous_pin:
        print("Authentication successful!")
    else:
        print("Error: Invalid PIN.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 connect.py <username> new OR python3 connect.py <username> <password> <pin>")
        sys.exit(1)

    username = sys.argv[1]

    if sys.argv[2] == "new":
        # Register a new user
        register_user(username)
    elif len(sys.argv) == 4:
        # Authenticate an existing user
        password = sys.argv[2]
        pin = sys.argv[3]
        authenticate_user(username, password, pin)
    else:
        print("Invalid command. Use 'new' for registration or provide <password> <pin> for authentication.")
