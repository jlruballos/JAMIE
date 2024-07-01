import serial
import time
import math

# Initialize the serial connection to Arduino
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

def send_servo_angles(angles):
    packet = [0xFF]  # Start byte
    packet.extend(min(180, max(0, int(angle))) for angle in angles)  # Ensure angles are within 0-180 and convert to int
    packet.append(0xFE)  # End byte
    arduino.write(bytearray(packet))
    print(bytearray(packet))
    time.sleep(1)  # Short delay for transmission
    print("Data Sent!")


def read_confirmation():
    # if arduino.in_waiting > 0:
    return arduino.readline().decode().strip()
    # return None

try:
    step = 0  # Initialize step for sine wave calculation
    while True:
        # Generate wave pattern with step to create a moving wave
        angles = [(math.sin(math.radians(angle_step + step * 10)) * 90 + 90) for angle_step in range(0, 361, 17)]
        #print(angles)
        send_servo_angles(angles)
        confirmation = read_confirmation()
        if confirmation:
            print("Arduino says:", confirmation)
        step += 1  # Increment step for the next wave pattern

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    arduino.close()  # Close the serial connection when done
