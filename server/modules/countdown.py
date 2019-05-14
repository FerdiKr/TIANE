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
    monate = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    monat = int(monat)
    month_in_format = str(monate.get(monat))
    xs = ''
    xs = xs + str(tag) + ' '
    xs = xs + month_in_format + ' '
    xs = xs + str(jahr)
    ts = datetime.datetime.now()
    heute = ts.strftime('%d %b %Y')
    diff =  datetime.datetime.strptime(xs, '%d %b %Y') - datetime.datetime.strptime(heute, '%d %b %Y')
    daynr = diff.days
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
