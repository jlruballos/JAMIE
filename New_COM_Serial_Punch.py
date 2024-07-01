import serial
import time

# Initialize the serial connection to Arduino
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)  # Adjust port if needed

# Function to send servo angles in the correct format
def send_servo_angles(angles):
    packet = f"<J{' '.join(map(str, angles))}>"
    print("Sending:", packet)  # Debug print
    arduino.write(packet.encode())
    time.sleep(0.1)  # Increased delay

# Function to send emote commands
def send_emote(emote_number):
    packet = f"<E{emote_number}>"
    arduino.write(packet.encode())
    time.sleep(0.01)

# Function to read a confirmation message from Arduino (if needed)
def read_confirmation(timeout=5):
    print("Waiting for confirmation from Arduino...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"Arduino says: {response}")
            return response
    print("No confirmation received within timeout period.")
    return None

# Function to perform a punch sequence (example)
def perform_punch():
    initial_angles = [90, 90, 90, 90, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    between_punch_angles = [90, 135, 135, 135, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    punch_angles = [90, 180, 180, 180, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

    for angles in [initial_angles, between_punch_angles, punch_angles, initial_angles]:
        send_servo_angles(angles)
        time.sleep(0.5)  # Adjust hold time as needed

# Main loop
try:
    while True:
        perform_punch()  # Example function
        # Add other actions here (e.g., sending different angles or emotes)
        time.sleep(1)   # Delay between actions 

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    arduino.close()  # Close the serial connection
