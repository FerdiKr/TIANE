import datetime

SECURE = True

def get_text(tiane, txt):
    remembrall = ''
    e_ind = 0
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
    ausgabe = ausgabe.replace('ich', ('du'))
    ausgabe = ausgabe.replace('mich', ('dich'))
    if 'dass ' in text:
        lang = len(ausgabe)
        if ausgabe[(lang-1):] == ' ':
            ausgabe = ausgabe[:(lang-1)]
        l = len(ausgabe)
        if ausgabe[(l-2):] == 'st':
            ausgabe = ausgabe
        elif ausgabe[(l-1):] == 's':
            ausgabe = ausgabe + 't'
        else:
            ausgabe = ausgabe + 'st'
    return ausgabe



def get_reply_time(tiane, dicanalyse):
    time = dicanalyse.get('time')
    jahr = str(time['year'])
    monat = str(time['month'])
    tag = str(time['day'])
    stunde = str(time['hour'])
    minute = str(time['minute'])
    if int(minute) <= 9:
        minute = '0' + minute
    if int(monat) <= 9:
        monat = '0' + monat
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
    reply = zeit_der_erinnerung
    return reply



def handle(text, tiane, profile):
    if text != '_UNDO_':
        reply = ''
        Erinnerung = {}
        r = get_text(tiane, text)
        E_eins = {'Zeit': tiane.analysis['datetime'], 'Text': r, 'Benutzer': tiane.user}
        if 'Erinnerungen' in tiane.local_storage.keys():
            tiane.local_storage['Erinnerungen'].append(E_eins)
        else:
            tiane.local_storage['Erinnerungen'] = [E_eins]
        rep = get_reply_time(tiane, tiane.analysis)
        if 'dass ' in r:
            antwort = 'Alles klar, ich sage dir am ' + rep + ' bescheid, ' + r + '.' ###
        elif 'ans ' in text:
            antwort = 'Alles klar, ich erinnere dich am ' + rep + ' ans ' + r + '.'
        else:
            antwort = 'Alles klar, ich sage dir am ' + rep + ' bescheid, dass du ' + r + ' musst.'
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
    if 'erinner' in text or 'erinnere' in text:
        return True
    else:
        return False


class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'town': None, 'room': None, 'rooms': [None, 'Schlafzimmer'], 'datetime': datetime.datetime(2019, 8, 15, 19, 45, 6, 601174), 'time': {'day': 15, 'month': 8, 'year': 2019, 'hour': 19, 'minute': 45, 'second': 6}}

    def say(self, text):
        print (text)


def main():
    profile = {}
    tiane = Tiane()
    handle('Erinner mich in 3 Minuten ans Kuchen backen', tiane, profile)


if __name__ == "__main__":
    main()
