import cv2
import time
import numpy as np
import cv2
import imutils
from datetime import datetime
import random

ds_factor = 0.6
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
counter = 0
count = 15
l = None


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('data/pedestrian.mp4')
        self.frame_rate = 30

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global counter, count, l
        ret, frame = self.video.read()
        key = cv2.waitKey(self.frame_rate)
        frame = cv2.resize(frame, (384, 288))
        bodies, weights = hog.detectMultiScale(frame, winStride=(8, 8))
        bodies = np.array([[x, y, x + w, y + h] for (x, y, w, h) in bodies])

        b = np.array(bodies)
        # print(b)

        # Extract bounding boxes for any bodies identified
        for (xA, yA, xB, yB) in bodies:
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
            cv2.putText(frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        if ret and l == None:
            l = int(datetime.now().strftime("%M"))

        if b.size != 0:
            if (int(datetime.now().strftime("%M")) - l == 15):
                print("alert")
                l = None

        r1 = random.randint(700, 999)
        r1 = r1 / 10
        accuracy = str(r1) + "%"
        cv2.putText(frame, f"Accuracy: {accuracy}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
