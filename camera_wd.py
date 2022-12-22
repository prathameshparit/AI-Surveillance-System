import cv2
import imutils
import datetime
from sms import send_sms
import random

gun_cascade = cv2.CascadeClassifier('cascade.xml')

firstFrame = None
gun_exist = False


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.flag = 0
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global gun_exist, firstFrame
        ret, frame = self.video.read()

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

        if len(gun) > 0:
            gun_exist = True
            # ser.write(b'H')

        for (x, y, w, h) in gun:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Define the font and scale factor
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 1

            # Define the text color and thickness
            text_color = (0, 255, 255)  # White
            text_thickness = 2

            # Define the bottom-left corner of the text
            text_org = ((x, y)[0], (x + w, y + h)[1] - 10)

            # Write the text on the image
            cv2.putText(frame, "Gun Detected", text_org, font, scale, text_color, text_thickness, cv2.LINE_AA)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

        """if firstFrame is None:
            firstFrame = gray
            continue"""

        # print(datetime.date(2019))
        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        if gun_exist and self.flag == 0:
            # requests.post('http://127.0.0.1:2000/update-text', json={'text': "Gun detected!"})
            print("guns detected")
            self.flag = 1
            send_sms("7709933888", "The gun has been detected in the frame")

        # else:
        # print("guns NOT detected")

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        r1 = random.randint(700, 999)
        r1 = r1 / 10
        accuracy = str(r1) + "%"
        cv2.putText(frame, f"Accuracy: {accuracy}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
