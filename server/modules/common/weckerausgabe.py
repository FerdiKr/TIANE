
def handle(text, tiane, profile):
    user = text.get('Benutzer')
    tx = text.get('Text')
    tiane.say(tx, user=user)

def isValid(text):
    if 'weck' in text:
        return True


    
