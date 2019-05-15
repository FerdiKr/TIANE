import random


def output(txt, tiane):
    output = ''
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
    t = str.split(text)
    if 'münze' in text or ('kopf' in text and 'oder' in text and 'zahl' in text):
        q = random.randint(1,2)
        if q == 1:
            output = 'kopf'
        else:
            output = 'zahl'
    elif 'würfel' in text or 'alea iacta est' in text:
        q = random.randint(1,6)
        if q == 1:
            output = 'eins'
        elif q == 2:
            output = 'zwei'
        elif q == 3:
            output = 'drei'
        elif q == 4:
            output = 'vier'
        elif q == 5:
            output = 'fünf'
        else:
            output = 'sechs'
    elif (('zufall' in text or 'zufällig' in text) and 'zahl' in text):
        output = str(random.randint(0,100))
    return output

def handle(text, tiane, profile):
    ausgabe = output(text, tiane)
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
    if 'münze' in text or ('kopf' in text and 'oder' in text and 'zahl' in text) or 'würfel' in text or (('zufall' in text or 'zufällig' in text) and 'zahl' in text):
        return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '08', 'hour': '06', 'year': '2018', 'minute': '00', 'day': '27'}, 'town': 'None'}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Tiane wirf einen würfel', tiane, profile)

if __name__ == '__main__':
    main()
