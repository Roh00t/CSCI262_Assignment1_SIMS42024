

# Two-Factor Authentication System

This project implements a simple two-factor authentication (2FA) system using two separate programs:
1. **device.py** - Continuously generates time-based one-time passwords (OTPs) every 15 seconds.
2. **connect.py** - Allows users to register and authenticate using a username, password, and OTP.

The OTP is based on a combination of the username, password, and current time, ensuring synchronization between `device.py` and `connect.py`.

## Files
- **device.py**: Generates a 6-digit OTP every 15 seconds.
- **connect.py**: Provides user registration and authentication functions.
- **Passwords.txt**: Stores registered usernames and passwords in a key:value format (`username:password`).

## Prerequisites
- Python 3.x
- Basic command-line knowledge

## Usage

### 1. Set Up `Passwords.txt`
`Passwords.txt` is automatically created by `connect.py` when a new user registers. The file will store usernames and passwords in plain text in the format `username:password`.

### 2. Running `device.py` for OTP Generation
The `device.py` script generates a new OTP every 15 seconds based on the username and password provided. This OTP can then be used for authentication in `connect.py`.

#### Command:
Existing User

Cammand:
python3 device.py <username> <password>

Example:
python3 device.py Alice mySecurePassword!

Register a New User
To register a new user, run connect.py with the new option. You’ll be prompted to enter a password and confirm a password.

Command:
python3 connect.py <username> new

Example:
python3 connect.py Alice new

