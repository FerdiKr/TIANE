import re

# Beschreibung
'''
Mit diesem Modul kann sich ein User Nachrichten per Telegram zuschicken lassen.
Dazu sagt er beispielsweise "Sende <text> an mein Smartphone".
'''

def isValid(text):
    text = text.lower()
    if 'smartphone' in text and ('nachricht' in text or 'sende' in text):
        return True
    else:
        return False

def handle(text, tiane, local_storage):
    if tiane.telegram_call:
        tiane.say('Du hast geschrieben: ' + text)
    else:
        # Nachricht per Telegram senden
        # Nachricht filtern

        nachricht = ''

        tiane.say(nachricht, output = 'telegram')
