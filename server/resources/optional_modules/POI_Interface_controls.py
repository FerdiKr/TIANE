PRIORITY = 1

def handle(text, tiane, profile):
    text = text.lower()
    if ('interface' in text and 'start' in text) or 'status' in text:
        profile['TIANE_POI_INTERFACE_OPTIONS']['statusbox'] = True
    if 'du' in text and 'mich' in text and ('siehst' in text or 'sehen' in text):
        profile['TIANE_POI_INTERFACE_OPTIONS']['boxes'] = True
        tiane.say('Klar doch.')
        profile['TIANE_POI_INTERFACE_OPTIONS']['infoboxes'] = True

def isValid(text):
    text = text.lower()
    if ('interface' in text and 'start' in text) or 'status' in text:
        return True
    if 'du' in text and 'mich' in text and ('siehst' in text or 'sehen' in text):
        return True
    return False
