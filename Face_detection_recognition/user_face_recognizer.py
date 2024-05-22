"""
This code recognizes each registered user and links it with the user's ID. 
This code is runned everytime me start the car or whenever the user indicates it.

python user_face_recognizer.py
"""

import cv2
import numpy as np
import os 

def face_detection(recognizer,faceCascade,font,user_name_directory):
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(1)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:
        ret, img =cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        id = 0
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                
            # If confidence is less them 100 ==> "0" : perfect match 
            if (confidence > 50):
                id = user_name_directory[id]
                confidence = "  {0}%".format(round(100 - confidence))
            elif (confidence < 50):
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(
                        img, 
                        str(id), 
                        (x+5,y-5), 
                        font, 
                        1, 
                        (255,255,255), 
                        2
                    )
            cv2.putText(
                        img, 
                        str(confidence), 
                        (x+5,y+h-5), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                    )  
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

def getUserNames(directory):
    names_dict = {}
    for filename in os.listdir(directory):
        # Split filename into base and extension, then further split base by '.'
        base, _ = os.path.splitext(filename)
        name = base.split('.')[0]
        names_dict[name] = True  # Store the name as a key with a placeholder value
    return list(names_dict.keys())  # Return a list of the unique names

def pipeline():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    directory = "dataset"
    user_name_directory = getUserNames(directory)
    face_detection(recognizer,faceCascade,font,user_name_directory)

if __name__ == '__main__':
    pipeline()
