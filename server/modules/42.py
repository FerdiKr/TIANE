PRIORITY = -1

def isValid(text):
    text = text.lower()
    if ('was' in text or 'wie' in text) and 'die antwort' in text:
        return True
    else:
        return False

def handle(text, tiane, profile):
    if 'antwort' in text.lower():
        tiane.say('42')
