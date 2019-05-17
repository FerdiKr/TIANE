def isValid(text):
    text = text.lower()
    if 'präsentation' in text and 'modus' in text:
        return True

def handle(text, tiane, profile):
    if tiane.core.presentation_mode:
        tiane.core.presentation_mode = False
        tiane.say('In Ordnung, der Präsentationsmodus ist beendet.')
    else:
        tiane.core.presentation_mode = True
        tiane.say('Alles klar, der Präsentationsmodus ist gestartet.')
