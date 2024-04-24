"""
This code creates new users and stores their face for further use
"""

import cv2
import os
import argparse
import sys

def user_input():
    parser = argparse.ArgumentParser(prog='User Face Dataset', 
                                    description='Capture and store new user face ID information', 
                                    epilog='JCCV - 2024')
    parser.add_argument('-ID',
                        '--input_user_ID',
                        type=str,
                        required=True,
                        help="Please type the name of the new user")
    
    args = parser.parse_args()
    return args

def face_detection(user_ID):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print("\n Initializing face capture. Look the camera and wait ...")

    # Initialize individual sampling face count
    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(user_ID) + '.' +  
                        str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30: # Take 30 face sample and stop video
            break
    
    cam.release()
    cv2.destroyAllWindows()

def pipeline():
    user_data = user_input()
    user_ID = user_data.input_user_ID
    face_detection(user_ID)

if __name__ == '__main__':
    pipeline()