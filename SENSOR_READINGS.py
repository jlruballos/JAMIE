import serial
import time
import datetime
import os
import random
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Establish Serial Connection
arduino_port = 'COM3'  # Replace with the correct port for your Arduino
baud_rate = 115200     # Make sure this matches your Arduino code

ser = serial.Serial(arduino_port, baud_rate, timeout=1)  # 1 second timeout
time.sleep(2)  # Give the connection time to settle

start_marker = '<'
end_marker = '>'
pir_msg = 'P'
pb_msg1 = 'B'
pb_msg2 = 'N'
ult_msg = 'U'

def read_serial_message():
    """Reads and processes a message from the Arduino."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    jokes_folder = os.path.join(script_dir, "jokes")
    joke_files = [f for f in os.listdir(jokes_folder) if f.startswith("Joke_") ]
    
    with open("button_log.txt", "a") as log_file:
        if ser.in_waiting > 0:
            message = ser.readline().decode().strip()
            if message.startswith(start_marker) and message.endswith(end_marker):
                message = message[1:-1]  # Remove the start and end markers
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if message[0] == pir_msg:
                    motion_status = message[1]
                    if motion_status in ['\x01', '1']:
                        print(f"PIR Motion Detected: {motion_status}")
                        log_file.write(f"{timestamp} - PIR Motion detected: {motion_status}\n")
                    if motion_status in ['\x00', '0']:
                        print(f"PIR Motion Ended: {motion_status}")
                        log_file.write(f"{timestamp} - PIR Motion Ended: {motion_status}\n")
                
                elif message[0] == ult_msg:
                    user_status = message[1]
                    if user_status in ['\x00', '0']:
                        print(f"Ultrasonic Detected User Is Gone: {user_status}")
                        log_file.write(f"{timestamp} - Ultrasonic Detected User is Gone: {user_status}\n")
                    elif user_status in ['\x01', '1']:
                        print(f"Ultrasonic Detected User: {user_status}")
                        log_file.write(f"{timestamp} - Ultrasonic Detected User: {user_status}\n") 
                
                elif message[0] == pb_msg1:
                    button_state1 = message[1]
                    if button_state1 in ['\x00', '0']:
                        #button_state1 = int(button_state1)
                        print(f"Push Button 1 State: {button_state1}")
                        log_file.write(f"{timestamp} - Push Button 1 State: {button_state1}\n")
                        if joke_files:
                            joke_to_play = random.choice(joke_files)
                            sound = pygame.mixer.Sound(os.path.join(jokes_folder, joke_to_play))
                            sound.play()
                        else:
                            print(f"Unexpected Push Button 1 State: {button_state1}")
                            log_file.write(f"{timestamp} - Unexpected Push Button 1 State: {button_state1}\n")
                    elif button_state1 in ['\x01', '1']:
                        print(f"Push Button 2 State: {button_state1}")
                        log_file.write(f"{timestamp} - Push Button 2 State: {button_state1}\n")
                        if joke_files:
                            joke_to_play = random.choice(joke_files)
                            sound = pygame.mixer.Sound(os.path.join(jokes_folder, joke_to_play))
                            sound.play()
                    else:
                        print(f"Unexpected Push Button 2 State: {button_state1}")
                        log_file.write(f"{timestamp} - Unexpected Push Button 2 State: {button_state1}\n")
                else:
                    print(f"Unexpected message type: {message[0]}")
                    log_file.write(f"{timestamp} - Unexpected message type: {message[0]}\n")

while True:
    #send_joint_command(joint_ids, joint_angles)
    read_serial_message()
    time.sleep(0.1)