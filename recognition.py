# It helps in identifying the faces 
import cv2, sys, numpy, os, requests
size = 2
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
confirmations = 0
not_found = 0
name = ''

# Part 1: Create fisherRecognizer 
print('Recognizing Face Please Be in sufficient Lights...') 
data = {'status':'unknown','name' : ''}
requests.post('http://127.0.0.1:2204/postjson',json=data)
# Create a list of images and a list of corresponding names 
(images, lables, names, id) = ([], [], {}, 0) 
for (subdirs, dirs, files) in os.walk(datasets): 
    for subdir in dirs: 
        names[id] = subdir 
        subjectpath = os.path.join(datasets, subdir) 
        for filename in os.listdir(subjectpath): 
            path = subjectpath + '/' + filename 
            lable = id
            images.append(cv2.imread(path, 0)) 
            lables.append(int(lable)) 
        id += 1
(width, height) = (130, 100) 

# Create a Numpy array from the two lists above 
(images, lables) = [numpy.array(lis) for lis in [images, lables]] 

# OpenCV trains a model from the images 
# NOTE FOR OpenCV2: remove '.face' 
model = cv2.face.LBPHFaceRecognizer_create() 
model.train(images, lables) 

# Part 2: Use fisherRecognizer on camera stream 
face_cascade = cv2.CascadeClassifier(haar_file)
#webcam = cv2.VideoCapture(0) 
webcam = cv2.VideoCapture('http://0.0.0.0:2204/video_feed') 
while True: 
    (_, im) = webcam.read() 
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(80, 80),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces: 
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        face = gray[y:y + h, x:x + w] 
        face_resize = cv2.resize(face, (width, height)) 
        # Try to recognize the face 
        prediction = model.predict(face) 
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3) 
        #night 73 , day 60
        if prediction[1]<73:
            name = names[prediction[0]]
            confirmations += 1
            print(prediction[1])
            cv2.putText(im, '% s - %.0f' %
(names[prediction[0]], prediction[1]), (x-10, y-10), 
cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
        else: 
            print(prediction[1])
            not_found += 1
            cv2.putText(im, 'not recognized', 
(x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 

    #cv2.imshow('frame', im) 
    
    key = cv2.waitKey(10) 
    if confirmations>20:
        print("Welcome",name)
        data = {'name' : name}
        requests.post('http://127.0.0.1:2204/postjson',json=data)
        requests.get('http://0.0.0.0:2204/video_feed/stop')
        #requests.get('http://0.0.0.0:2204/door/open')
        #requests.get(f'http://0.0.0.0:2204/verified/{name}')   
        break
    elif not_found>30:
        requests.get('http://0.0.0.0:2204/video_feed/stop')
        print("Not found")
        break

