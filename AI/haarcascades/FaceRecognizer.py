#!C:\Users\SUR\AppData\Local\Programs\Python\Python38-32\python.exe
# -*- coding: utf-8 -*-
print ("Content-Type: text/html")
print()
import cv2
import os
import numpy as np

faceCascade = cv2.CascadeClassifier("E:/JS/CheatingDetection/AsyncFaceRecognition/face_recognition/haarcascades/haarcascade_frontalface_default.XML")


# Call the trained model yml file to recognize faces
recognizer =  cv2.face.LBPHFaceRecognizer_create()
recognizer.read("E:/JS/CheatingDetection/AsyncFaceRecognition/face_recognition/training.yml")

#indiciate id counter
Id_predicted = 0
# Names corresponding to each id
names = []
for users in os.listdir("E:/5th year/School_Project/Cheating_Detection/face_recognition/dataset"):
    names.append(users)

img =  cv2.VideoCapture(0);
font = cv2.FONT_HERSHEY_SIMPLEX
#Setting video width and Height
img.set(3,640)
img.set(4,480)

#Define minimum window size to be recognized as face
minW = 0.1*img.get(3)
minH = 0.1*img.get(4)
print(help(cv2.face))

while True:
    _, Vimage = img.read()
    gray_image = cv2.cvtColor(Vimage, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray_image, scaleFactor=1.03,
        minNeighbors=4, minSize=(int(minW), int(minH))
    )

    # Try to predict the face and get the id
    # Accordingly add the names
    for (x, y, w, h) in faces:
        cv2.rectangle(Vimage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        Id_predicted, confidence = recognizer.predict(gray_image[y:y+h,x:x+w])
        Id_predicted = int(Id_predicted)
        # print(Id_predicted)
        print(names)
        # If confidence is less them 100 ==> "0" : perfect match 
        if (confidence < 80):
            Id_predicted = names[Id_predicted]
            confidence = "{0}%".format(100 - confidence)
        else:
            Id_predicted = "unknown"
            confidence = "{0}%".format(round(100 - confidence))
        
        cv2.putText(
                    Vimage, 
                    str(Id_predicted), 
                    (x+5,y-5), 
                    font, 
                    1, 
                    (255,255,255), 
                    2
                   )
        cv2.putText(
                    Vimage, 
                    str(confidence), 
                    (x+5,y+h-5), 
                    font, 
                    1, 
                    (255,255,0), 
                    1
                   ) 
    cv2.imshow("Recognize", Vimage)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# video_capture.release()
cv2.destroyAllWindows()
