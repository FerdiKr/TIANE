import datetime
import random

def get_inhalt(txt, tiane):
    inhalt = ''
    start_index = 0
    satz = {}
    ind = 1
    sag_ind = 0
    tt = txt.replace('.', (''))
    tt = tt.replace('?', (''))
    tt = tt.replace('!', (''))
    tt = tt.replace('.', (''))
    tt = tt.replace(',', (''))
    tt = tt.replace('"', (''))
    tt = tt.replace('(', (''))
    tt = tt.replace(')', (''))
    tt = tt.replace('â‚¬', ('Euro'))
    tt = tt.replace('%', ('Prozent'))
    tt = tt.replace('$', ('Dollar'))
    text = tt.lower()
    i = str.split(text)
    nutzer = ''
    for w in i:
        satz[ind] = w
        ind += 1
    for index, word in satz.items():
        if word.lower() == 'sag' or word.lower() == 'sage': 
            sag_ind = index
            break
    if sag_ind != 500: 
        nutzer = satz.get(sag_ind + 1)
        vorhandene_nutzer = tiane.local_storage.get('users')
        if nutzer in vorhandene_nutzer.keys():
            nutzer = nutzer
            start_index = sag_ind + 2
        else:
            nutzer = ''
            start_index = sag_ind + 1
        if satz.get(start_index).lower() == 'bescheid':
            start_index += 1
            if satz.get(start_index).lower() == 'dass':
                start_index += 1
                for index, word in satz.items():
                    try:
                        if index == start_index:
                            inhalt = inhalt + word + ' '
                            start_index += 1
                    except ValueError:
                        inhalt = inhalt
                        break
        elif satz.get(start_index).lower() == 'dass':
            start_index += 1
            for index, word in satz.items():
                try:
                    if index == start_index:
                        inhalt = inhalt + word + ' '
                        start_index += 1
                except ValueError:
                    inhalt = inhalt
                    break
        else:
            for index, word in satz.items():
                try:
                    if index == start_index:
                        inhalt = inhalt + word + ' '
                        start_index += 1
                except ValueError:
                    inhalt = inhalt
                    break
    i_und_n = [inhalt, nutzer]
    return i_und_n

def get_aufruf(text, tiane):
    aufruf = ''
    i_und_n = get_inhalt(text, tiane)
    inhalt = i_und_n[0]
    inhalt = inhalt.replace(' mir', (' ' + tiane.user))
    inhalt = inhalt.replace(' mich', (' ' + tiane.user))
    inhalt = inhalt.replace(' ich', (' ' + tiane.user))
    inhalt = inhalt.replace('er', 'du')
    inhalt = inhalt.replace('sie', 'du')
    nutzer = i_und_n[1]
    aufruf = nutzer + ', ' + tiane.user + ' mÃ¶chte dir sagen, dass ' + inhalt
    x = aufruf[-1:]
    if x == ' ':
        aufruf = aufruf[:-1]
        x = aufruf[-1:]
    if x == 's':
        aufruf = aufruf + 't'
    else:
        aufruf = aufruf + 'st'
    return aufruf

def get_antwort(text, tiane):
    antwort = ''
    i_und_n = get_inhalt(text, tiane)
    nutzer = i_und_n[1]
    inhalt = i_und_n[0]
    inhalt = inhalt.replace(' mir', ' dir')
    inhalt = inhalt.replace(' mich', ' dich')
    inhalt = inhalt.replace(' ich', ' mich')
    antwort = 'Alles klar, ich sage ' + nutzer + ', dass ' + inhalt
    return antwort


def handle(text, tiane, profile):
    aufruf = get_aufruf(text, tiane)
    antwort = get_antwort(text, tiane)
    i_und_n = get_inhalt(text, tiane)
    nutzer = i_und_n[1]
    tiane.say(aufruf, user = nutzer)
    tiane.say(antwort, user = tiane.user)
    neuertext = tiane.listen(user = nutzer)
    if neuertext != 'TIMEOUT_OR_INVALID':
        if 'wo ist ' in neuertext.lower() and tiane.user in neuertext:
            usersdictionary = tiane.local_storage.get('users')
            user = usersdictionary.get(tiane.user)
            raum = user.get('room')
            if raum == 'KÃ¼che':
                zweite_antwort = random.choice([tiane.user + ' ist gerade in der KÃ¼che', tiane.user + ' ist momentan in der KÃ¼che'])
            else:
                zweite_antwort = random.choice([tiane.user + ' ist gerade im ' + raum, tiane.user + ' ist momentan im ' + raum])
            tiane.say(zweite_antwort, user = nutzer)
            
                    

def isValid(txt):
    tt = txt.replace('.', (''))
    tt = tt.replace('?', (''))
    tt = tt.replace('!', (''))
    tt = tt.replace('.', (''))
    tt = tt.replace(',', (''))
    tt = tt.replace('"', (''))
    tt = tt.replace('(', (''))
    tt = tt.replace(')', (''))
    tt = tt.replace('â‚¬', ('Euro'))
    tt = tt.replace('%', ('Prozent'))
    tt = tt.replace('$', ('Dollar'))
    text = tt.lower()
    if 'sag ' in text or 'sage ' in text or 'ruf ' in text or 'rufe ' in text:
        return True
    else:
        return False

class Tiane:
    def __init__(self):
        self.local_storage = {'users': {'Ferdi': {'name': 'Ferdi',
                                                  'uid': 1,
                                                  'room': 'Wohnzimmer'},
                                        'Klara': {'name': 'Klara',
                                                  'uid': 2,
                                                  'room': 'KÃ¼che'}
                                        }
                              }
        self.user = 'Klara'
        self.analysis = {'room': 'Wohnzimmer', 'time': {'month': 'None', 'hour': 'None', 'year': 'None', 'minute': 'None', 'day': 'None'}, 'town': 'None'}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext
        

def main():
    profile = {}
    tiane = Tiane()
    handle('Sag Ferdi Bescheid dass er zu mir in die KÃ¼che kommen soll', tiane, profile)
    
    
if __name__ == "__main__":
    main()

