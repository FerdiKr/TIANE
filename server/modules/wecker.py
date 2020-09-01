import datetime

SECURE = True

def get_reply(tiane, dicanalyse):
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
    month = Monate.get(monat)
    hour = Stunden.get(stunde)
    zeit_des_weckers = str(day) + ' ' + str(month) + ' um ' + str(hour) + ' Uhr ' + str(mine) + '.'
    reply = 'Alles klar, ich wecke dich am ' + zeit_des_weckers
    return reply




def handle(text, tiane, profile):
    if text != '_UNDO_':
        Wecker = {}
        W_eins = {'Zeit': tiane.analysis['datetime'], 'Benutzer': tiane.user}
        if 'Wecker' in tiane.local_storage.keys():
            tiane.local_storage['Wecker'].append(W_eins)
        else:
            tiane.local_storage['Wecker'] = [W_eins]
        rep = get_reply(tiane, tiane.analysis)
        tiane.say(rep)
    else:
        liste = tiane.local_storage.get('Wecker')
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
    if 'weck ' in text or 'wecke' in text:
        return True

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
    handle('Bitte weck mich morgen um 11', tiane, profile)


if __name__ == "__main__":
    main()
