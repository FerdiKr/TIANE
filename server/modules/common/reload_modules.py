import time

def handle(text, tiane, profile):
    print('\n\n--------- RELOAD ---------')
    tiane.say('Okay, warte einen Moment')
    # Befehl an alle Räume senden
    rooms_counter = 0
    for room in tiane.rooms.values():
        room.Clientconnection.send({'TIANE_reload_modules':True})
        rooms_counter += 1

    # Eigene Module neu laden
    tiane.core.Modules.stop_continuous()
    tiane.core.Modules.load_modules()
    tiane.core.Modules.start_continuous()

    # Warten, bis die Räume fertig sind
    while rooms_counter > 0:
        for room in tiane.rooms.values():
            response = room.Clientconnection.readanddelete('TIANE_confirm_reload_modules')
            if response is not None:
                if response == True:
                    rooms_counter -= 1
    time.sleep(1)
    print('--------- FERTIG ---------\n\n')
    tiane.say('Die Module wurden neu geladen.')


def isValid(text):
    text = text.lower()
    if 'lad' in text and 'module' in text:
        return True
    else:
        return False
