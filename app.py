from flask import Flask, Response, render_template, request
from flask import jsonify
import json
import cv2,os

app = Flask(__name__)
video = cv2.VideoCapture(0)
name = ''

@app.route('/')
def index():
    return render_template('index.html', **templateData)

def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/stop')
def video_feed_stop():
    global video
    video.release()
    video = cv2.VideoCapture(0)
    resp = jsonify(success=True)
    return resp

@app.route('/verify')
def verify():
    os.system('python recognition.py')
    #resp = jsonify(success=True)
    return 'True'

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
    global name
    content = request.get_json()
    name = content['name']
    print('Name ->',name)
    return name

@app.route('/getname', methods=['GET'])
def getname():
    if len(name)>0:
        return jsonify(status='verified',name=name)
    else:
        return jsonify(status='error',name='unknown')

'''
@app.route('/door/open')
def door_open():
    global door_status
    door_status = 'Open'
    templateData = { 'door_status' : door_status }
    return render_template('index.html', **templateData )

@app.route('/door/close')
def door_close():
    global door_status
    door_status = 'Closed'
    templateData = { 'door_status' : door_status }
    return render_template('index.html', **templateData )

'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
    