import time

def reload_own(tiane):
    print('\n\n--------- RELOAD ---------')
    # Eigene Module neu laden
    tiane.core.Modules.stop_continuous()
    tiane.core.Modules.load_modules()
    tiane.core.Modules.start_continuous()

def handle(text, tiane, profile):
    tiane.asynchronous_say('Okay, warte einen Moment')
    rooms_counter = 0
    reloaded = False

    if 'server' in text.lower() or tiane.server_name in text.lower():
        reload_own(tiane)
        reloaded = True
    elif not tiane.analysis['room'] == 'None':
        # Befehl nur an einen bestimmten Raum senden
        tiane.rooms[tiane.analysis['room']].Clientconnection.send({'TIANE_reload_modules':True})
        rooms_counter += 1
    else:
        # Befehl an alle Räume senden
        for room in tiane.rooms.values():
            room.Clientconnection.send({'TIANE_reload_modules':True})
            rooms_counter += 1
        reload_own(tiane)
        reloaded = True

    # Warten, bis die Räume fertig sind
    while rooms_counter > 0:
        for room in tiane.rooms.values():
            response = room.Clientconnection.readanddelete('TIANE_confirm_reload_modules')
            if response is not None:
                if response == True:
                    rooms_counter -= 1
    if reloaded:
        time.sleep(1)
        print('--------- FERTIG ---------\n\n')
    tiane.say('Die Module wurden neu geladen.')


def isValid(text):
    text = text.lower()
    if 'lad' in text and 'module' in text:
        return True
    else:
        return False
