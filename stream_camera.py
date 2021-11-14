from flask import Flask,render_template,Response

from nanny.camera import Camera
from nanny.logger import Logger
from nanny.shared import CAMERA_STREAM_PORT

app = Flask('camera-video-stream')

def frames_generator(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    logger = Logger('werkzeug') # Use this logger to see output
    return Response(frames_generator(Camera(logger)),
                    mimetype='multipart/x-mixed-replace; boundary=frame'
                   )

if __name__=="__main__":
    app.run(host='0.0.0.0', port=CAMERA_STREAM_PORT, debug=False, threaded=True)
