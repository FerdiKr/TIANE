def isValid(text):
    text = text.lower()
    if 'hallo' in text or text == 'hi':
        return True

def handle(text, tiane, local_storage):
    tiane.say('Hallo ' + tiane.user)
