"""
This code creates a trainer to identify each registered user and links it with the user's ID. This code is runned everytime me store a new user.

python user_face_trainer.py
"""

import cv2
import numpy as np
from PIL import Image
import os

# function to get the images and label data
def getImagesAndLabels(path,detector):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    names = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # grayscale
        img_numpy = np.array(PIL_img,'uint8')
        name = os.path.split(imagePath)[-1].split(".")[0] 
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            names.append(name)  # Append name
    return faceSamples, names

def pipeline():
    path = "dataset"

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")

    faces, names = getImagesAndLabels(path, detector)
    unique_names = np.unique(names)  # Capture unique names for counting
    recognizer.train(faces, np.array([unique_names.tolist().index(n) for n in names]))
    # Save the model into trainer/trainer.yml
    recognizer.write('trainer/trainer.yml') 
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(unique_names)))
    

if __name__ == '__main__':
    pipeline()