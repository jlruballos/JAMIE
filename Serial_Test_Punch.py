import serial
import time

# Initialize the serial connection to Arduino
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

def send_servo_angles(angles):
    packet = [0x3C]
    # Emote commands
    #packet.append(0x45)
    #packet.append(0x08)
    #Joint commands
    packet.append(0x4A)
    
    #packet = [0xFF]  # Start byte
    packet.extend(min(180, max(0, angle)) for angle in angles)  # Servo angles
    #packet.append(0xFE)  # End byte
    packet.append(0x3E)
    arduino.write(bytearray(packet))
   # print (bytearray(packet))
    time.sleep(0.1)  # Short delay for transmission
    #print("Data Sent!")


#def read_confirmation():
    #if arduino.in_waiting > 0:
 #   return arduino.readline().decode().strip()
    #return None
 
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

def perform_punch():
    # Initial position
    initial_angles = [90,90,90,90,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
    send_servo_angles(initial_angles)
    #time.sleep(0.5)  # Hold initial position
    
    between_punch_angles = [90,135,135,135,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21] #punch
    #send_servo_angles(between_punch_angles)
    #time.sleep(0.5)  # Hold punch position
    
    # Punch movement
    punch_angles = [90,180,180,180,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21] #punch
    #send_servo_angles(punch_angles)
    #time.sleep(0.5)  # Hold punch position

    # Return to initial position
    #send_servo_angles(initial_angles)
    #time.sleep(1)  # Hold initial position

try:
    while True:
        # Automatically assign angles from 1 to 21
        perform_punch()
        #time.sleep(1)  # Short delay for transmission    
        #confirmation = read_confirmation()
        #if confirmation:
         #   print("Arduino says:", confirmation)
        #else:
         #   print("No confirmation from Arduino, checking connection...")
          #  break  # Exit loop if no confirmation is received
        
        time.sleep(1)  # Longer delay to allow for cooling and prevent buffer overflow

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    arduino.close()  # Close the serial connection when done