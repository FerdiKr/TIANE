import random
import re

zwischenPattern = re.compile(r'.*(von|zwischen) (-?\d+) (und|bis) (-?\d+).*', re.I)
bisPattern = re.compile(r'.*(bis|kleiner gleich) (-?\d+).*', re.I)
kleinerPattern = re.compile(r'.*(unter|kleiner) (als)? (-?\d+).*', re.I)

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
        try:
            match = zwischenPattern.match(text)
            if (output == '' and match is not None):
                if (int(match.group(2)) < int(match.group(4))):
                    output = str(random.randint(int(match.group(2)), int(match.group(4))))
                else:
                    output = str(random.randint(int(match.group(4)), int(match.group(2))))
            match = bisPattern.match(text)
            if (output == '' and match is not None):
                if (match.group(2) > 0):
                    output = str(random.randint(1, int(match.group(2))))
                else:
                    output = str(random.randint(int(match.group(2)), 1))
            match = kleinerPattern.match(text)
            if (output == '' and match is not None):
                if (match.group(3) > 0):
                    output = str(random.randrange(1, int(match.group(3))))
                else:
                    output = str(random.randrange(int(match.group(3)), 1))
        except ValueError:
            output = ''
        if (output == ''):
            output = str(random.randint(1,100))
    return output

def handle(text, tiane, profile):
    ausgabe = output(text, tiane).strip()
    if (ausgabe.startswith('-')):
        ausgabe = 'minus ' + ausgabe[1:]
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
