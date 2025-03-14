from flask import Flask, render_template, Response, request, jsonify
import cv2
import subprocess

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    camera.release()  # Release camera when done

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register', methods=['POST'])
def register():
    subprocess.run(["python", "Readface.py"])
    subprocess.run(["python", "Train.py"])
    return jsonify({"message": "Face registered and model trained successfully"})

@app.route('/login', methods=['POST'])
def login():
    subprocess.run(["python", "Detectface.py"])
    return jsonify({"message": "Login process started"})

if __name__ == '__main__':
    app.run(debug=True)
