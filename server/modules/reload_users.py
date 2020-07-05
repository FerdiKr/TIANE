import time

SECURE = False

def isValid(text):
    text = text.lower()
    if 'lad' in text and 'nutzer' in text:
        return True
    else:
        return False

def handle(text, tiane, profile):
    tiane.asynchronous_say('Okay, warte einen Moment')
    # Einfach der Nutzer-Klasse den Laden-Befehl geben...
    tiane.Users.load_users()
    time.sleep(1)
    print('--------- FERTIG ---------\n\n')
    tiane.say('Die Nutzer wurden neu geladen.')
