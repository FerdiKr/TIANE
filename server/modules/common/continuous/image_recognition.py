import face_recognition
import imutils
import pickle
import time
import cv2

PRIORITY = 1

def start(tiane, profile):
    profile['TIANE_face_recognition_data'] = pickle.loads(open('encodings.pickle', 'rb').read())
    profile['TIANE_face_boxes_names'] = {}
    profile['TIANE_cam_recognized_users'] = {}

def run(tiane, profile):
    for room in tiane.rooms.copy().values():
        profile['TIANE_face_boxes_names'][room.name] = {}
        profile['TIANE_cam_recognized_users'][room.name] = []
        cams = room.Clientconnection.readanddelete('TIANE_room_cam_frames')
        # cams: [(frame, name), (frame, name),...]
        if cams is not None:
            for cam in cams:
                frame, camname = cam
                profile['TIANE_face_boxes_names'][room.name][camname] = [frame, camname,[]]
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = imutils.resize(frame, width=750)
                r = frame.shape[1] / float(rgb.shape[1])

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input frame, then compute
                # the facial embeddings for each face
                boxes = face_recognition.face_locations(rgb, model='cnn')
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []

                # loop over the facial embeddings
                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(profile['TIANE_face_recognition_data']["encodings"],
                        encoding)
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
                            name = profile['TIANE_face_recognition_data']["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)

                    # update the list of names
                    names.append(name)

                    '''# Diese Nutzer-Raum-Zuweisung bedarf dringend einer Überarbeitung...
                    if not name == 'Unknown':
                        profile['users'][name]['room'] = room.name
                        for raum in profile['rooms'].values():
                            try:
                                for user in raum['users']:
                                    if user == name:
                                        raum['users'].remove(name)
                            except KeyError:
                                continue
                        try:
                            profile['rooms'][room.name]['users'].append(name)
                        except KeyError:
                            profile['rooms'][room.name]['users'] = [name]'''

                    
                    #try:
                    profile['TIANE_cam_recognized_users'][room.name].append(name)
                    #except KeyError:
                    #    profile['TIANE_cam_recognized_users'][room.name] = [name]

                    # loop over the recognized faces
                    for ((top, right, bottom, left), name) in zip(boxes, names):
                        # rescale the face coordinates
                        top = int(top * r)
                        right = int(right * r)
                        bottom = int(bottom * r)
                        left = int(left * r)
                        if not (top, right, bottom, left, name) in profile['TIANE_face_boxes_names'][room.name][camname][2]:
                            profile['TIANE_face_boxes_names'][room.name][camname][2].append((top,right,bottom,left,name))

                        '''# draw the predicted face name on the image
                        cv2.rectangle(frame, (left, top), (right, bottom),
                            (0, 255, 0), 2)
                        y = top - 15 if top - 15 > 15 else top + 15
                        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)'''
                #cv2.imshow(camname, frame)
    #key = cv2.waitKey(1) & 0xFF
