import datetime
from datetime import date
import random

def get_date(text, tiane):
    tagesdifferenz = ''
    now = datetime.datetime.now()
    found_time = tiane.analysis.get('datetime')
    if found_time < now:
        event_time = str(found_time)
        found_time = event_time.replace(str(now.year), str((now.year + 1)))
        found_time = datetime.datetime.strptime(found_time, '%Y-%m-%d %H:%M:%S.%f')
    time_to_event = abs(found_time - now)
    daynr = time_to_event.days
    tagesdifferenz = 'in ' + str(daynr) + ' Tagen'
    if tagesdifferenz == '':
        if jetzt_jahr == jahr and jetzt_monat == monat and jetzt_tag == tag:
            tagesdifferenz == 'heute'
        else:
            d0 = date(int(jetzt_jahr), int(jetzt_monat), int(jetzt_tag))
            d1 = date(int(jahr), int(monat), int(tag))
            delta = d1 - d0
            delta = str(delta)
            elemente = str.split(delta)
            tagesanzahl = elemente[0]
            tagesanzahl = int(tagesanzahl)
            if tagesanzahl < 0:
                tagesdifferenz = ''
            elif tagesanzahl == 0:
                tagesdifferenz = 'heute'
            elif tagesanzahl == 1:
                tagesdifferenz = 'morgen'
            else:
                tagesdifferenz = 'in ' + str(tagesanzahl) + ' Tagen'
    return tagesdifferenz


def get_birthday(txt, tiane):
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
    answer = ''
    nutzer = tiane.local_storage['users'][tiane.user]
    try:
        geburtsdatum = nutzer['date_of_birth']
        jahr = geburtsdatum['year']
        monat = geburtsdatum['month']
        tag = geburtsdatum['day']
        tage = {1: 'ersten', 2: 'zweiten', 3: 'dritten', 4: 'vierten', 5: 'fünften',
            6: 'sechsten', 7: 'siebten', 8: 'achten', 9: 'neunten', 10: 'zehnten',
            11: 'elften', 12: 'zwölften', 13: 'dreizehnten', 14: 'vierzehnten', 15: 'fünfzehnten',
            16: 'sechzehnten', 17: 'siebzehnten', 18: 'achtzehnten', 19: 'neunzehnten', 20: 'zwanzigsten',
            21: 'einundzwanzigsten', 22: 'zweiundzwanzigsten', 23: 'dreiundzwanzigsten', 24: 'vierundzwanzigsten',
            25: 'fünfundzwanzigsten', 26: 'sechsundzwanzigsten', 27: 'siebenundzwanzigsten', 28: 'achtundzwanzigsten',
            29: 'neunundzwanzigsten', 30: 'dreißigsten', 31: 'einunddreißigsten', 32: 'zweiunddreißigsten'}
        day = tage.get(tag)
        month = tage.get(monat)
        answer = 'Dein Geburtstag ist am ' + day + ' ' + month + ' ' + str(jahr)
    except KeyError:
        answer = 'Ich weiß leider nicht, wann dein Geburtstag ist.'
    return answer


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
    ausgabe = ''
    if 'geburtstag' in text:
        ausgabe = get_birthday(text, tiane)
    else:
        datum = get_date(text, tiane)
        ausgabe = random.choice([datum + ' ist das Ereignis.', 'Das Ereignis ist ' + datum + '.'])
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
    if 'wie' in text:
        if 'lange' in text or 'tage' in text and 'viele' in text:
            return True
    if 'geburtstag' in text:
        return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'town': None, 'room': None, 'rooms': [None, 'Schlafzimmer'], 'datetime': datetime.datetime(2019, 6, 4, 12, 43, 35, 718049), 'time': {'day': 4, 'month': 6, 'year': 2019, 'hour': 12, 'minute': 43, 'second': 35}}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('In wie vielen Tagen ist der 4. Mai?', tiane, profile)
if __name__ == '__main__':
    main()
