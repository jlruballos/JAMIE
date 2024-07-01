import serial
import time

# Initialize the serial connection to Arduino
arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)

def send_servo_angles(angles):
    packet = [0xFF]  # Start byte
    packet.extend(min(180, max(0, angle)) for angle in angles)  # Servo angles
    packet.append(0xFE)  # End byte
    arduino.write(bytearray(packet))
    print (bytearray(packet))
    time.sleep(1)  # Short delay for transmission
    print("Data Sent!")


def read_confirmation():
    #if arduino.in_waiting > 0:
    return arduino.readline().decode().strip()
    #return None

try:
    while True:
        # Automatically assign angles from 1 to 21
        angles = [90,180,180,180,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
        print(angles)
        send_servo_angles(angles)
        #time.sleep(1)  # Short delay for transmission    
        confirmation = read_confirmation()
        if confirmation:
            print("Arduino says:", confirmation)

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    arduino.close()  # Close the serial connection when done