# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from imutils import paths
import face_recognition
import argparse
import pickle
import imutils
import cv2
import os

def list_user_image_paths(user, local_storage):
    # Gibt eine Liste mit den vollen Pfaden zu allen Bildern eines Nutzers aus
    image_folder_path = local_storage['users'][user]['path'] + '/pictures'
    image_paths = []
    for image_path in os.listdir(image_folder_path):
        if (image_path.lower().endswith('.png')
            or image_path.lower().endswith('.jpg')
            or image_path.lower().endswith('.jpeg')):
            image_paths.append(os.path.join(image_folder_path, image_path))
    return image_paths

def handle(text, tiane, local_storage):
    print('\n\n--------- RETRAIN --------')
    tiane.say('Okay, warte einen Moment. Ich trainiere die Gesichtserkennung neu.')
    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the users
    for user in local_storage['users'].copy().keys():
        print('[INFO] Lade Bilder von {}'.format(user))
        imagePaths = list_user_image_paths(user, local_storage)
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] Bild {}/{} wird verarbeitet".format(i + 1,
                  len(imagePaths)))

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            image = imutils.resize(image, width=800)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model='cnn')

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(user)

    # dump the facial encodings + names to disk
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(local_storage['TIANE_PATH'] + '/resources/face_encodings.pickle', "wb")
    f.write(pickle.dumps(data))
    f.close()

    # encode the labels
    le = LabelEncoder()
    labels = le.fit_transform(data["names"])

    # train the face recognition model
    print("[INFO] Neural Network wird trainiert...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(data["encodings"], labels)

    # write the actual face recognition model to disk
    print("[INFO] Daten werden gespeichert...")
    f = open(local_storage['TIANE_PATH'] + '/resources/face_recognizer', "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    f = open(local_storage['TIANE_PATH'] + '/resources/face_label_encoder.pickle', "wb")
    f.write(pickle.dumps(le))
    f.close()


    print('--------- FERTIG ---------\n\n')
    tiane.say('Die Gesichtserkennung wurde neu trainiert.')

def isValid(text):
    text = text.lower()
    if ('lad' in text or 'train' in text) and 'gesicht' in text:
        return True
    else:
        return False
