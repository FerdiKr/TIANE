import datetime
from datetime import date
import random

def get_date(text, tiane):
    tagesdifferenz = ''
    now = datetime.datetime.now()
    datum = ''
    jetzt_jahr = now.year
    jetzt_monat = now.month
    jetzt_tag = now.day
    time = tiane.analysis.get('time')
    jahr = time.get('year')
    if jahr == 'None':
        jahr = str(now.year)
    tag = time.get('day')
    if tag == 'None':
        tag = str(now.day)
    monat = time.get('month')
    if monat == 'None':
        if int(tag) == 28:
            if now.month == 2:
                if int(jahr) / 4 == 0:
                    monat = '3'
                else:
                    monat = '2'
            else:
                monat = str(now.month)
        elif int(tag) == 29:
            if now.month == 2:
                monat = '3'
            else:
                monat = str(now.month)
        elif int(tag) == 30:
            if now.month == 4 or now.month == 6 or now.month == 9 or now.month == 11:
                monat = str(now.month + 1)
            else:
                monat = str(now.month)
        elif int(tag) == 31:
            monat = str(now.month + 1)
        else:
            monat = str(now.month)

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

def get_birthday(text, tiane):
    now = datetime.datetime.now()
    Tage = {'01': 'ersten', '02': 'zweiten', '03': 'dritten', '04': 'vierten', '05': 'fünften',
            '06': 'sechsten', '07': 'siebten', '08': 'achten', '09': 'neunten', '10': 'zehnten',
            '11': 'elften', '12': 'zwölften', '13': 'dreizehnten', '14': 'vierzehnten', '15': 'fünfzehnten',
            '16': 'sechzehnten', '17': 'siebzehnten', '18': 'achtzehnten', '19': 'neunzehnten', '20': 'zwanzigsten',
            '21': 'einundzwanzigsten', '22': 'zweiundzwanzigsten', '23': 'dreiundzwanzigsten', '24': 'vierundzwanzigsten',
            '25': 'fünfundzwanzigsten', '26': 'sechsundzwanzigsten', '27': 'siebenundzwanzigsten', '28': 'achtundzwanzigsten',
            '29': 'neunundzwanzigsten', '30': 'dreißigsten', '31': 'einunddreißigsten', '32': 'zweiunddreißigsten'}

    Monate = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni',
              '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November',
              '12': 'Dezember'}
    benutzer = tiane.user
    date = benutzer.get('date_of_birth')
    b_day = date.get('day')
    b_month = date.get('month')
    if b_day == 0 or b_month == 0:
        antwort = 'Ich weiß leider nicht, wann der Geburtstag ist.'
    else:
        if b_day <= 9:
            b_day = '0' + str(b_day)
        else:
            b_day = str(b_day)
        tag = Tage.get(b_day)
        if b_month <= 9:
            b_month = '0' + str(b_month)
        else:
            b_month = str(b_month)
        monat = Monate.get(b_month)
        antwort = 'Geburtstag ist am ' + tag + ' ' + monat + '.'
    return antwort

def get_past_date(text, tiane):
    now = datetime.datetime.now()
    jetzt_jahr = now.year
    jetzt_monat = now.month
    jetzt_tag = now.day
    time = tiane.analysis.get('time')
    jahr = time.get('year')
    if jahr == 'None':
        jahr = str(now.year)
    tag = time.get('day')
    if tag == 'None':
        tag = str(now.day)
    monat = time.get('month')
    if monat == 'None':
        if int(tag) == 28:
            if now.month == 2:
                if int(jahr) / 4 == 0:
                    monat = '3'
                else:
                    monat = '2'
            else:
                monat = str(now.month)
        elif int(tag) == 29:
            if now.month == 2:
                monat = '3'
            else:
                monat = str(now.month)
        elif int(tag) == 30:
            if now.month == 4 or now.month == 6 or now.month == 9 or now.month == 11:
                monat = str(now.month + 1)
            else:
                monat = str(now.month)
        elif int(tag) == 31:
            monat = str(now.month + 1)
        else:
            monat = str(now.month)

    d0 = date(int(jetzt_jahr), int(jetzt_monat), int(jetzt_tag))
    d1 = date(int(jahr), int(monat), int(tag))
    delta = d0 - d1
    delta = str(delta)
    elemente = str.split(delta)
    tagesanzahl = elemente[0]
    if tagesanzahl == 1:
        differenz = 'gestern'
    else:
        differenz = 'vor ' + str(tagesanzahl) + ' Tagen'
    return differenz



def handle(text, tiane, profile):
    ausgabe = ''
    datum = get_date(text, tiane)
    if datum == '':
        datum = get_past_date(text, tiane)
        ausgabe = random.choice([datum + ' war das Ereignis.', 'Das Ereignis war ' + datum + '.'])
    else:
        ausgabe = random.choice([datum + ' ist das Ereignis.', 'Das Ereignis ist ' + datum + '.'])
    tiane.say(ausgabe)

def isValid(text):
    text = text.lower()
    if 'wie' in text:
        if 'lange' in text or 'tage' in text and 'viele' in text or 'wann' in text and 'geburtstag' in text:
            return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '09', 'hour': '05', 'year': '2018', 'minute': '00', 'day': '19'}, 'town': 'None'}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Vor wie vielen Tagen war Ferdis Geburtstag', tiane, profile)
if __name__ == '__main__':
    main()
