import cv2
import numpy as np
import os
from PIL import Image, ImageTk

def face_detection(frame_queue, recognizer, faceCascade, font, user_name_directory, label, should_process):
    while True:
        if frame_queue.empty():
            continue
        frame = frame_queue.get()
        if not should_process():
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=frame)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            continue  # Skip processing if should_process is False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(0.1 * frame.shape[1]), int(0.1 * frame.shape[0])),
        )
        id = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence > 40:
                id = user_name_directory[id]
                confidence = "  {0}%".format(round(100 - confidence))
            elif confidence < 40:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(
                frame,
                str(id),
                (x + 5, y - 5),
                font,
                1,
                (255, 255, 255),
                2
            )
            cv2.putText(
                frame,
                str(confidence),
                (x + 5, y + h - 5),
                font,
                1,
                (255, 255, 0),
                1
            )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=frame)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        if cv2.waitKey(10) & 0xFF == 27:  # Press 'ESC' for exiting video
            break

    print("\n [INFO] Exiting Program and cleanup stuff")
    cv2.destroyAllWindows()

def getUserNames(directory):
    names_dict = {}
    for filename in os.listdir(directory):
        base, _ = os.path.splitext(filename)
        name = base.split('.')[0]
        names_dict[name] = True
    return list(names_dict.keys())

def pipeline(frame_queue, label, should_process):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    directory = "dataset"
    user_name_directory = getUserNames(directory)
    face_detection(frame_queue, recognizer, faceCascade, font, user_name_directory, label, should_process)