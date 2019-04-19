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
    if 'wirf die mÃ¼nze' in text or 'was sagt die mÃ¼nze' in text or 'frag die mÃ¼nze' in text:
        q = random.randint(1,2)
        if q == 1:
            output = 'kopf'
        else:
            output = 'zahl'
    elif 'kopf oder zahl' in text:
        q = random.randint(1,2)
        if q == 1:
            output = 'kopf'
        else:
            output = 'zahl'
    elif 'wÃ¼rfel' in text or 'alea iacta est' in text:
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
            output = 'fÃ¼nf'
        else:
            output = 'sechs'
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
    if 'mÃ¼nze' in text or 'kopf' in text or 'zahl' in text or 'wÃ¼rfel' in text:
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
    handle('Tiane wirf die mÃ¼nze', tiane, profile)

if __name__ == '__main__':
    main()
