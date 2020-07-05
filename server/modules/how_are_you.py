import random

SECURE = True

def isValid(text):
    text = text.lower()
    if 'wie' in text and (('geht' in text and 'dir' in text) or 'läuft' in text or 'geht\'s' in text or 'gehts' in text):
        return True
    else:
        return False

def handle(text, tiane, profile):
    answers = ['Danke, gut!',
               'Mir gehts gut, {}.'.format(tiane.user),
               'Alles gut, {}.'.format(tiane.user)]
    tiane.say(random.choice(answers))
    tiane.say('Und wie geht es dir?')
    reply = tiane.listen()
    reply = reply.lower()
    if 'nicht so' in reply or 'schlecht' in reply or 'müde' in reply or 'mies' in reply or 'suboptimal' in reply:
        tiane.say('Das ist schade. Mach doch etwas, was du gerne tust, vielleicht geht es dir dann besser.')
    elif 'gut' in reply or 'besser' in reply or 'bestens' in reply or 'super' in reply or 'wundervoll' in reply or 'glücklich' in reply or 'froh' in reply:
        tiane.say('Das freut mich!')
    else:
        tiane.say('Ich fürchte, ich konnte dich nicht verstehen.')
