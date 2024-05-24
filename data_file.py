import tkinter as tk
from tkinter import ttk
import threading
import cv2
import user_face_recognizer
import user_face_dataset
from queue import Queue
import serial
import csv
import os
import time

# Global variables for the webcam capture, frame queue, and control flags
cam = None
frame_queue = Queue(maxsize=10)
process_frames = True  # Flag to control frame processing
recognition_active = True  # Flag to indicate if recognition is active
recognized_name_queue = Queue()  # Queue to get recognized names

# Setup serial communication with Arduino
def init_serial():
    try:
        #arduino = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM3' with the appropriate serial port
        arduino = serial.Serial('COM3', 9600)
        arduino.dtr = False  # Disable DTR to prevent Arduino reset
        arduino.rts = False  # Disable RTS to prevent Arduino reset
        time.sleep(2)    # Wait for a moment after disabling DTR and RTS
        arduino.reset_input_buffer()  # Flush input buffer after disabling DTR and RTS
        print("Serial port opened successfully.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

arduino = init_serial()

# Function to capture frames from the camera (Producer)
def capture_frames():
    global cam, frame_queue
    while True:
        if not cam.isOpened():
            continue
        ret, frame = cam.read()
        if not ret:
            continue
        if frame_queue.full():
            frame_queue.get()  # Discard the oldest frame to make room for the new frame
        frame_queue.put(frame)  # Put the new frame into the queue

# Function to run the predetermined OpenCV code for the right frame (Consumer)
def run_opencv_right(label):
    user_face_recognizer.pipeline(frame_queue, label, lambda: process_frames, recognized_name_queue)

# Function to capture user data (Consumer)
def run_user_data():
    global process_frames, recognition_active
    process_frames = False
    recognition_active = False
    name = name_entry.get()
    print(f"Running code with name: {name}")
    dataset_thread = threading.Thread(target=user_face_dataset.capture_user_data, args=(frame_queue, name))
    dataset_thread.start()
    dataset_thread.join()  # Wait for the dataset capturing to complete
    process_frames = True
    recognition_active = True

# Function to handle detection button click
def detect():
    if not recognized_name_queue.empty():
        recognized_name = recognized_name_queue.get()
        print(f"Recognized Name: {recognized_name}")
        send_servo_positions_to_arduino(recognized_name, arduino)

def send_servo_positions_to_arduino(user_name, arduino):
    if arduino is None:
        print("Arduino is not connected.")
        return
    csv_file_path = os.path.join(os.path.dirname(__file__), 'servo_positions.csv')
    try:
        with open(csv_file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == user_name:
                    print(f"Data for {user_name}: {row}")
                    servo_positions = f"{user_name},{row[1]},{row[2]},{row[3]},{row[4]}\n"
                    print(f"Sending servo positions to Arduino: {servo_positions}")
                    arduino.write(servo_positions.encode())
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
    finally:
        ser.close()

def UI():
    global name_entry

    # Create the main window
    root = tk.Tk()
    root.title("Sistema Automático de Ajuste de Espejos Retrovisores para Vehículos || Proyecto Integrador Mecatronica")
    root.geometry("1280x720")

    # Create the left frame
    left_frame = ttk.Frame(root, width=int(1280 * 0.2), height=720)
    left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    left_frame.grid_propagate(False)

    # Create the right frame
    right_frame = ttk.Frame(root, width=int(1280 * 0.7), height=720)
    right_frame.grid(row=0, column=2, rowspan=2, sticky="nsew")
    right_frame.grid_propagate(False)

    # Create the right OpenCV display label
    right_label = ttk.Label(right_frame)
    right_label.place(relx=0.5, rely=0.5, anchor="center")

    # Create a label above the text box for entering the name
    name_label = ttk.Label(left_frame, text="Nombre del Usuario Nuevo")
    name_label.pack(padx=20, pady=(280, 10))

    # Create the text box for entering the name
    name_entry = ttk.Entry(left_frame, width=50)
    name_entry.pack(padx=20, pady=10)

    # Create a frame for the buttons
    button_frame = ttk.Frame(left_frame)
    button_frame.pack(pady=10)

    # Create the button to run the predetermined code
    run_button = ttk.Button(button_frame, text="Registrar", command=run_user_data)
    run_button.pack(side=tk.LEFT, padx=5)

    # Start the recognition process by default
    detect_button = ttk.Button(button_frame, text="Detectar", command=detect)
    detect_button.pack(side=tk.LEFT, padx=5)

    # Start the OpenCV thread for the right frame
    threading.Thread(target=run_opencv_right, args=(right_label,), daemon=True).start()

    # Start the Tkinter event loop
    root.mainloop()

def pipeline():
    global cam
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height

    # Start the frame capture thread
    threading.Thread(target=capture_frames, daemon=True).start()

    # Start the UI
    UI()

if __name__ == "__main__":
    pipeline()