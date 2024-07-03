import cv2
import csv
import os
import time
import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port.device}: {port.description}")

def capture_user_data(frame_queue, user_ID, serial_manager):
    path = "dataset"
    face_detection(frame_queue, user_ID, path)
    read_serial_and_store(user_ID, serial_manager)

def face_detection(frame_queue, user_ID, path):
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print("\n Initializing face capture. Look the camera and wait ...")

    count = 0
    while True:
        if frame_queue.empty():
            continue
        frame = frame_queue.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite(path + "\\" + str(user_ID) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
            cv2.imshow('image', frame)
        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30:  # Take 30 face sample and stop video
            break

    cv2.destroyAllWindows()

def read_serial_and_store(user_ID, serial_manager):
    def read_from_serial():
        # List available ports
        list_serial_ports()
        # Read a single line from the serial port
        while True:
            if serial_manager.serial_port.in_waiting > 0:
                line = serial_manager.serial_port.readline()
                try:
                    decoded_line = line.decode('utf-8').strip()
                    print(f"Raw data received: {decoded_line}")  # Debugging: print raw data
                    servo_positions = decoded_line.split(',')

                    # Ensure we have exactly four positions
                    if len(servo_positions) == 4:
                        csv_file = 'servo_positions.csv'
                        # Open the CSV file in append mode
                        with open(csv_file, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            # Write the username and servo positions to the CSV file
                            writer.writerow([user_ID] + servo_positions)
                        print(f"Stored positions for {user_ID}: {servo_positions}")
                        break  # Exit the loop after storing one valid line
                    else:
                        print("Error: Invalid data received from serial port")
                except UnicodeDecodeError as e:
                    print(f"Error decoding line: {line}, error: {e}")

    serial_manager.execute_with_lock(read_from_serial)

if __name__ == '__main__':
    import argparse
    from queue import Queue
    from main import serial_manager  # Import serial_manager from main

    parser = argparse.ArgumentParser(description='Capture user face data and read serial information')
    parser.add_argument('user_ID', type=str, help='User ID')
    args = parser.parse_args()

    # Dummy frame queue for testing (replace with actual queue in production)
    frame_queue = Queue(maxsize=10)
    capture_user_data(frame_queue, args.user_ID, serial_manager)
