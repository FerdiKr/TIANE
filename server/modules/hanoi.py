import math

PRIORITY = 2

def toh

def multiplikation(d, t):
    eins = d.get('eins')
    zwei = d.get('zwei')
    result = eins * zwei
    return result

def division(d, t):
    eins = d.get('eins')
    zwei = d.get('zwei')
    if zwei == 0:
        result = 'Möchtest du ein Wurmloch kreieren? Etwas durch null zu teilen beschwört Dämonen!'
    else:
        result = eins / zwei
    return result

def potenzierung(d, t):
    eins = d.get('eins')
    zwei = d.get('zwei')
    if zwei == 0:
        result = 1
    elif zwei == 1:
        result = eins
    else:
        result = eins ** zwei
    return result

def addition(d, t):
    eins = d.get('eins')
    zwei = d.get('zwei')
    f = False
    if '*' in t:
        text = t.lower()
        satz = {}
        ind = 1
        i = str.split(text)
        for w in i:
            satz[ind] = w
            ind += 1
        for i, w in satz.items():
            if w == '*':
                try:
                    e = int(satz.get(i-1))
                    z = int(satz.get(i+1))
                    ergebnis = e * z
                    f = True
                    g = True
                except ValueError or TypeError:
                    g = False
                    break
    if f == False:
        result = eins + zwei
    else:
        if g == True:
            result = ergebnis + eins
        else:
            result = ''
    return result

def subtraktion(d, t):
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
    rechenzeichen = ''
    for w in i:
        satz[ind] = w
        ind += 1
    for ix, wd in satz.items():
        if wd == '*' or wd == 'x':
            try:
                eins = int(satz.get(ix-1))
                zwei = int(satz.get(ix+1))
                rechenzeichen = 'mal'
            except ValueError or TypeError:
                break
    for ix, wd in satz.items():
        if wd == '+':
            try:
                eins = int(satz.get(ix-1))
                zwei = int(satz.get(ix+1))
                rechenzeichen = 'plus'
            except ValueError or TypeError:
                break
    for ix, wd in satz.items():
        if wd == '-':
            try:
                eins = int(satz.get(ix-1))
                zwei = int(satz.get(ix+1))
                rechenzeichen = 'minus'
            except ValueError or TypeError:
                break
    for ix, wd in satz.items():
        if wd == '/':
            try:
                eins = int(satz.get(ix-1))
                zwei = int(satz.get(ix+1))
                rechenzeichen = '/'
            except ValueError or TypeError:
                break
    for ix, wd in satz.items():
        if wd == 'hoch' or wd == '**':
            try:
                eins = int(satz.get(ix-1))
                zwei = int(satz.get(ix+1))
                rechenzeichen = 'hoch'
            except ValueError or TypeError:
                break
    if rechenzeichen != 'Baum':
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
            if rechenzeichen == '':
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
        if rechenzeichen == 'mal' or rechenzeichen == 'x' or rechenzeichen == '*':
            ergebnis = multiplikation(dic, text)
        elif rechenzeichen == 'geteilt' or rechenzeichen == 'durch' or rechenzeichen == '/':
            ergebnis = division(dic, text)
        elif rechenzeichen == 'plus' or rechenzeichen == 'und' or rechenzeichen == '+':
            ergebnis = addition(dic, text)
        elif rechenzeichen == 'minus' or rechenzeichen == '-':
            ergebnis = subtraktion(dic, text)
        elif rechenzeichen == 'hoch':
            ergebnis = potenzierung(dic, text)
        else:
            ergebnis = ergebnis
    return ergebnis

def handle(txt, tiane, profile):
    '''
    tt = txt.replace('?', (''))
    tt = tt.replace('!', (''))
    tt = tt.replace('"', (''))
    tt = tt.replace('(', (''))
    tt = tt.replace(')', (''))
    tt = tt.replace('â‚¬', ('Euro'))
    tt = tt.replace('%', ('Prozent'))
    tt = tt.replace('$', ('Dollar'))
    text = tt.lower()
    try:
        easy_e = int(text)
    except ValueError:
        easy_e = 'x'
    if str(easy_e) != 'x':
        tiane.say('Die Lösung ist ' + str(easy_e) + '.')
    else:
        ergebnis = rechnen(text, tiane)
        e = str(ergebnis)
        if '.' in e:
            e = e[:6] ##imperfect for high numbers with .!
            e = e.replace('.', (' Komma '))
        if e != ' ' and e != '':
            if e == 'Möchtest du ein Wurmloch kreieren? Etwas durch null zu teilen beschwört Dämonen!':
                tiane.say(e)
            else:
                tiane.say('Die Lösung ist ' + e + '.')
        else:
            tiane.say('Das kann ich leider nicht berechnen.')
    '''
    

def isValid(text):
    text = text.lower()
    ret = False
    keyWords = ["scheiben","felder","plätze"]
    for i in keyWords:
        if i in text:
            ret = True
        if ret:
            break
    return ret

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
    handle('0 / 0', tiane, profile)

if __name__ == '__main__':
    main()
