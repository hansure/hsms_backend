from django.shortcuts import render, redirect
import cv2
from pathlib import Path
import os
# import dlib

from time import time
import pickle

from settings import BASE_DIR
# Create your views here.

# Initialize the classifier
faceCascade = cv2.CascadeClassifier("E:/5th year/School_Project/Cheating_Detection/face_recognition/haarcascades/haarcascade_frontalface_default.xml")


# Start the video camera
vc = cv2.VideoCapture(0)
# Get the userId and userName
userId=input('Enter User id:')
fName = input('Enter your name:')
lName = input("Enter your father's name:")

# Initially Count is = 1
count = 1

# Function to save the image
def saveImage(image, fName, lName, userId, imgId):
    # Create a folder with the name as userName
    Path(f"E:/5th year/School_Project/Cheating_Detection/face_recognition/dataset/{fName} {lName}").mkdir(parents=True, exist_ok=True)
    # Save the images inside the previously created folder
    cv2.imwrite(f"E:/5th year/School_Project/Cheating_Detection/face_recognition/dataset/{fName} {lName}/{userId}.{imgId}.jpg", image)
    print("[INFO] Image {} has been saved in folder : {} {}".format(
        imgId, fName,lName))


print("[INFO] Video Capture is now starting please stay still")

while True:
    # Capture the frame/image
    _, img = vc.read()

    # assign the image to a variable called original_img to later save it
    original_img = img.copy()

    # Get the gray version of our image
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get the coordinates of the location of the face in the picture
    faces = faceCascade.detectMultiScale(gray_img,
                                         scaleFactor=1.05,
                                         minNeighbors=4, 
                                         minSize=(25, 25))

    # Draw a rectangle at the location of the coordinates
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_image = original_img[y:y+h, x:x+w]

    # Show the image
    cv2.imshow("Identified Face", img)

    # Wait for user keypress
    key = cv2.waitKey(1) & 0xFF

    # Check if the pressed key is 'k' or 'q'
    if key == ord('s'):
        # If count is less than 5 then save the image
        for count in range(10):
            saveImage(roi_image, fName, lName, userId, count)
            count += 1
        else:
            break
    # If q is pressed break out of the loop
    elif key == ord('q'):
        break

print("[INFO] Dataset has been created for {} {}".format(fName, lName))
# Stop the video camera
vc.release()
# Close all Windows
cv2.destroyAllWindows()
