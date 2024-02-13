import cv2
import os
# import sqlite3
import numpy as np
from PIL import Image
from Justwalkout.settings import BASE_DIR

detector = cv2.CascadeClassifier(BASE_DIR+'/Face_Detection/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

class EnterFaceRecognition:

    def enterFace(self):
        recognizer.read(BASE_DIR+'/Face_Detection/trainer/trainer.yml')
        cascadePath = BASE_DIR+'/Face_Detection/haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0
        cam = cv2.VideoCapture(0)

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while True:

            ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )

            for(x,y,w,h) in faces:
                startX = x    
                startY = y
                endX = w+x
                endY = h+y
                
                cv2.line(img, (startX, startY), (startX+20, startY), (142,42,27), thickness=2)
                cv2.line(img, (startX, startY), (startX, startY+20), (142,42,27), thickness=2)
                # ending right
                cv2.line(img, (endX, endY), (endX, endY-20), (142,42,27), thickness=2)
                cv2.line(img, (endX, endY), (endX-20, endY), (142,42,27), thickness=2)

                # ending left
                cv2.line(img,(startX+20, endY),(startX, endY), (142,42,27), thickness=2)
                cv2.line(img,(startX, endY-20),(startX, endY), (142,42,27), thickness=2)
                
                # starting left
                cv2.line(img,(endX, startY+20),(endX, startY), (142,42,27), thickness=2)
                cv2.line(img,(endX-20, startY),(endX, startY), (142,42,27), thickness=2)
                
                face_id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less then 100 ==> "0" is perfect match 
                if (confidence < 100):
                    name = 'Detecting...'
                else:
                    name = "Unknown"
                
                # cv2.putText(img, str(name), (10,5), font, 1, (255,255,255), 2)
                # cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('Detect Face',img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            if confidence > 50:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()
        print(face_id)
        return face_id