from flask import Flask,render_template,Response

from nanny.camera_alternative import Camera
from nanny.logger import Logger

app = Flask(__name__)

def frames_generator(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    logger = Logger('werkzeug') # Use this logger to see output
    return Response(frames_generator(Camera(logger)),
                    mimetype='multipart/x-mixed-replace; boundary=frame'
                   )

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True)
