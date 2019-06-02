import random

# Beschreibung
'''
In diesem Spiel geht es darum, eine Zufallszahl in möglichst wenigen Schritten zu erraten.
'''

def isValid(text):
    text = text.lower()
    if 'spiel' in text and ('zahl' in text or 'erraten' in text):
        return True
    else:
        return False
