def isValid(text):
    text = text.lower()
    if (text.startswith('hallo') or text == 'hi' or text == 'hey' or text == '/start') and not 'geht' in text or 'läuft' in text:
        return True

def handle(text, tiane, local_storage):
    tiane.say('Hallo ' + tiane.user)
