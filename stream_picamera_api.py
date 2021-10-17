from flask import Flask,render_template,Response
from nanny.camera import Camera

app = Flask(__name__)

def generate_frames(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame'
                   )

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True)
