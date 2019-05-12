import random

def isValid(text):
    text = text.lower()
    if 'wie' in text and (('geht' in text and 'dir' in text) or 'läuft' in text):
        return True
    else:
        return False

def handle(text, tiane, profile):
    answers = ['Danke, gut!',
               'Mir gehts gut, {}.'.format(tiane.user),
               'Alles gut, {}.'.format(tiane.user)]
    tiane.say(random.choice(answers))
