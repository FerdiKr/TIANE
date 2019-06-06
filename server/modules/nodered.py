import requests
import re

# Beschreibung
'''
Mit diesem Modul lassen sich an NodeRed angebundene SmartHome-Geräte steuern.
'''

def isValid(text):
    text = text.lower()
    if 'schalte' in text and ('an' in text or 'ein' in text or 'aus' in text):
        return True
    elif ('wie ist' in text and ('status' in text or 'temperatur' in text)):
        return True
    else:
        return False

def handle(text, tiane, profile):
    text = text.lower()
    length = len(text)
    URL = 'http://<IP>:1880/tiane/'

    if 'schalte' in text and ('an' in text or 'ein' in text or 'aus' in text):
        # Geraet schalten
        sayStatus = False
        URL += 'controllDevice'

        matchDevice = re.search('schalte', text)
        if matchDevice != None:
            startDevice = matchDevice.end() + 1
            matchAction = re.search('(an|ein|aus)', text)
            if matchAction != None:
                endDevice = matchAction.start() - 1
                device = text[startDevice:endDevice]

        if 'an' in text or 'ein' in text:
            action = 'on'
        elif 'aus' in text:
            action = 'off'

        PARAMS = {'device': device, 'action': action}

    elif ('wie ist' in text and ('status' in text or 'temperatur' in text)):
        # Status abfragen
        sayStatus = True
        URL += 'getStatus'

        if 'status von' in text:
            matchDevice = re.search('status von', text)
            if matchDevice != None:
                startDevice = matchDevice.end() + 1
                device = text[startDevice:length]
        elif 'temperatur' in text:
            matchDevice = re.search('temperatur i(m|n)', text)
            if matchDevice != None:
                startDevice = matchDevice.end() + 1
                device = text[startDevice:length]

        PARAMS = {'device': device}

    r = requests.get(url = URL, params = PARAMS)
    result = r.json()

    if result['status'] == 'ERROR':
        tiane.say('Es ist ein Fehler aufgetreten')
    elif result['status'] == 'OK':
        if sayStatus:
            antwort = 'Der Status von ' + device + ' ist ' + result['val']
        else:
            antwort = 'Das Gerät ' + device + ' wurde geschaltet'
        tiane.say(antwort)
