import serial
import time

# Initialize the serial connection to Arduino
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def parse_data(data):
    """Parse the incoming data from the Arduino and print it."""
    if data:
        if data.startswith('<U'):
            distance = data[2:-1]  # Strip off the markers and the type character
            print(f"Ultrasonic distance: {distance} cm")
        elif data.startswith('<P'):
            motion_status = data[2:-1]  # Strip off the markers and the type character
            if motion_status == '1':
                print("Motion Detected!")
            else:
                print("Motion Ended!")

try:
    # Main loop to continuously read data from the serial port
    while True:
        line = arduino.readline().decode('utf-8').strip()  # Read a line from the serial port
        if line:  # Check if line is not empty
            parse_data(line)
        time.sleep(0.1)  # Slight delay to prevent spamming

except KeyboardInterrupt:
    print("Program interrupted by the user.")

finally:
    arduino.close()  # Ensure serial connection is closed on program termination
