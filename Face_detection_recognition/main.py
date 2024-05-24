import tkinter as tk
from tkinter import ttk
import threading
import cv2
import user_face_recognizer
import user_face_dataset
from queue import Queue

# Global variables for the webcam capture, frame queue, and control flags
cam = None
frame_queue = Queue(maxsize=10)
process_frames = True  # Flag to control frame processing
recognition_active = True  # Flag to indicate if recognition is active

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
    user_face_recognizer.pipeline(frame_queue, label, lambda: process_frames)

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
    second_button = ttk.Button(button_frame, text="Detectar", command=lambda: run_opencv_right(right_label))
    second_button.pack(side=tk.LEFT, padx=5)

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