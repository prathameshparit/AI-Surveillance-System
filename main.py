from flask import Flask, render_template, Response, request
import requests
from camera_fr import VideoCamera as VideoCamera_fr
from camera_wd import VideoCamera as VideoCamera_wd
from camera_pd import VideoCamera as VideoCamera_pd
from camera_tp import VideoCamera as VideoCamera_tp
import webbrowser

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/camera_tampering')
def camera_tampering():
    return render_template('camera_tampering.html')


@app.route('/face_recognition')
def face_recognition():
    return render_template('face_recognition.html')


@app.route('/weapon_detection')
def weapon_detection():
    return render_template('weapon_detection.html')


@app.route('/long_time_pedestrian')
def long_time_pedestrian():
    return render_template('long_time_pedestrian.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed_fr')
def video_feed_fr():
    return Response(gen(VideoCamera_fr()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_wd')
def video_feed_wd():
    return Response(gen(VideoCamera_wd()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_pd')
def video_feed_pd():
    return Response(gen(VideoCamera_pd()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_tp')
def video_feed_tp():
    return Response(gen(VideoCamera_tp()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:2000/')
    app.run(debug=True, port=2000)
