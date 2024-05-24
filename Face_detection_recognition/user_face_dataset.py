import cv2

def capture_user_data(frame_queue, user_ID):
    path = "dataset"
    face_detection(frame_queue, user_ID, path)

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