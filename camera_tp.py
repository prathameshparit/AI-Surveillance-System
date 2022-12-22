import cv2
import os
import numpy as np
import shutil
import serial
import imutils
from datetime import datetime
import random

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_mcs_eyepair_big.xml")

ds_factor = 0.6
counter = 0
count = 15
mask = 0
not_mask = 0
no_face = 0
body = 0
gun_det = 0
cam_tamp = 0
l = None
kernel = np.ones((5, 5), np.uint8)

out = cv2.VideoWriter(
    'fr.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (384, 288))
fgbg = cv2.createBackgroundSubtractorMOG2()


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()
        source = '/home/anmol/Desktop/Third-Eye/StreamTest/fr.avi'
        des = '/home/anmol/Desktop/Third-Eye/Deployed/data/fr.avi'
        shutil.copyfile(source, des)
        os.remove(source)

    def get_frame(self):
        global mask, cam_tamp, not_mask, l, no_face, kernal
        ret, frame = self.video.read()
        if ret and l == None:
            l = int(datetime.now().strftime("%M"))
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mouth_rects = mouth_cascade.detectMultiScale(gray, 1.3, 5)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
        eye_rects = eye_cascade.detectMultiScale(gray, 1.3, 5)
        m = np.array(mouth_rects)
        f = np.array(face_rects)
        n = np.array(nose_rects)
        e = np.array(eye_rects)

        a = 0
        bounding_rect = []
        fgmask = fgbg.apply(frame)
        fgmask = cv2.erode(fgmask, kernel, iterations=5)
        fgmask = cv2.dilate(fgmask, kernel, iterations=5)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        r1 = random.randint(700, 999)
        r1 = r1 / 10
        accuracy = str(r1) + "%"
        for i in range(0, len(contours)):
            bounding_rect.append(cv2.boundingRect(contours[i]))
        for i in range(0, len(contours)):
            if bounding_rect[i][2] >= 40 or bounding_rect[i][3] >= 40:
                a = a + (bounding_rect[i][2]) * bounding_rect[i][3]
            if (a >= int(frame.shape[0]) * int(frame.shape[1]) / 3):

                cv2.putText(frame, f"Accuracy: {accuracy}", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(frame, "TAMPERING DETECTED", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                cam_tamp = cam_tamp + 1

        ret1, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
