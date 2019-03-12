PRIORITY = 7


# Dieses Modul empfängt alle Kamerabilder von allen Räumen und speichert sie im
# Local_storage unter folgendem Schema:
#Local_storage = {'TIANE_cams': {roomname1: {camname1: frame1, camname2: frame2}, roomname2:{camname3: frame3}}}

def start(tiane, profile):
    profile['TIANE_cams'] = {}

def run(tiane, profile):
    profile['TIANE_cams'] = {}
    for room in tiane.rooms.copy().values():
        cams = room.Clientconnection.readanddelete('TIANE_room_cam_frames')
        # cams: [(frame, name), (frame, name),...]
        if cams is not None:
            profile['TIANE_cams'][room.name] = {}
            for frame, camname in cams:
                profile['TIANE_cams'][room.name][camname] = frame
