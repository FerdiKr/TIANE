import numpy as np
import time
import cv2

PRIORITY = 5

def overlayimg(back, fore, x, y, w, h):
    # Load two images
    img1 = np.array(back)
    img2 = np.array(fore)

    try:
        # create new dimensions
        r = float((h)) / img2.shape[1]
        dim = ((w), int(img2.shape[1] * r))
    except IndexError:
        return back

    # Now create a mask of box and create its inverse mask also
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # resize box and masks
    resized_img2 = cv2.resize(img2, dim, interpolation=cv2.INTER_AREA)
    resized_mask = cv2.resize(mask, dim, interpolation=cv2.INTER_AREA)
    resized_mask_inv = cv2.resize(mask_inv, dim, interpolation=cv2.INTER_AREA)

    # Experimentell, behebt aber eventuell einen gravierenden Fehler, der immer wieder zu Abstürzen führte...
    if x < 0 or y < 0 or y + resized_img2.shape[0] > back.shape[0] or x + resized_img2.shape[1] > back.shape[1]:
        return back

    # I want to put box in co-ordinates, So I create a ROI
    rows, cols, channels = resized_img2.shape
    roi = img1[y:y+rows, x:x+cols]

    # Now black-out the area of box in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=resized_mask_inv)

    # Take only region of box from box image.
    img2_fg = cv2.bitwise_and(resized_img2, resized_img2, mask=resized_mask)

    # Put box in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    img1[y:y+rows, x:x+cols] = dst
    return img1

def poi_image(frame, x, y, w, h, sub_type):
    if sub_type == 'AUX_ADMIN':
        sub_type = 'ADMIN'
    assets_path = "resources/POI_Interface/"
    box_path = assets_path + sub_type.lower() + '_focus.tif'
    box = cv2.imread(box_path)
    x -= 30
    y -= 20
    w += 60
    h += 60
    return overlayimg(frame, box, x, y, w, h)

def poi_infobox(frame, x, y, subject_number, subject_name, subject_type):
    if subject_type == 'ADMIN' or subject_type == 'ANALOG' or subject_type == 'AUX_ADMIN':
        id_colour = (58, 238, 247)
    elif subject_type == 'USER':
        id_colour = (243, 124, 13)
    elif subject_type == 'THREAT':
        id_colour = (000, 000, 255)
    else:
        id_colour = (000, 000, 1)
    multiple = 0.60
    infobox_path = "resources/POI_Interface/infobox_slim_short_out.tif"
    infobox = cv2.imread(infobox_path)
    grey_path = "resources/POI_Interface/infobox_slim_in_short.tif"
    grey = cv2.imread(grey_path)

    w = int(400 * multiple)
    h = int(219 * multiple)

    grey_frame = overlayimg(frame, grey, x, y, w, h)
    frame = cv2.addWeighted(grey_frame, 0.75, frame, 0.25, 0)

    id_type = "{} IDENTIFIED".format(subject_type)
    id_alias = "NAME: {}".format(subject_name)
    id_num = "***-***-{}".format(str(subject_number).zfill(3))
    cv2.putText(infobox, id_type, (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, id_colour, 2)
    cv2.putText(infobox, id_alias, (15, 92), cv2.FONT_HERSHEY_SIMPLEX, 1, (12, 12, 12), 2)
    cv2.putText(infobox, "UID:", (15, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(infobox, id_num, (125, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return overlayimg(frame, infobox, x, y, w, h)

def poi_statusbox(frame, x, y, uptime, subjectno):
    multiple = .5
    statusbox_path = "resources/POI_Interface/statusbox_new.tif"
    statusbox = cv2.imread(statusbox_path)

    w = int(580 * multiple)
    h = int(190 * multiple)


    cv2.putText(statusbox, "o", (30, 33), cv2.FONT_HERSHEY_SIMPLEX, .25, (000, 255, 000), 15)
    cv2.putText(statusbox, "PROGRAM: TIANE", (55, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (220, 220, 220), 2)
    cv2.putText(statusbox, "STATUS:", (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (13, 13, 13), 2)
    cv2.putText(statusbox, "ACTIVE", (150, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(statusbox, "UPTIME: {}".format(uptime), (15, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    if not subjectno == '[CAMERAS OFFLINE]':
        cv2.putText(statusbox, "USERS DETECTED: {}".format(subjectno), (15, 168), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        cv2.putText(statusbox, '[CAMERAS OFFLINE]', (15, 168), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return overlayimg(frame, statusbox, x, y, w, h)

def get_time(profile):
    uptimesec = time.time() - profile['TIANE_starttime']
    if uptimesec > 59:
        mins, secs = divmod(round(uptimesec), 60)
        if mins > 59:
            hrs, mins = divmod(mins, 60)
            if hrs >= 24:
                days, hrs = divmod(hrs, 24)
                if days != 1:
                    uptime = "{} DAYS, {} HOURS".format(int(days), int(hrs))
                else:
                    uptime = "1 DAY, {} HOURS".format(int(hrs))
            else:
                if hrs != 1:
                    uptime = "{} HOURS, {} MINUTES".format(int(hrs), int(mins))
                else:
                    uptime = "1 HOUR, {} MINUTES".format(int(mins))
        else:
            if mins != 1:
                uptime = "{} MINUTES, {} SECONDS".format(int(mins), int(secs))
            else:
                uptime = "1 MINUTE, {} SECONDS".format(int(secs))
    else:
        uptime = "{} SECONDS".format(int(uptimesec))
    return uptime

def start(tiane,profile):
    profile['TIANE_POI_INTERFACE_OPTIONS'] = {'boxes':True, 'infoboxes':True, 'statusbox':True}
    profile['TIANE_cams'] = {}
    profile['TIANE_face_boxes_names'] = {}

    profile['TIANE_cam_offline_counter'] = 0
    profile['TIANE_prev_roomnames'] = []
    profile['TIANE_prev_room_camframes'] = {}
    profile['TIANE_room_cam_timeout'] = {}

def run(tiane, profile):
    # Borders für insgesamt: min. 200,200,300,300
    # Borders für jedes Bild: 50,50,50,50
    # Dementsprechend Borders übrig: 150,150,250,250
    cams = []
    roomnames = []
    # Der folgende Abschnitt dient zunächst dazu, die nach Räumen sortierten Kamerabilder in eine zweidimensionale Liste zu verwanden.
    # Außerdem werden die Bilder "zeitlich geglättet": Wenn ein Raum nur ein einziges mal keine Kamerabilder liefert (was aufgrund von
    # Latenzen durchaus vorkommen kann) soll sich noch nicht direkt das Fenster verkleinern, sondern es wird noch für kurze Zeit mit dem
    # letzten Bild gearbeitet, das der Raum geliefert hat.
    for roomname, roomcams in profile['TIANE_cams'].copy().items():
        profile['TIANE_prev_room_camframes'][roomname] = roomcams
        roomnames.append(roomname)
        if not roomname in profile['TIANE_prev_roomnames']:
            profile['TIANE_prev_roomnames'].append(roomname)
        profile['TIANE_room_cam_timeout'][roomname] = 0
        for camname, camframe in roomcams.items():
            try:
                cam = (camframe, camname, profile['TIANE_face_boxes_names'][roomname][camname], roomname)
            except KeyError:
                cam = (camframe, camname, [], roomname)
            cams.append(cam)
        profile['TIANE_face_boxes_names'][roomname] = {}
    for roomname in profile['TIANE_prev_roomnames']:
        if not roomname in roomnames:
            if profile['TIANE_room_cam_timeout'][roomname] <= 25:
                for camname, camframe in profile['TIANE_prev_room_camframes'][roomname].items():
                    cam = (camframe, camname, [], roomname)
                    cams.append(cam)
                profile['TIANE_room_cam_timeout'][roomname] += 1
            else:
                profile['TIANE_prev_roomnames'].remove(roomname)
                del profile['TIANE_prev_room_camframes'][roomname]
    if not cams == []:
        coordinates_combined_bordered = []
        profile['TIANE_cam_offline_counter'] = 0

        if len(cams) == 1:
            # kleinen Rahmen machen
            frame_combined = cv2.copyMakeBorder(cams[0][0], 50,50,
                                                50,50, cv2.BORDER_CONSTANT,
                                                (0,0,0,0))
            # Kameraname dazuschreiben
            cv2.putText(frame_combined, cams[0][3] + ' - ' + cams[0][1], (50,45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (235,235,235), 1)
            # Gesichtskoordinaten umrechnen (für mit großem Rahmen!)
            for top,right,bottom,left,name,proba in cams[0][2]:
                x = left + 300
                y = top + 200
                w = right - left
                h = bottom - top
                coordinates_combined_bordered.append((x,y,w,h,name))

        elif len(cams) == 2:
            frames = []
            i = 0
            for cam in cams:
                # kleinen Rahmen machen
                frames.append(cv2.copyMakeBorder(cam[0], 50,50,
                                                 50,50, cv2.BORDER_CONSTANT,
                                                 (0,0,0,0)))
                # Kameraname dazuschreiben
                cv2.putText(frames[i], cams[i][3] + ' - ' + cams[i][1], (50,45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (235,235,235), 1)
                # Gesichtskoordinaten umrechnen (für kombiniert und mit großem Rahmen!)
                if i == 0:
                    for top,right,bottom,left,name,proba in cams[0][2]:
                        x = left + 300
                        y = top + 200
                        w = right - left
                        h = bottom - top
                        coordinates_combined_bordered.append((x,y,w,h,name))
                else:
                    x = 0
                    for frame in frames[:i]:
                        x += frame.shape[1]
                    for top,right,bottom,left,name,proba in cams[i][2]:
                        x = left + 300 + x
                        y = top + 200
                        w = right - left
                        h = bottom - top
                        coordinates_combined_bordered.append((x,y,w,h,name))
                i += 1
            # Bildhöhen vereinheitlichen
            max_frame_height = max([frame.shape[0] for frame in frames])
            for frame in frames:
                if frame.shape[0] < max_frame_height:
                    frame = cv2.copyMakeBorder(frame, 0, max_frame_height - frame.shape[0],
                                               0,0, cv2.BORDER_CONSTANT,
                                               (0,0,0,0))
            # Bilder kombinieren
            frame_combined = np.hstack((frames[0], frames[1]))

        else:
            top_row = []
            bottom_row = []
            columns, remainder = divmod(len(cams),2)
            # OBERE REIHE
            i = 0
            for cam in cams[:(columns+remainder)]:
                # kleinen Rahmen machen
                top_row.append(cv2.copyMakeBorder(cam[0], 50,50,
                                                  50,50, cv2.BORDER_CONSTANT,
                                                  (0,0,0,0)))
                # Kameraname dazuschreiben
                cv2.putText(top_row[i], cams[i][3] + ' - ' + cams[i][1], (50,45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (235,235,235), 1)
                # Gesichtskoordinaten umrechnen (für kombiniert und mit großem Rahmen!)
                if i == 0:
                    for top,right,bottom,left,name,proba in cams[0][2]:
                        x = left + 300
                        y = top + 200
                        w = right - left
                        h = bottom - top
                        coordinates_combined_bordered.append((x,y,w,h,name))
                else:
                    x = 0
                    for frame in top_row[:i]:
                        x += frame.shape[1]
                    for top,right,bottom,left,name,proba in cams[i][2]:
                        x = left + 300 + x
                        y = top + 200
                        w = right - left
                        h = bottom - top
                        coordinates_combined_bordered.append((x,y,w,h,name))
                i += 1
            # Bildhöhen vereinheitlichen
            max_frame_height = max([frame.shape[0] for frame in top_row])
            for frame in top_row:
                if frame.shape[0] < max_frame_height:
                    frame = cv2.copyMakeBorder(frame, 0, max_frame_height - frame.shape[0],
                                               0,0, cv2.BORDER_CONSTANT,
                                               (0,0,0,0))
            # Bilder kombinieren
            top_frame = top_row[0]
            for frame in top_row[1:]:
                top_frame = np.hstack((top_frame, frame))
            # UNTERE REIHE
            for cam in cams[(columns+remainder):]:
                # kleinen Rahmen machen
                bottom_row.append(cv2.copyMakeBorder(cam[0], 50,50,
                                                     50,50, cv2.BORDER_CONSTANT,
                                                     (0,0,0,0)))
                # Kameraname dazuschreiben
                cv2.putText(bottom_row[-1], cams[i][3] + ' - ' + cams[i][1], (50,45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (235,235,235), 1)
                # Gesichtskoordinaten umrechnen (für kombiniert und mit großem Rahmen!)
                # Dafür brauchen wir diesmal die Höhe der oberen Reihe:
                shapes = [frame.shape for frame in top_row]
                top_row_height = max([shape[0] for shape in shapes])
                if i == len(top_row):
                    for top,right,bottom,left,name,proba in cams[i][2]:
                        x = left + 300
                        y = top + 200 + top_row_height
                        w = right - left
                        h = bottom - top
                        coordinates_combined_bordered.append((x,y,w,h,name))
                else:
                    x = 0
                    for frame in bottom_row[:(i-len(top_row))]:
                        x += frame.shape[1]
                    for top,right,bottom,left,name,proba in cams[i][2]:
                        x = left + 300 + x
                        y = top + 200 + top_row_height
                        w = right - left
                        h = bottom - top
                        coordinates_combined_bordered.append((x,y,w,h,name))
                i += 1
            # Bildhöhen vereinheitlichen
            max_frame_height = max([frame.shape[0] for frame in bottom_row])
            for frame in bottom_row:
                if frame.shape[0] < max_frame_height:
                    frame = cv2.copyMakeBorder(frame, 0, max_frame_height - frame.shape[0],
                                               0,0, cv2.BORDER_CONSTANT,
                                               (0,0,0,0))
            # Bilder kombinieren
            bottom_frame = bottom_row[0]
            for frame in bottom_row[1:]:
                bottom_frame = np.hstack((bottom_frame, frame))

            # Reihenbreiten vereinheitlichen
            max_row_width = max([top_frame.shape[1], bottom_frame.shape[1]])
            rows = [top_frame, bottom_frame]
            for i in range(2):
                if rows[i].shape[1] < max_row_width:
                    rows[i] = cv2.copyMakeBorder(rows[i], 0,0,
                                                 0,max_row_width - rows[i].shape[1], cv2.BORDER_CONSTANT,
                                                 (0,0,0,0))
            # Bilder kombinieren
            frame_combined = np.vstack((rows[0], rows[1]))


        # Egal was wir vorher gemacht haben, der große Rahmen fehlt noch:
        frame_combined_bordered = cv2.copyMakeBorder(frame_combined, 150,150,
                                                     250, 250, cv2.BORDER_CONSTANT,
                                                     (0, 0, 0, 0))

        if profile['TIANE_POI_INTERFACE_OPTIONS']['statusbox'] == True:
            users_detected = []
            for cam in cams:
                for box in cam[2]:
                    if box[4] not in users_detected:
                        users_detected.append(box[4])
            frame_combined_bordered = poi_statusbox(frame_combined_bordered, 60, frame_combined_bordered.shape[0] - 150, get_time(profile), len(users_detected))
        for x,y,w,h,name in coordinates_combined_bordered:
            if name == 'Unknown':
                if profile['TIANE_POI_INTERFACE_OPTIONS']['boxes'] == True:
                    frame_combined_bordered = poi_image(frame_combined_bordered,x,y,w,h,'UNKNOWN')
                if profile['TIANE_POI_INTERFACE_OPTIONS']['infoboxes'] == True:
                    frame_combined_bordered = poi_infobox(frame_combined_bordered, x+w+30, y+int(h*.5-50), 0, 'Unknown','UNKNOWN')
            else:
                if profile['TIANE_POI_INTERFACE_OPTIONS']['boxes'] == True:
                    frame_combined_bordered = poi_image(frame_combined_bordered,x,y,w,h,profile['users'][name]['role'])
                if profile['TIANE_POI_INTERFACE_OPTIONS']['infoboxes'] == True:
                    frame_combined_bordered = poi_infobox(frame_combined_bordered, x+w+30, y+int(h*.5-50), profile['users'][name]['uid'], profile['users'][name]['name'],profile['users'][name]['role'])

        cv2.imshow('TIANE',frame_combined_bordered)

    else:
        if profile['TIANE_cam_offline_counter'] >= 25:
            frame = np.zeros((104,300,3),dtype=np.uint8)
            frame = poi_statusbox(frame, 5, 5, get_time(profile), '[CAMERAS OFFLINE]')
            cv2.imshow('TIANE',frame)
        else:
            profile['TIANE_cam_offline_counter'] += 1

    cv2.waitKey(1) & 0xFF

def stop(tiane, profile):
    cv2.destroyAllWindows()
