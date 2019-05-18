import math
import re

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

def movenumber(text):
    text = text.lower()
    textlist = re.split("\s", text)
    nosuccess = False
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1]
                except:
                    nosuccess = True
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    nosuccess = True
    if not nosuccess:
        ret = "Für {} Scheiben und {} Felder benötigt man mindestens {} Züge.".format(n, k , M(n,k))
    else:
        ret = "Ich konnte leider keine Zugzahl ermitteln
    return ret, not nosuccess

def possibilitynumber(n,k):
    text = text.lower()
    textlist = re.split("\s", text)
    success = True
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1]
                except:
                    success = False
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    success = False
    if success:
        ret = "Um die Türme von Hanoi mit {} Scheiben und {} Felder optimal zu lösen, gibt es {} Möglichkeiten.".format(n, k , upsilon(n,k))
    else:
        ret = "Ich konnte die Anzahl der Möglichkeiten leider nicht ermitteln
    return ret, success

def movetime(text):
    text = text.lower()
    textlist = re.split("\s", text)
    nosuccess = False
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1]
                except:
                    nosuccess = True
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    nosuccess = True
    if not nosuccess:
        m = M(n,k)
        years = int(m/(3600*24*365))
        remaining = m-years *3600*24*365
        months = int(remaining/(3600*24*(365/12)))
        remaining -= months * 3600*24*(365/12)
        days = int(remaining/(3600*24))
        remaining -= days *3600*24
        hours = int(remaining/(3600))
        remaining -= hours * 3600
        minutes = int(remaining/60)
        remaining -= minutes * 60
        seconds = remaining

        time_string = ""
        if years > 0:
            if years ==1:
                time_string += "1 Jahr"
            else:
                time_string += str(years) + " Jahre"
        
        if months > 0:
            time_string += ","
            if months == 1:
                time_string += "1 Monat"
            else:
                time_string += str(months) + " Monate"
        
        if days > 0:
            time_string += ","
            if months == 1:
                time_string += "1 Tag"
            else:
                time_string += str(days) + "Tage"
        
        if days > 0:
            time_string += ","
            if days == 1:
                time_string += "1 Tag"
            else:
                time_string += str(days) + "Tage"

        if hours > 0:
            time_string += ","
            if hours == 1:
                time_string += "1 Stunde"
            else:
                time_string += str(hours) + "Stunden"
        
        if minutes > 0:
            time_string += ","
            if minutes == 1:
                time_string += "1 Minute"
            else:
                time_string += str(minutes) + "Minuten"
        
        if seconds > 0:
            time_string += ","
            if seconds == 1:
                time_string += "1 Sekunde"
            else:
                time_string += str(seconds) + "Sekunden"

        ret = "Wenn man pro Sekunde einen Zug macht, benötigt man für {} Scheiben und {} Felder {}.".format(n, k , timestring)
    else:
        ret = "Ich konnte leider keine Zugzahl ermitteln
    success = not nosuccess
    return ret, success

def moves(text):
    text = text.lower()
    textlist = re.split("\s", text)
    nosuccess = False
    ret = ''
    for index, word in enumerate(textlist):
        if index > 1:
            if re.search(r"feld|felder|platz|plätze|stab|stäbe", word):
                try:
                    k = int(textlist[index-1]
                except:
                    nosuccess = True
            if re.search(r"scheibe|scheiben|klotz|klötze", word):
                try:
                    n = int(textlist[index-1])
                except:
                    nosuccess = True
    if not nosuccess:
        moveslist = movessequence(n, k)

        for move in moveslist:
            #disk = move[0]
            startpeg = str(move[1])
            endpeg = str(move[2])
            ret += 'Bewege {} die oberste Scheibe von Feld {} nach Feld {}.'.format(konjunctionlist[random.randint(0,len(konjunctionlist))], startpeg, endpeg)


        ret = "Für {} Scheiben und {} Felder benötigt man mindestens {} Züge.".format(n, k , M(n,k))
    else:
        ret = "Ich konnte leider keine Zugzahl ermitteln
    return ret, not nosuccess

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
    tt = txt.replace('?', (''))
    tt = tt.replace('!', (''))
    tt = tt.replace('"', (''))
    tt = tt.replace('(', (''))
    tt = tt.replace(')', (''))
    text = tt.lower()

    keyPossibilities = ['möglichkeit','upsilon']
    keyMoveSequence  = ['zugfolge']
    keyMoveNumber    = ['züge']
    keyTime          = ['wie lang','dauert']
    weiter = True

    for key in keyMoveNumber:
        if key in text:
            answer, success = movenumber(text)
            weiter = False
            break

    if weiter:
        for key in keyPossibilities:
            if key in text:
                answer, success = possibilitynumber(text)
                weiter = False
                break

    if weiter:
        for key in keyMoveSequence:
            if key in text:
                # answer, success = movenumber(text)
                # Methode für MoveSequence
                weiter = False
                break
                
    if weiter:
        for key in keyTime:
            if key in text:
                # answer, success = movenumber(text)
                # Methode für Zeit sagen
                break
    

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
