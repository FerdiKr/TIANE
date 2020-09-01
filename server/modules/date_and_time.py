import datetime
import random

SECURE = True

def get_time(i):
    now = datetime.datetime.now()
    stunde = now.hour
    nächste_stunde = now.hour + 1
    if nächste_stunde == 24:
        nächste_stunde = 0
    minute = now.minute
    stunde = str(stunde)
    minute = str(minute)
    if minute == 0:
        ausgabe = 'Es ist ' + stunde + ' Uhr.'
    elif minute == 5:
        ausgabe = 'Es ist fünf nach ' + stunde + '.'
    elif minute == 10:
        ausgabe = 'Es ist zehn nach ' + stunde + '.'
    elif minute == 15:
        ausgabe = 'Es ist viertel nach ' + stunde + '.'
    elif minute == 20:
        ausgabe = 'Es ist zwanzig nach ' + stunde + '.'
    elif minute == 25:
        ausgabe = 'Es ist fünf vor halb ' + stunde + '.'
    elif minute == 30:
        ausgabe = 'Es ist halb ' + nächste_stunde + '.'
    elif minute == 35:
        ausgabe = 'Es ist fünf nach halb ' + nächste_stunde + '.'
    elif minute == 40:
        ausgabe = 'Es ist zwanzig vor ' + nächste_stunde + '.'
    elif minute == 45:
        ausgabe = 'Es ist viertel vor ' + nächste_stunde + '.'
    elif minute == 50:
        ausgabe = 'Es ist zehn vor ' + nächste_stunde + '.'
    elif minute == 55:
        ausgabe = 'Es ist fünf vor ' + nächste_stunde + '.'
    else:
        ausgabe = 'Es ist ' + stunde + ' Uhr ' + minute + '.'
    return ausgabe

def get_day(i):
    now = datetime.datetime.now()
    wochentag = datetime.datetime.today().weekday()
    tage = {0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'}
    nummern = {1: 'erste', 2: 'zweite', 3: 'dritte', 4: 'vierte', 5: 'fünfte',
                6: 'sechste', 7: 'siebte', 8: 'achte', 9: 'neunte', 10: 'zehnte',
                11: 'elfte', 12: 'zwölfte', 13: 'dreizehnte', 14: 'vierzehnte', 15: 'fünfzehnte',
                16: 'sechzehnte', 17: 'siebzehnte', 18: 'achtzehnte', 19: 'neunzehnte', 20: 'zwanzigste',
                21: 'einundzwanzigste', 22: 'zweiundzwanzigste', 23: 'dreiundzwanzigste', 24: 'vierundzwanzigste',
                25: 'fünfundzwanzigste', 26: 'sechsundzwanzigste', 27: 'siebenundzwanzigste', 28: 'achtundzwanzigste',
                29: 'neunundzwanzigste', 30: 'dreißigste', 31: 'einunddreißigste', 32: 'zweiunddreißigste'}
    ausgabe = 'Heute ist ' + tage.get(wochentag) + ' der ' + nummern.get(now.day) + ' ' + nummern.get(now.month) + '.'
    return ausgabe



def handle(txt, tiane, profile):
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
    now = datetime.datetime.now()
    wochentag = datetime.datetime.today().weekday()
    uhrzeit = now.hour
    if 'uhr' in text or 'spät' in text or 'uhrzeit' in text:
        tiane.say(get_time(text))
    elif 'welchen tag' in text or 'welcher tag' in text or 'wochentag' in text or 'datum' in text or 'den wievielten haben wir heute' in text or 'der wievielte ist es' in text:
        tiane.say(get_day(text))
    elif 'hallo' in text:
        tiane.say('Hallo, {}!'.format(tiane.user))
    elif uhrzeit >= 19 and uhrzeit <= 23:
        if 'guten morgen' in text:
            tiane.say('Bist du etwa gerade erst aufgewacht?')
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            if 'ja' in antwort_eins or 'warum nicht' in text or 'ich war müde' in antwort_eins or 'ich war halt müde' in antwort_eins or 'jetzt bin ich ja wach' in antwort_eins or 'jetzt bin ich jedenfalls wach' in antwort_eins:
                tiane.say('Du solltest wirklich nachts schlafen, sonst bringst du noch deinen Schlafrhytmus durcheinander!')
            else:
                tiane.say('In Ordnung.')
        elif 'guten abend' in text:
            tiane.say('Guten Abend, {}. Hast du heute noch was vor?'.format(tiane.user))
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            if 'TIMEOUT_OR_INVALID' in antwort_eins:
                tiane.say('Ich konnte deine Pläne leider nicht verstehen.')
            elif 'nein' in antwort_eins or 'nicht wirklich' in antwort_eins or 'ich bleibe lieber' in antwort_eins or 'ich habe nichts' in antwort_eins:
                tiane.say('Dann genieße den freien Abend!')
            else:
                tiane.say('Das klingt toll! Ich wünsche dir viel Spaß dabei!')
        elif 'guten tag' in text:
            tiane.say('Guten Tag, {}'.format(tiane.user))
        elif 'gute nacht' in text:
            tiane.say('Soll ich dich morgen wecken?')
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            if 'TIMEOUT_OR_INVALID' in antwort_eins:
                tiane.say('Ich fürchte, ich habe dich nicht ganz verstanden. Soll ich dich morgen früh wecken?')
                antwort_zwei = tiane.listen()
                antwort_zwei = tiane_zwei.lower()
                if 'ja' in antwort_zwei or 'weck mich' in antwort_zwei or 'wecke mich' in antwort_zwei or 'ich mÃ¶chte um' in antwort_zwei or 'ich will um' in antwort_zwei or 'bitte um' in antwort_zwei:
                    tiane.start_module(text=antwort_zwei)
                elif 'nein' in antwort_zwei or 'nicht' in antwort_zwei:
                    tiane.say('In Ordnung. Schlaf gut, {}'.format(tiane.user))
                else:
                    tiane.say('Ich konnte dich leider nicht verstehen. Du bist wohl schon zu müde.')
            elif 'ja' in antwort_eins or 'weck mich' in antwort_eins or 'wecke mich' in antwort_eins or 'ich möchte um' in antwort_eins or 'ich will um' in antwort_eins or 'bitte um' in antwort_eins:
                tiane.start_module(text=antwort_eins)
            elif 'nein' in antwort_eins or 'nicht' in antwort_eins:
                tiane.say('In Ordnung. Schlaf gut, {}'.format(tiane.user))
            else:
                tiane.say('Ich konnte dich leider nicht verstehen. Du bist wohl schon zu müde.')
    elif uhrzeit >= 5 and uhrzeit <= 10:
        if 'guten morgen' in text or 'guten tag' in text:
            tiane.say('Guten Morgen, {}. Hast du gut geschlafen?'.format(tiane.user))
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            if 'ja' in antwort_eins or 'ich habe gut' in antwort_eins or 'das habe ich' in antwort_eins:
                tiane.say('Das freut mich! Kann ich etwas für dich tun?')
                antwort_zwei = tiane.listen()
                antwort_zwei = antwort_zwei.lower()
                tiane.start_module(text=antwort_zwei)
                if 'wie viel uhr ist es' in antwort_zwei or 'wie spät ist es' in antwort_zwei:
                    tiane.say(get_time(antwort_eins))
            else:
                tiane.say('Ich hoffe, du bist nicht allzu müde.')
        elif 'guten abend' in text or 'gute nacht' in text:
            tiane.say('Hast du etwa noch nicht geschlafen?')
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            if 'nein' in antwort_eins or 'ich hatte besseres zu tun' in antwort_eins or 'ich bin nicht dazu gekommen' in antwort_eins or 'ich bin noch nicht dazu gekommen' in antwort_eins or 'ich bin zu beschäftigt' in antwort_eins or 'schlaf ist für die schwachen' in antwort_eins:
                tiane.say('Du solltest wirklich ins Bett gehen! 23 Stunden ohne Schlaf sind nicht gut für deinen Körper!')
            else:
                tiane.say('Ich konnte dich leider nicht verstehen. Du bist wohl noch zu müde.')
    elif uhrzeit >= 0 and uhrzeit <= 4:
        if 'guten morgen' in text or 'guten tag' in text:
            tiane.say('Schlaf ruhig weiter, es ist noch mitten in der Nacht!')
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            antwort = antwort_eins.replace('aber', (''))
            if 'ich bin wach' in antwort or 'etwas vor' in antwort or 'muss los' in antwort or 'müssen los' in antwort or 'jetzt stehe ich auf' in antwort or 'egal' in antwort:
                tiane.say('Alles klar! Wie wäre es mit Kaffee oder Tee?')
                antwort_zwei = tiane.listen()
                antwort_zwei = antwort_zwei.lower()
                if 'ja' in antwort_zwei or 'gerne' in antwort_zwei or 'wäre jetzt gut' in antwort_zwei or 'warum nicht' in antwort_zwei:
                    tiane.say('Wenn endlich mal jemand ein Kaffeemaschienen Modul programmieren würde, würde ich dir jetzt sehr gerne Kaffee kochen.') #Das ist gut, er wird dich aufwecken. (Vielleicht ist HTCPCP ja doch für was gut xD)
                elif 'nein' in antwort_zwei or 'nicht' in antwort_zwei:
                    tiane.say('In Ordnung')
                else:
                    tiane.say('Ich konnte dich leider nicht verstehen. Du bist wohl schon zu müde.')
        elif 'gute nacht' in text:
            tiane.say('Hast du etwa noch nicht geschlafen?')
            antwort_eins = tiane.listen()
            antwort_eins = antwort_eins.lower()
            if 'nein' in antwort_eins or 'ich hatte besseres zu tun' in antwort_eins or 'ich bin nicht dazu gekommen' in antwort_eins or 'ich bin noch nicht dazu gekommen' in antwort_eins or 'ich bin zu beschÃ¤ftigt' in antwort_eins or 'schlaf ist fÃ¼r die schwachen' in antwort_eins:
                tiane.say('Du solltest wirklich ins Bett gehen! 23 Stunden ohne Schlaf sind nicht gut für deinen Körper!')
            else:
                tiane.say('Ich konnte dich leider nicht verstehen. Du bist wohl schon zu müde.')
        elif 'guten abend' in text:
            tiane.say('Ob es noch Abend ist, liegt wohl im Blickwinkel des Betrachters. In Amerika ist es jetzt in der Tat Abend.')
    elif uhrzeit >= 14 and uhrzeit <= 18:
        if 'guten morgen' in text or 'guten tag' in text:
            tiane.say('Guten Tag, {}'.format(tiane.user))
        elif 'gute nacht' in text:
            tiane.say('Willst du etwa schon schlafen gehen, {}?'.format(tiane.user))
            antwort_zwei = tiane.listen()
            a_z = antwort_zwei.lower()
            if 'ja' in a_z or 'warum nicht' in a_z or 'klar' in a_z:
                tiane.say('Dann schlaf gut, aber vergiss nicht, auch wieder aufzuwachen!')
            elif 'nein' in a_z or 'noch nicht' in a_z or 'natürlich nicht' in a_z:
                tiane.say('Alles klar, dann wünsche ich dir noch einen schönen Abend!')
            else:
                tiane.say('Ich konnte dich leider nicht verstehen. Du bist wohl doch schon zu müde.')
        elif 'guten abend' in text:
            tiane.say('Ob es schon Abend ist, liegt wohl im Blickwinkel des Betrachters. Ich würde sagen, es ist gerade eher Nachmittag.')
    elif uhrzeit >= 11 and uhrzeit <= 13:
        if 'guten morgen' in text or 'guten tag' in text:
            tiane.say('Guten Tag, {}'.format(tiane.user))
        elif 'gute nacht' in text:
            tiane.say('Willst du etwa schon schlafen gehen, {}?'.format(tiane.user))
            antwort_zwei = tiane.listen()
            a_z = antwort_zwei.lower()
            if 'ja' in a_z or 'warum nicht' in a_z or 'klar' in a_z:
                tiane.say('Du solltest wirklich nachts schlafen, sonst bringst du noch deinen Schlafrhytmus durcheinander!')
            elif 'nein' in a_z or 'noch nicht' in a_z or 'natürlich nicht' in a_z:
                tiane.say('Alles klar, dann wünsche ich dir noch einen schönen Tag!')
            else:
                tiane.say('Ich konnte dich leider nicht verstehen, {}.'.format(tiane.user))
        elif 'guten abend' in text:
            tiane.say('Ob es schon Abend ist, liegt wohl im Blickwinkel des Betrachters. In Asien ist es jetzt in der Tat Abend.')
    else:
        tiane.say('Guten Tag, {}'.format(tiane.user))






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
    if 'guten abend' in text or 'uhrzeit' in text or 'guten morgen' in text or 'gute nacht' in text or 'welches datum' in text or 'wie spät' in text or 'wie viel uhr' in text or 'wochentag' in text or 'welcher tag' in text or 'welchen tag' in text or 'guten tag' in text:
        return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '10', 'hour': '19', 'year': '2018', 'minute': '47', 'day': '19'}, 'town': 'None'}

    def say(self, text):
        print(text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Guten Morgen', tiane, profile)

if __name__ == '__main__':
    main()
