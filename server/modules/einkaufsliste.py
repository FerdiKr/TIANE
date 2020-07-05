import datetime
from datetime import date
import random

SECURE = True

def get_item(txt, tiane):
    item = ''
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
    eingabe = tt.lower()
    satz = {}
    mind = 1 
    i = str.split(eingabe)
    ind = 1 
    for w in i:
        satz[ind] = w 
        ind += 1
    if 'setz' in eingabe and 'auf die' in eingabe:
        for iindex, word in satz.items():
            if word == 'setz' or word == 'setze':
                start = iindex
                for iindex, word in satz.items():
                    if iindex == start + mind:
                        if word != 'auf':
                            item = item + word + ' '
                            mind += 1
                        else:
                            break
    elif 'füg' in eingabe and 'zu' in eingabe:
        for iindex, word in satz.items():
            if word == 'füg' or word == 'füge':
                start = iindex
                for iindex, word in satz.items():
                    if iindex == start + mind:
                        if word != 'liste':
                            item = item + word + ' '
                            mind += 1
                        else:
                            h = str.split(item)
                            i = h[0:len(h)-1]
                            j = h[len(h)-1:]
                            if j == 'gemeinsamen':
                                i = i[0:len(h)-2]
                            else:
                                i = i
                            item = ''
                            for x in i:
                                item = item + str(x) + ' '
                            break
    else:
        item = item
    return item


def get_aussage(txt, tiane): #Imperfection
    aussage = ''
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
    eingabe = tt.lower()
    nutzer = tiane.user
    usersdictionary = tiane.local_storage.get('users')
    nutzerdictionary = usersdictionary.get(nutzer)
    if 'liste' in nutzerdictionary.keys():
        liste = nutzerdictionary.get('liste')
        i = 0
        if len(liste) > 1:
            while i < len(liste) - 1:
                aktuellesitem = liste[i]
                aussage = aussage + aktuellesitem + ', '
                i += 1
            aussage = aussage + ' und ' + liste[len(liste) - 1]
        else:
            while i < len(liste):
                aktuellesitem = liste[i]
                aussage = aussage + aktuellesitem + ', '
                i += 1
    else:
        aussage = ''
    return aussage


def get_aussage_gemeinsam(txt, tiane): #fertig und sollte laufen
    aussage = ''
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
    eingabe = tt.lower()
    liste = tiane.local_storage.get('liste')
    i = 0
    while i < len(liste) - 1:
        aktuellesitem = liste[i]
        aussage = aussage + aktuellesitem + ', '
        i += 1
    aussage = aussage + ' und ' + liste[len(liste) - 1]
    return aussage


def handle(txt, tiane, profile):
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
    if 'gemeinsame' in text and 'liste' in text:
        if 'setze' in text and 'auf die' in text or 'füg' in text and 'zu' in text:
            item = get_item(text, tiane)
            if text != '_UNDO_':
                ausgabe = ''
                liste = {}
                if 'liste' in tiane.local_storage.keys():
                    tiane.local_storage['liste'].append(item)
                else:
                    tiane.local_storage['liste'] = item
                ausgabe = random.choice(['In Ordnung, ich habe ' + str(item) + 'zur gemeinsamen Liste hinzugefügt.', 'Alles klar, ich habe ' + str(item) + 'auf die gemeinsame Liste gesetzt.', 'Alles klar, {}, ich habe '.format(tiane.user) + str(item) + 'zur gemeinsamen Liste hinzugefügt.', 'In Ordnung, {}, ich habe '.format(tiane.user) + str(item) + 'auf die gemeinsame Liste gesetzt.']) #
                tiane.say(ausgabe)
        elif 'steht' in text and 'auf' in text or 'was sagt die' in text or 'gibt' in text and 'auf' in text:
            aussage = get_aussage_gemeinsam(text, tiane)
            if aussage != '':
                ausgabe = 'Auf der geimeinsamen Liste steht ' + aussage + ', {}.'.format(tiane.user)
            else:
                ausgabe = random.choice(['Aktuell steht nichts auf der gemeinsamen Liste.', 'Aktuell steht nichts auf der gemeinsamen Liste, {}.'.format(tiane.user), 'Gerade steht nichts auf der gemeinsamen Liste.', 'Gerade steht nichts auf der gemeinsamen Liste, {}.'.format(tiane.user)])
            tiane.say(ausgabe) 
    else:
        if 'setze' in text and 'auf die' in text or 'füge' in text and 'zu' in text:
            item = get_item(text, tiane)
            if text != '_UNDO_':
                ausgabe = ''
                liste = {}
                nutzer = tiane.user
                nutzerdictionary = tiane.local_storage.get('users')
                nd = nutzerdictionary.get(nutzer)
                if 'liste' in nd.keys():
                    nd['liste'].append(item)
                else:
                    nd['liste'] = item
                ausgabe = random.choice(['In Ordnung, ich habe ' + str(item) + 'zur Liste hinzugefügt.', 'Alles klar, ich habe ' + str(item) + 'auf die Liste gesetzt.', 'Alles klar, {}, ich habe '.format(tiane.user) + str(item) + 'zur Liste hinzugefügt.', 'In Ordnung, {}, ich habe '.format(tiane.user) + str(item) + 'auf die Liste gesetzt.']) 
                tiane.say(ausgabe)
        elif 'steht' in text and 'auf' in text or 'was sagt die' in text or 'gibt' in text and 'auf' in text:
            aussage = get_aussage(text, tiane)
            if aussage != '':
                ausgabe = 'Auf der Liste steht für dich ' + aussage + ', {}.'.format(tiane.user)
            else:
                ausgabe = random.choice(['Für dich steht aktuell nichts auf der Liste.', 'Für dich steht aktuell nichts auf der Liste, {}.'.format(tiane.user), 'Für dich steht gerade nichts auf der Liste.', 'Für dich steht gerade nichts auf der Liste, {}.'.format(tiane.user)])
            tiane.say(ausgabe)


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
    if 'liste' in text:
        if 'setze' in text and 'auf die' in text or 'füge' in text and 'zu' in text:
            return True
        elif 'steht' in text and 'auf' in text or 'was sagt die' in text or 'gibt' in text and 'auf' in text:
            return True
        else: return False
    else:
        return False

class Tiane:
    def __init__(self):
        self.local_storage = {'liste': ['Mehl', 'Butter', 'Cornflakes', 'Äpfel kaufen'], 'users':{'Ferdi': {'name': 'Ferdi', 'liste': ['gefrorene himbeeren', 'chips und cola', 'Schokolade', 'Nudeln']},
                                                                                                  'Klara': {'name': 'Klara', 'liste': ['zur oma gehen', 'Kuchen backen']}}}
        self.user = 'Ferdi'
        self.analysis = {'room': 'None', 'time': {'month': '09', 'hour': '05', 'year': '2018', 'minute': '00', 'day': '19'}, 'town': 'None'}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Füge Putzen zur Liste hinzu', tiane, profile)
if __name__ == '__main__':
    main()
