
import time
import random
import sys
"""Generate a 6-digit PIN based on the username, password, and the current time window."""

def generate_pin(username, password, interval=15):
    current_time = int(time.time() // interval)  # Current time window based on the interval
    random.seed(f"{username}{password}{current_time}")  # Seed random generator with user and time data
    pin = random.randint(100000, 999999)  # Generate a 6-digit random PIN
    return f"{pin:06d}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 device.py <username> <password>")
        sys.exit(1)
    
    username, password = sys.argv[1], sys.argv[2]

    print("Device is generating PINs. Press Ctrl+C to stop.")
    try:
        while True:
            pin = generate_pin(username, password)
            print(f"Device: {pin}")
            time.sleep(15)  # Wait 15 seconds before generating the next PIN
    except KeyboardInterrupt:
        print("\nDevice stopped.")
