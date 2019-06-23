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

def handle(text, tiane, local_storage):
    if tiane.telegram_call:
        zahl = random.randrange(1000)
        tipp = 0
        i = 0

        tiane.say('Ok, lasse uns spielen. Versuche die Zufallszahl in möglichst wenigen Schritten zu erraten')

        while tipp != zahl:
            tiane.say('Dein Tipp:')
            tipp = int(tiane.listen())

            if zahl < tipp:
                tiane.say("Die gesuchte Zahl ist kleiner als " + str(tipp))
            if zahl > tipp:
                tiane.say("Die gesuchte Zahl ist größer als " + str(tipp))
            i += 1

        tiane.say("Du hast die Zahl beim " + str(i) + ". Tipp erraten! SUPER!")

    else:
        tiane.say('Das Spiel kann leider nur über Telegram gespielt werden')
