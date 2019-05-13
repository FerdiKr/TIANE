import math

def multiplikation(d):
    eins = d.get('eins')
    zwei = d.get('zwei')
    result = eins * zwei
    return result

def division(d):
    eins = d.get('eins')
    zwei = d.get('zwei')
    if zwei == 0:
        result = 'Möchtest du ein Wurmloch kreieren? Etwas durch null zu teilen beschwört Dämonen!'
    else:
        result = eins / zwei ###runden?
    return result

def addition(d):
    eins = d.get('eins')
    zwei = d.get('zwei')
    result = eins + zwei
    return result

def subtraktion(d):
    eins = d.get('eins')
    zwei = d.get('zwei')
    result = eins - zwei
    return result

def rechnen(text, tiane):
    ergebnis = ''
    e = False
    text = text.lower()
    satz = {}
    ind = 1
    i = str.split(text)
    for w in i:
        satz[ind] = w
        ind += 1
    for ix, wd in satz.items():
        try:
            if int(wd) >= 0 or int(wd) <= 0:
                eins = int(wd)
                eix = ix
                e = True
                break
        except ValueError or TypeError:
            e = False
    if e == True:
        rechenzeichen = satz.get(eix + 1)
        if rechenzeichen == 'geteilt':
            try:
                if int(satz.get(eix + 3)) >= 0 or int(satz.get(eix + 3)) <= 0: ################################################################## wie Type und Value verschachteln?
                    zwei = int(satz.get(eix + 3)) 
            except TypeError:
                try:
                    if int(satz.get(eix + 3)) >= 0 or int(satz.get(eix + 3)) <= 0:
                        zwei = int(satz.get(eix + 3))
                except ValueError:
                    ergebnis = 'Ich kann das Ergebnis leider nicht berechnen'
        else:
            try:
                if int(satz.get(eix + 2)) >= 0 or int(satz.get(eix + 2)) <= 0: 
                    zwei = int(satz.get(eix + 2))
            except TypeError:
                try:
                    if int(satz.get(eix + 2)) >= 0 or int(satz.get(eix + 2)) <= 0:
                        zwei = int(satz.get(eix + 2))
                except ValueError:
                    ergebnis = 'Ich kann das Ergebnis leider nicht berechnen'
        dic = {'eins': eins, 'zwei': zwei}
        #if text.lower().startswith('und'):
            #print('asked for: (same), parameter(s): {};{}, operator: {}'.format(eins,zwei,rechenzeichen))
        #else:
            #print('asked for: result, parameter(s): {};{}, operator: {}'.format(eins,zwei,rechenzeichen))
        #print('\n\ncalculating response...')
        if rechenzeichen == 'mal' or rechenzeichen == 'x':
            ergebnis = multiplikation(dic)
        elif rechenzeichen == 'geteilt' or rechenzeichen == 'durch' or rechenzeichen == '/':
            ergebnis = division(dic)
        elif rechenzeichen == 'plus' or rechenzeichen == 'und' or rechenzeichen == '+':
            ergebnis = addition(dic)
        elif rechenzeichen == 'minus' or rechenzeichen == '-':
            ergebnis = subtraktion(dic)
        else:
            ergebnis = ergebnis
    return ergebnis

def handle(text, tiane, profile):
    ergebnis = rechnen(text, tiane)
    e = str(ergebnis)
    e = e[:5]
    e = e.replace('.', (' Komma '))
    ausgabe = 'Die Lösung ist ' + e + '.'
    tiane.say(ausgabe)

def isValid(text):
    text = text.lower()
    if 'wie viel ist' in text or 'wie viel ergibt' in text or 'was ergibt' in text or 'was macht' in text or 'was ist' in text:
        return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '08', 'hour': '06', 'year': '2018', 'minute': '00', 'day': '27'}, 'town': 'None'}

    def say(self, text):
        print(text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Tiane wie viel ist 14 geteilt durch 5', tiane, profile)

if __name__ == '__main__':
    main()
