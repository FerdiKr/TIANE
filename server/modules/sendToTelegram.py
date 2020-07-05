import re

SECURE = False # Nicht SECURE, da Nachrichten an Telegram bei einer Verbindung per WebSocket
               # nicht speziell behandelt werden. Deshalb macht das keinen Sinn.

# Beschreibung
'''
Mit diesem Modul kann man sich Nachrichten per Telegram zuschicken lassen.
Dazu sagt man "Sende <text> an mein Smartphone" oder "Smartphone Nachricht <text>".
'''

def isValid(text):
    text = text.lower()
    if 'smartphone' in text and ('nachricht' in text or 'sende' in text):
        return True
    else:
        return False

def handle(text, tiane, local_storage):
    text = text.lower()
    length = len(text)

    match = re.search('^smartphone nachricht', text)
    if match != None:
        end = match.end() + 1
        nachricht = text[end:length]

    else:
        liste = re.split('\s', text)
        elements = len(liste)
        if liste[0] == 'sende' and liste[elements-1] == 'smartphone':
            nachricht = ''
            for i in range(1,elements):
                if liste[i] == 'an' and liste[i+1] == 'mein':
                    break
                else:
                    nachricht += liste[i]
                    nachricht += ' '

    if nachricht != '':
        if tiane.telegram_call:
            tiane.say('Du hast folgende Nachricht an dich selbst geschrieben:')
        else:
            tiane.say("Ok, ich sende " + nachricht + " an dein Smartphone")
            tiane.say("Nachricht an dich:", output='telegram')
        tiane.say(nachricht, output='telegram')
    else:
        tiane.say("Ich konnte deine Nachricht nicht heraus filtern")
