import datetime

def uhrzeit(dicanalyse):

    now = datetime.datetime.now()

    time = dicanalyse.get('time')

    jahr = time.get('year')

    if jahr == 'None':

        jahr = str(now.year)

    tag = time.get('day')

    if tag == 'None':

        tag = str(now.day)

        if int(tag) <= 9:

            tag = '0' + tag

    monat = time.get('month')

    if monat == 'None':

        if int(tag) == 28:

            if now.month == 2:

                if int(jahr) / 4 == 0:

                    monat = '03'

                else:

                    monat = '02'

            else:

                monat = str(now.month)

                if int(monat) <= 9:

                    monat = '0' + monat

        elif int(tag) == 29:

            if now.month == 2:

                monat = '03'

            else:

                monat = str(now.month)

                if int(monat) <= 9:

                    monat = '0' + monat

        elif int(tag) == 30:

            if now.month == 4 or now.month == 6 or now.month == 9 or now.month == 11:

                monat = str(now.month + 1)

            else:

                monat = str(now.month)

            if int(monat) <= 9:

                monat = '0' + monat

        elif int(tag) == 31:

            monat = str(now.month + 1)

            if int(monat) <= 9:

                monat = '0' + monat

        else:

            monat = str(now.month)

            if int(monat) <= 9:

                monat = '0' + monat

    stunde = time.get('hour')

    if stunde == 'None':

         stunde = '08'

    minute = time.get('minute')

    if minute == 'None':

         minute = '00'

    zeit = jahr + '-' + monat + '-' + tag + ' ' + stunde + ':' + minute + ':' + '00.000000'

    return zeit



def get_text(tiane, text):

    remembrall = ''

    e_ind = 0

    text = text.lower()

    if ' zu ' not in text:

        remembrall = text.replace('zu', (''))

        remembrall = remembrall.replace(' ans ', (' '))

    else:

        remembrall = text.replace(' ans ', (' '))

    if ' in ' in text and ' minuten' in text:

        remembrall = remembrall.replace(' minuten ', (' '))

        remembrall = remembrall.replace(' in ', (' '))

        s = str.split(remembrall)

        for t in s:

            try:
                
                if int(t) >= 0:

                    remembrall = remembrall.replace(t, (''))

            except ValueError:

                remembrall = remembrall

    satz = {}

    ausgabe = ''

    ind = 1

    i = str.split(remembrall)

    for w in i:

        satz[ind] = w

        ind += 1              

    if ' am ' in satz.items():

        for index, word in satz.items():

            if word == 'am':

                am_ind = index

                try:

                    if int(satz.get(am_ind + 2)):

                        summand = 3

                        for i, w in satz.items():

                            try:

                                ausgabe = ausgabe + satz.get(am_ind + summand) + ' '

                                summand += 1

                            except TypeError:

                                ausgabe = ausgabe

                except ValueError or TypeError:

                    summand = 2

                    for i, w in satz.items():

                        try:

                            ausgabe = ausgabe + satz.get(am_ind + summand) + ' '

                            summand += 1

                        except TypeError:

                            ausgabe = ausgabe

    elif ' daran das' in text:

        for ind, w in satz.items():
            
            if w == 'daran':

                reminder = ''

                n = 1

                try:

                    try:

                        while n < 30:
                            
                            if satz.get(ind + n) != None:

                                reminder = reminder + str(satz.get(ind + n)) + ' '

                                n += 1

                            else:

                                reminder = reminder

                                break

                    except KeyError:

                        reminder = reminder

                        break

                except ValueError:

                    reminder = reminder

                    break

                ausgabe = reminder

                        
    else:

        for index, word in satz.items():

            if word == 'erinner' or word == 'erinnere':

                e_ind = index

                s_ind = e_ind + 2

                ausgabe = satz.get(s_ind) + ' '

                summand = 1

                for i, w in satz.items():

                    try:

                        ausgabe = ausgabe + satz.get(s_ind + summand) + ' '

                        summand += 1

                    except TypeError:

                        ausgabe = ausgabe

    ausgabe = ausgabe.replace('übermorgen ', (' '))

    ausgabe = ausgabe.replace('morgen ', (' '))

    ausgabe = ausgabe.replace('daran ', (' '))

    return ausgabe





def get_time_for_reply(dicanalyse):

    now = datetime.datetime.now()

    time = dicanalyse.get('time')

    jahr = time.get('year')

    if jahr == 'None':

        jahr = str(now.year)

    tag = time.get('day')

    if tag == 'None':

        tag = str(now.day)

        if int(tag) <= 9:

            tag = '0' + tag

    monat = time.get('month')

    if monat == 'None':

        monat = str(now.month)

        if int(monat) <= 9:

            monat = '0' + str(monat)

    stunde = time.get('hour')

    if stunde == 'None':

         stunde = str(now.hour) #08

         if int(stunde) <= 9:

             stunde = '0' + stunde

    minute = time.get('minute')

    if minute == 'None':

         minute = '00'

    zeit = {'year': jahr, 'month': monat, 'day': tag, 'hour': stunde, 'minute': minute}

    return zeit



def get_reply(tiane, dicanalyse):

    time = get_time_for_reply(dicanalyse)

    jahr = time.get('year')

    monat = time.get('month')

    tag = time.get('day')

    stunde = time.get('hour')

    minute = time.get('minute')

    tage = {'01': 'ersten', '02': 'zweiten', '03': 'dritten', '04': 'vierten', '05': 'fünften',
                '06': 'sechsten', '07': 'siebten', '08': 'achten', '09': 'neunten', '10': 'zehnten',
                '11': 'elften', '12': 'zwölften', '13': 'dreizehnten', '14': 'vierzehnten', '15': 'fünfzehnten',
                '16': 'sechzehnten', '17': 'siebzehnten', '18': 'achtzehnten', '19': 'neunzehnten', '20': 'zwanzigsten',
                '21': 'einundzwanzigsten', '22': 'zweiundzwanzigsten', '23': 'dreiundzwanzigsten', '24': 'vierundzwanzigsten',
                '25': 'fünfundzwanzigsten', '26': 'sechsundzwanzigsten', '27': 'siebenundzwanzigsten', '28': 'achtundzwanzigsten',
                '29': 'neunundzwanzigsten', '30': 'dreißigsten', '31': 'einunddreißigsten', '32': 'zweiunddreißigsten'}

    Monate = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni',
                  '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November',
                  '12': 'Dezember'}

    Stunden = {'01': 'ein', '02': 'zwei', '03': 'drei', '04': 'vier', '05': 'fünf', '06': 'sechs',
               '07': 'sieben', '08': 'acht', '09': 'neun', '10': 'zehn', '11': 'elf', '12': 'zwölf',
               '13': 'dreizehn', '14': 'vierzehn', '15': 'fünfzehn', '16': 'sechzehn', '17': 'siebzehn',
               '18': 'achtzehn', '19': 'neunzehn', '20': 'zwanzig', '21': 'einundzwanzig', '22': 'zweiundzwanzig',
               '23': 'dreiundzwanzig', '24': 'vierundzwanzig'}

    if minute[0] == '0':

        mine = minute[1]

        if mine == '0':

            mine = ''

        else:

            mine = mine

    else:

        mine = minute

    day = tage.get(tag)

    month = Monate.get(str(monat))

    hour = Stunden.get(str(stunde))

    zeit_der_erinnerung = str(day) + ' ' + str(month) + ' um ' + str(hour) + ' Uhr ' + str(mine)

    reply = 'Alles klar, ich sage dir am ' + zeit_der_erinnerung + ' bescheid, ' 

    return reply

    







def handle(text, tiane, profile):

    if text != '_UNDO_':

        reply = ''

        Erinnerung = {}

        r = get_text(tiane, text)

        E_eins = {'Zeit': uhrzeit(tiane.analysis), 'Text': r, 'Benutzer': tiane.user}

        if 'Erinnerungen' in tiane.local_storage.keys():

            tiane.local_storage['Erinnerungen'].append(E_eins)

        else:

            tiane.local_storage['Erinnerungen'] = [E_eins]

        rep = get_reply(tiane, tiane.analysis)

        if 'dass ' in r:

            antwort = rep + r + '.'

        else:

            antwort = ' dass du ' + rep + r + ' musst.'

        tiane.say(antwort)

    else:

        liste = tiane.local_storage.get('Erinnerungen')

        element = liste[len(liste)]

        if element.get('Benutzer') == tiane.user:

            del liste[len(liste)]

        else:

            element = liste[len(liste) - 1]

            if element.get('Benutzer') == tiane.user:

                del liste[len(liste) - 1]

            else:

                element = liste[len(liste) - 2]

                if element.get('Benutzer') == tiane.user:

                    del liste[len(liste) - 2]

                else:

                    del liste[len(liste) - 3]

        

        



def isValid(text):
    text = text.lower()
    if 'erinner' in text or 'erinnere' in text:
        return True
    else:
        return False



class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': 'None', 'hour': 'None', 'year': 'None', 'minute': 'None', 'day': 'None'}, 'town': 'None'}


    def say(self, text):
        print (text)   



def main():
    profile = {}
    tiane = Tiane()
    handle('Erinner mich in 20 Minuten dass die Präsentation zu Ende ist', tiane, profile)
    

if __name__ == "__main__":
    main()
