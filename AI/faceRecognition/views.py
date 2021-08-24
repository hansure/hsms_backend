print ("Content-Type: text/html")
print()
import cv2
from pathlib import Path
import os
from django.http import StreamingHttpResponse
import numpy as np
from imutils import paths
import face_recognition
import argparse
from rest_framework.response import Response
import pickle
import dlib
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import time
from ..camera import livefe
import os
abs_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(abs_dir))
# XMLFILES_FOLDER = os.path.join(PROJECT_ROOT, 'xml_files/')

from rest_framework.decorators import api_view
dirname = os.path.dirname(__file__)
# import dlib
@api_view(['GET','POST'])
# username = request.user.username
def create_dataset(request):
    # Initialize the classifier
    faceCascade = cv2.CascadeClassifier(os.path.join(PROJECT_ROOT, "../haarcascades/haarcascade_frontalface_default.xml"))

    # Start the video camera
    # vc = cv2.VideoCapture(0)
    # Get the userId and userName
    username = request.user.username
    fName = request.user.first_name
    lName = request.user.last_name

    # Initially Count is = 1
    count = 1

    # Function to save the image
    def saveImage(image, fName, lName, username, imgId):
        # Create a folder with the name as userName
        Path(os.path.join(PROJECT_ROOT, f"../dataset/{fName} {lName}").mkdir(parents=True, exist_ok=True))
        # Save the images inside the previously created folder
        cv2.imwrite(os.path.join(PROJECT_ROOT,f"../dataset/{fName} {lName}/{username}.{imgId}.jpg", image))
        print("[INFO] Image {} has been saved in folder : {} {}".format(
            imgId, fName,lName))


    print("[INFO] Video Capture is now starting please stay still")

    while True:
        # Capture the frame/image
        _, img = request.get_json()

        # assign the image to a variable called original_img to later save it
        original_img = img.copy()

        # Get the gray version of our image
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Get the coordinates of the location of the face in the picture
        faces = faceCascade.detectMultiScale(gray_img,
                        scaleFactor=1.05,minNeighbors=6, minSize=(25, 25))

        # Draw a rectangle at the location of the coordinates
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_image = original_img[y:y+h, x:x+w]
            # roi_image = np.zeros((img.shape[0], img.shape[1]))
            # roi_image = cv2.normalize(img, roi_image, 0, 255, cv2.NORM_MINMAX)

        # Show the image
        cv2.imshow("Identified Face", img)

        # Wait for user keypress
        key = cv2.waitKey(1) & 0xFF

        def rotate_bound(image, angle):
            # grab the dimensions of the image and then determine the
            # center
            (h, w) = image.shape[:2]
            (cX, cY) = (w // 2, h // 2)

            # grab the rotation matrix (applying the negative of the
            # angle to rotate clockwise), then grab the sine and cosine
            # (i.e., the rotation components of the matrix)
            M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])

            # compute the new bounding dimensions of the image
            nW = int((h * sin) + (w * cos))
            nH = int((h * cos) + (w * sin))

            # adjust the rotation matrix to take into account translation
            M[0, 2] += (nW / 2) - cX
            M[1, 2] += (nH / 2) - cY

            # perform the actual rotation and return the image
            return cv2.warpAffine(image, M, (nW, nH))
        
        #Create a sharpening kernel
        def sharpen(image):
            sharpening_filter = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
            #Applying kernel(s) to the input image to get the sharpened image
            return cv2.filter2D(image, -1, sharpening_filter)
        # Check if the pressed key is 's'
        if key == ord('s'):
            # If count is between -45 and 45 then save the image
            count = 0
            for deg in range(-45,46,1):
                for i in range(2):
                    alpha = 2
                    beta = 50
                    brightenImage = cv2.addWeighted(roi_image, alpha, np.zeros(roi_image.shape, roi_image.dtype), 0, beta)
                    saveImage(rotate_bound(sharpen(brightenImage),deg), fName, lName, username, count)
                    count += 1
                    saveImage(rotate_bound(brightenImage,deg), fName, lName, username, count)
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
    return Response(request.data)

def train_dataset(request):
    # import the necessary packages
    # construct the argument parser and parse the arguments
    print(dlib.DLIB_USE_CUDA)
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--dataset", required=True,default='dataset',
    #     help="path to input directory of faces + images")
    # ap.add_argument("-e", "--encodings",required=True, default="encodings.pickle",
    #     help="path to serialized db of facial encodings")
    # ap.add_argument("-d", "--detection_method", type=str, default="hog",
    #     help="face detection model to use: either `hog` or `cnn`")
    # args = vars(ap.parse_args())
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(os.path.join(PROJECT_ROOT, "encodings.pickle")))
    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []
    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model="hog")
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)
    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(os.path.join(PROJECT_ROOT, "encodings.pickle"), "wb")
    f.write(pickle.dumps(data))
    f.close()
    #python encode_faces.py --dataset dataset --encodings encodings.pickle
    return Response(request.data)
def face_recognizer(request):
    fps = 0
    frame_counter = 0
    start_time = time.time()

    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(open(os.path.join(PROJECT_ROOT, "faceRecognition/encodings.pickle"), "rb").read())
    # initialize the video stream and pointer to output video file, then
    # allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    writer = None
    time.sleep(6.0)
    # sys.path.append(r'C:/Program Files\ffmpeg-N-102965-gf531a1a4e8-win64-gpl\bin')
    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream
        frame = request.data['question']
        frame = vs.read()
        # print(livefe)
        # convert the input frame from BGR to RGB then resize it to have
        # a width of 400px (to speedup processing)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=400)
        r = frame.shape[1] / float(rgb.shape[1])
        #Calculate the Average FPS
        frame_counter +=1
        fps = (frame_counter /(time.time() - start_time))
        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        # the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb,
            model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
            encoding, tolerance=0.6)
            name = "Unknown"
            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)
                                    
                        # update the list of names
                        names.append(name)
                    # loop over the recognized faces
                    for ((top, right, bottom, left), name) in zip(boxes, names):
                        # rescale the face coordinates
                        top = int(top * r)
                        right = int(right * r)
                        bottom = int(bottom * r)
                        left = int(left * r)
                        # draw the predicted face name on the image
                        cv2.rectangle(frame, (left, top), (right, bottom),
                            (0, 255, 0), 2)
                        cv2.rectangle(frame, (left, bottom -35), (right, bottom),
                            (0, 255, 0), cv2.FILLED)
                        # y = bottom - 15 if bottom - 15 > 15 else bottom + 15
                        cv2.putText(frame, name, (left+10, bottom-10), cv2.FONT_HERSHEY_DUPLEX,
                        1, (255, 255, 255), 1)
                        # Display FPS and size of object
                        cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255),2)
                    # if the video writer is None *AND* we are supposed to write
                    # the output video to disk initialize the writer
                    if writer is None:
                        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                        writer = cv2.VideoWriter(os.path.join(PROJECT_ROOT,"encodings.pickle/output"), fourcc, 20,
                        (frame.shape[1], frame.shape[0]), True)
                    # if the writer is not None, write the frame with recognized
                    # faces to disk
                    if writer is not None:
                        writer.write(frame)
                    # check to see if we are supposed to display the output frame to
                    # the screen
                    # if args["display"] > 0:
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(1) & 0xFF
                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break
        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
        # check to see if the video writer point needs to be released
        if writer is not None:
            writer.release()
        #python recognize_faces.py --encodings encodings.pickle 
        #--output output/webcam_face_recognition_output.avi --display 1
        #python -m ensurepip
        return Response(request.data)
