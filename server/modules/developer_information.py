#Information on TIANE's developers and their contact details

import random

def get_answer(text, tiane):
    reply = ''
    if 'wer' in text or 'von wem' in text:
        if 'programmiert' in text or 'erschaffen' in text or 'entwickelt' in text:
            v = random.choice(['entwickelt', 'programmiert', 'erschaffen'])
            reply = 'Ich wurde von Ferdinand und Klara Krämer ' + v + '. Du kannst Team Krämer unter der folgenden email Adresse erreichen. jufo Punkt kraemer at gmail Punkt com.'
    elif 'kontaktieren' in text or 'erreichen' in text or 'email' in text or 'e mail' in text:
        if 'team ' in text or 'schöpfer' in text or 'programmierer' in text or 'entwickler' in text:
            reply = 'Du kannst Team Krämer unter der folgenden email Adresse erreichen. jufo Punkt team kraemer at gmail Punkt com.'
    return reply

def handle(text, tiane, profile):
    reply = get_answer(text, tiane)
    tiane.say(reply)

def isValid(text):
    text = text.lower()
    if 'wer' in text or 'von wem' in text:
        if 'programmiert' in text or 'erschaffen' in text or 'entwickelt' in text:
            return True
    elif 'kontaktieren' in text or 'erreichen' in text or 'email' in text or 'e mail' in text:
        if 'team ' in text or 'schöpfer' in text or 'programmierer' in text or 'entwickler' in text:
            return True
