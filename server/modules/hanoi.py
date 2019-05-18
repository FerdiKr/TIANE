import math

PRIORITY = 2

def faculty(x):
    if x == 0:
        return 1
    value = 1
    for i in range(1, x+1):
        value *= i
    return int(value)


def bk(n, k):
    if n == k:
        return 1
    if k < 0 or k > n:
        return 0
    value = faculty(n) / (faculty(k) * faculty(n - k))
    return int(value)


def t_(n, k):
    t = -1
    x = 0
    while n > x:
        t += 1
        x = bk(k-2+t, k-2)
    return t


def formula(n, k, t):
    """berechnet die Mindestzugzahl bei "n" Knickpunkten, "m" Plätzen und "AS" Scheiben"""
    if k == 3:
        return 2**(n)-1
    x = 0
    for i in range(0, t+1):
        x = x + 2**i*bk(i+k-3, k-3)
    correction = 2**t*(n-bk(t+k-2, k-2))
    return x + correction


def M(n, k):
    """berechnet die Mindestanzahl von Zügen, die für "As" Scheiben bei "m" Plätzen benötigt werden"""
    t = t_(n, k)
    x = formula(n, k, t)
    return x

def upsilon(n,k):
    s = t_(n,k)
    above = bk(s+k-3,k-3)
    below = bk(s+k-2,k-2)-n
    result = bk(above,below)
    return result

def movessequence(startpeg, endpeg, disklist, peglist):
    """gibt alle benoetigten Zuege zurueck"""
    #print("Die Scheiben {} sollen unter Benutzung der Felder {} von {} nach {} bewegt werden".format(disklist,peglist,startpeg,endpeg))
    #print(disklist)
    #spezialfaelle
    if len(disklist) == 1:
        #print("es bleibt nur eine Scheibe zum bewegen",disklist[0],startpeg,endpeg)
        return [[disklist[0], startpeg, endpeg]]

    else:
        #zwischenturmhoehe berechnen
        pegheight = calculatemiddletower(startpeg, endpeg, disklist, peglist)
        #dann die movessequencelist fuer die Zwischentuerme berechnen
        movesequencelist = []
        #bewege einen Zwischenturm nach dem anderen
        peglist2 = peglist.copy()
        disklist2 = disklist.copy()
        for peg in peglist:
            height = pegheight[peg]
            if height != 0:
                #print("aktuell bearbeiteter Zwischenturmpeg:",peg,"in Rekursionstiefe",n_recursion)
                movingdisks = disklist2[-height:]
                #print(movingdisks)
                movesequencelist += movessequence(startpeg,
                                                  peg, movingdisks, peglist2)
                peglist2.remove(peg)
                disklist2 = disklist2[:-height]

        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        #danach die groesste Scheibe
        #print("groesste Scheibe:",[disklist[0],startpeg,endpeg])
        #dann rueckwaerts
        lastmoves = []
        for i in range(1, len(movesequencelist)+1):
            #iterates from len(firstmoves)-1 to 0
            currentmove = movesequencelist[len(movesequencelist)-i]
            #tauschen von start und endpeg
            if currentmove[1] == startpeg:
                peg2 = endpeg
            elif currentmove[1] == endpeg:
                peg2 = startpeg
            else:
                peg2 = currentmove[1]
            if currentmove[2] == startpeg:
                peg1 = endpeg
            elif currentmove[2] == endpeg:
                peg1 = startpeg
            else:
                peg1 = currentmove[2]
            newcurrentmove = [currentmove[0], peg1, peg2]
            lastmoves.append(newcurrentmove)

        return movesequencelist[:]+[[disklist[0], startpeg, endpeg]]+lastmoves[:]


def calculatemiddletower(startpeg, endpeg, disklist, peglist):
    """berechnet die Hoehe der Zwischentuerme und gibt ein dict mit dem Zwischenturm als key und der hoehe als wert aus"""
    m = len(peglist)
    As = len(disklist)
    mmpegdict = {}
    n = 0
    x = 1
    while As > x:
        n += 1
        x = bk(n+m-2, m-2)

    #print(As,n)
    #berechnen der minimalen und maximalen Hoehe eines Zwischenturms
    i = 0
    for peg in peglist:
        if peg == startpeg or peg == endpeg:
            mmpegdict[peg] = [0, 0]
        else:
            mmpegdict[peg] = [int(bk(n+m-i-4, m-i-2)), int(bk(n+m-i-3, m-i-2))]
            i += 1

    #im Fall von einer Scheibe stimmt die minimale Hoehe nicht
    for peg in mmpegdict:
        if mmpegdict[peg][1] == 1:
            mmpegdict[peg][0] = 0

    #berechnen der abzueglichen Scheibenzahl fuer nicht-inkrementgrenzfaelle
    knowndisks = int(bk(n+m-2, m-2))
    toomuchdisks = knowndisks-As
    pegheightdict = {}
    #wegnehmen von der pegheigthdisklist
    takenallaway = False  # true wenn alle ueberfluessigen Scheiben weggenommen sind
    for peg in peglist:
        min_value = mmpegdict[peg][0]
        max_value = mmpegdict[peg][1]
        difference = max_value-min_value
        toomuchdisks -= difference
        if takenallaway:
            pegheightdict[peg] = max_value
        elif toomuchdisks >= 0:
            pegheightdict[peg] = min_value
        else:
            pegheightdict[peg] = max_value-toomuchdisks-difference
            takenallaway = True
    return pegheightdict


def movessequence_ui(n, k):
    peglist = []
    disklist = []
    for i in range(k):
        peglist.append(i)
    for i in range(n):
        disklist.append(i)
    moves = movessequence(peglist[0], peglist[-1], disklist, peglist)
    #print(moves, len(moves))
    return moves

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
    keyWords = ["scheibe","feld","platz","plätze","stab","stäbe","hanoi","upsilon","inkrement"]
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
