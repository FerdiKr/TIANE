#!/usr/bin/env python3

import urllib.request

SECURE = True

def isValid(text):
    text = text.lower()
    if 'qr' in text:
        return True
    else:
        return False

def handle(text, tiane, profile):

    tiane.say('Was möchtest du in den qr-code schreiben?')

    # Frage den Nutzer nach Inhalt
    antwort = tiane.listen()
    if antwort == 'TIMEOUT_OR_INVALID':
        tiane.say('Ich konnte dich leider nicht verstehen')
    else:
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + urllib.parse.quote(antwort)
        tiane.say(url)
