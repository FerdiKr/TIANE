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
