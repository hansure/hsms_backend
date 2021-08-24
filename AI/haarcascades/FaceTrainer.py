#!C:\Users\SUR\AppData\Local\Programs\Python\Python38-32\python.exe
# -*- coding: utf-8 -*-
print ("Content-Type: text/html")
print()
import os
import cv2
import numpy as np
import cgi
# Command: pip install pillow
from PIL import Image

#Initialize names and path to empty list 
names = []
path = []

# Get the names of all the users
for users in os.listdir("E:/5th year/School_Project/Cheating_Detection/face_recognition/dataset"):
    names.append(users)

# Get the path to all the images
for name in names:
    for image in os.listdir("E:/5th year/School_Project/Cheating_Detection/face_recognition/dataset/{}".format(name)):
        path_string = os.path.join("E:/5th year/School_Project/Cheating_Detection/face_recognition/dataset/{}".format(name), image)
        path.append(path_string)


faces = []
ids = []

# For each image create a numpy array and add it to faces list
for img_path in path:
    image = Image.open(img_path).convert("L")

    imgNp = np.array(image, "uint8")

    id = int(float(os.path.split(img_path)[-1].split('.')[0]))

    faces.append(imgNp)
    ids.append(id)

# Convert the ids to numpy array and add it to ids list
ids = np.array(ids)

print("[INFO] Created faces and names Numpy Arrays")
print("[INFO] Initializing the Classifier")

# Make sure contrib is installed
# The command is pip install opencv-contrib-python

# Call the recognizer
trainer = cv2.face.LBPHFaceRecognizer_create()
# Give the faces and ids numpy arrays
trainer.train(faces, ids)
# Write the generated model to a yml file
trainer.write("E:/5th year/School_Project/Cheating_Detection/face_recognition/training.yml")

print("[INFO] Training Done")