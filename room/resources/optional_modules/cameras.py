from imutils.video import VideoStream, WebcamVideoStream
import json
import cv2

def start(tiane, profile):
    profile['TIANE_CAMS'] = {}
    with open(tiane.path + '/TIANE_config.json', 'r') as config_file:
        config_data = json.load(config_file)
    for camname, camsettings in config_data['Cameras'].items():
        if camsettings['PiCam']:
            profile['TIANE_CAMS'][camname] = (VideoStream(usePiCamera=True).start(), True)
        else:
            '''cam = WebcamVideoStream(src=camsettings['src'])
            try:
                cam.stream.set(cv2.CAP_PROP_FRAME_WIDTH, camsettings['width'])
                cam.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, camsettings['height'])
            except KeyError:
                pass
            profile['TIANE_CAMS'][camname] = (cam.start(), False)'''
            cam = cv2.VideoCapture(camsettings['src'])
            try:
                cam.set(cv2.CAP_PROP_FRAME_WIDTH, camsettings['width'])
            except KeyError:
                pass
            try:
                cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camsettings['height'])
            except KeyError:
                pass
            profile['TIANE_CAMS'][camname] = (cam, False)

def run(tiane, profile):
    camsandframes = []
    for camname, cam in profile['TIANE_CAMS'].items():
        if cam[1]:
            # Ist eine PiCam, die sind einfacher zu handlen
            camsandframes.append((cam[0].read(), camname))
        else:
            # Webcams bekommen optimalerweise einen zusätzlichen Schritt
            '''if cam[0].grabbed:
                camsandframes.append((cam[0].frame, camname))'''
            grabbed, frame = cam[0].read()
            if grabbed:
                camsandframes.append((frame, camname))
    if not camsandframes == []:
        tiane.serverconnection.send({'TIANE_room_cam_frames':camsandframes})

def stop(tiane, profile):
    for cam in profile['TIANE_CAMS'].values():
        if cam[1]:
            cam[0].stop()
        else:
            cam[0].release()
