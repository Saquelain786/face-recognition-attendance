import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import csv

  
    
path = 'ImageAttendance'

images=[]
classNames=[]
myList = os.listdir(path)
print(myList)

for cl in myList:
    currImg = cv2.imread(f'{path}/{cl}')
    images.append(currImg)
    classNames.append(os.path.splitext(cl)[0])
    
for names in classNames:
    print(names)


def findEncoding(images):
    encodeList=[]
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodeCurr = face_recognition.face_encodings(image)[0]
        encodeList.append(encodeCurr)
    
    return encodeList



def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')

# =============================================================================
# markAttendance('Elon');
# =============================================================================

encodeListKnown = findEncoding(images)
print('encoding complete !!!')


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS =  cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    faceCurrFrame = face_recognition.face_locations(imgS)
    encodesCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)
    
    for encodeFace, faceLoc in zip(encodesCurrFrame, faceCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace);
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
        
        
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            markAttendance(name)
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
            
            
            
            
    cv2.imshow('webcam', img)
    cv2.waitKey(1)




cv2.waitKey(0)
