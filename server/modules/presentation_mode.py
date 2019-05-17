def isValid(text):
    text = text.lower()
    if 'präsentation' in text and 'modus' in text:
        return True

def handle(text, tiane, profile):
    tiane.core.presentation_mode = not tiane.core.presentation_mode
    if tiane.core.presentation_mode:
        tiane.say('Alles klar, der Präsentationsmodus ist gestartet.')
    else:
        tiane.say('In Ordnung, der Präsentationsmodus ist beendet.')
