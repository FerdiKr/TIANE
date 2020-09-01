#Information on TIANE's developers and their contact details

SECURE = True

import random

def get_answer(text, tiane):
    reply = ''
    if 'github' in text or 'quellcode' in text or 'repository' in text:
        reply = 'Mein GitHub-Repository findest du unter https://github.com/FerdiKr/TIANE. Meine Entwickler freuen sich über Beiträge!'
    elif 'wer' in text or 'von wem' in text:
        if 'programmiert' in text or 'erschaffen' in text or 'entwickelt' in text or 'erstellt' in text:
            v = random.choice(['entwickelt', 'programmiert', 'erschaffen'])
            if tiane.telegram_call:
                reply = 'Ich wurde von Ferdinand und Klara Krämer ' + v + '. Du kannst Team Krämer unter der folgenden email Adresse erreichen: jufo.teamkraemer@gmail.com.'
            else:
                reply = 'Ich wurde von Ferdinand und Klara Krämer ' + v + '. Du kannst Team Krämer unter der folgenden email Adresse erreichen. jufo Punkt team kraemer ät g mail Punkt com.'
    elif 'kontaktieren' in text or 'erreichen' in text or 'email' in text or 'e mail' in text:
        if 'team ' in text or 'schöpfer' in text or 'programmierer' in text or 'entwickler' in text:
            if tiane.telegram_call:
                reply = 'Du kannst Team Krämer unter der folgenden email Adresse erreichen: jufo.teamkraemer@gmail.com.'
            else:
                reply = 'Du kannst Team Krämer unter der folgenden email Adresse erreichen. jufo Punkt team kraemer ät g mail Punkt com.'
    return reply

def handle(text, tiane, profile):
    text = text.lower()
    reply = get_answer(text, tiane)
    tiane.say(reply)

def isValid(text):
    text = text.lower()
    if 'wer' in text or 'von wem' in text:
        if 'programmiert' in text or 'erschaffen' in text or 'entwickelt' in text or 'erstellt' in text:
            return True
    if 'kontaktieren' in text or 'erreichen' in text or 'email' in text or 'e mail' in text:
        if 'team ' in text or 'schöpfer' in text or 'programmierer' in text or 'entwickler' in text:
            return True
    if 'github' in text or 'quellcode' in text or 'repository' in text:
        return True
