import time
import cv2

def start(tiane, profile):
    cam1 = cv2.VideoCapture(0)
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 544)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
    profile['cam1'] = cam1

    cam2 = cv2.VideoCapture(1)
    cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 544)#480
    cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)#360
    profile['cam2'] = cam2



def run(tiane, profile):
    camsandframes = []
    grabbed, frame = profile['cam1'].read()
    if grabbed:
        camsandframes.append((frame, 'Cam1'))
    grabbed, frame = profile['cam2'].read()
    if grabbed:
        camsandframes.append((frame, 'Cam2'))
    if not camsandframes == []:
        tiane.serverconnection.send({'TIANE_room_cam_frames':camsandframes})

def stop(tiane, profile):
    profile['cam1'].release()
    profile['cam2'].release()
