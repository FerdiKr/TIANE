#Tiane
#Spachselektion
import datetime

class Sentence_Analyzer:
    def __init__(self, room_list=[]):
        self.raumliste = room_list


    def get_text(self, eingabe):           #löscht falsches 'in'
        sonst = 'der dem den einer'
        satz = {}
        mind = 0
        falsches_in = 0
        i = str.split(eingabe)
        ind = 1
        for w in i:
            satz[ind] = w
            ind += 1
        for iindex, word in satz.items():
            if word in sonst:
                mind = mind + iindex
        for iindex, word in satz.items():
            if iindex == mind - 1:
                falsches_in = falsches_in + iindex
        if falsches_in >= 1:
            del satz[falsches_in]
        return satz


    def get_town(self, x): #checked
        satz = self.get_text(x)
        town = 'None'
        in_index = 0
        note = 'in'
        nope = 'der dem einem einer'
        if 'in ' not in x:
            if 'zu hause' in x or 'hier' in x:
                town = 'Weitersburg'
            else:
                town = 'None'
        else:
            for iindex, word in satz.items(): #findet Wort 'in''s key
                if word in note:
                    in_index = iindex
                    myind = in_index + 1
                    town = satz.get(myind)
                    if town in nope:
                        town = 'None'
        if town != 'None':
            try:
                if int(town) >= 1:
                    town = 'None'
            except TypeError:
                town = town
            except ValueError:
                town = town
        return town



    def get_room(self, text): #checked
        room = ''
        raum = str(self.raumliste)
        i = str.split(text)
        for r in raum:
            if r not in i:
                room = 'None'
        for w in i:
            if w in raum and len(w) >= 3:
                room = w
        return room


    def get_month_abs(self, text): #checked
        now = datetime.datetime.now()
        text = text.lower()
        month = 'None'
        if 'am ' not in text:
            month = 'None'
        else:
            Monate = {1: 'januar', 2: 'februar', 3: 'märz', 4: 'april', 5: 'mai', 6: 'juni',
                      7: 'juli', 8: 'august', 9: 'september', 10: 'oktober', 11: 'november',
                      12: 'dezember'}
            satz = self.get_text(text)
            for i, w in Monate.items():
                if w in text:
                    m = w
                    month = i
                    if month <= 9:
                        month = '0' + str(month)
                    else:
                        month = str(month)
                    break
            if month == 'None':
                for i, w in satz.items():
                    if w == 'am':
                        amindex = i
                        tagindex = i + 1
                        tag = satz.get(tagindex)
                        lange = len(tag)
                        nur_ende = lange - 1
                        if tag[nur_ende] == '.':
                            month = 'None'
                            break
                        else:
                            monat = tag[2:]
                            if monat != '.':
                                try:
                                    if int(monat) >= 1:
                                        try:
                                            if int(monat) >= 1:
                                                month = int(monat)
                                        except TypeError:
                                            monat_zwei = monat[1:]
                                except ValueError:
                                    monat_zwei = monat[1:]
                                try:
                                    if int(monat_zwei) >= 1:
                                        try:
                                            if int(monat_zwei) >= 1:
                                                month = int(monat_zwei)
                                        except TypeError:
                                            month = month
                                except ValueError:
                                    month = 'None'
                                if month != 'None':
                                    if month <= 9:
                                        month = '0' + str(month)
                                    else:
                                        month = str(month)
        return month



    def get_day_abs(self, text): #checked
        text = text.lower()
        day = 'None'
        if 'am ' not in text:
            day = 'None'
        else:
            tage = {1: 'ersten', 2: 'zweiten', 3: 'dritten', 4: 'vierten', 5: 'fünften',
                    6: 'sechsten', 7: 'siebten', 8: 'achten', 9: 'neunten', 10: 'zehnten',
                    11: 'elften', 12: 'zwölften', 13: 'dreizehnten', 14: 'vierzehnten', 15: 'fünfzehnten',
                    16: 'sechzehnten', 17: 'siebzehnten', 18: 'achtzehnten', 19: 'neunzehnten', 20: 'zwanzigsten',
                    21: 'einundzwanzigsten', 22: 'zweiundzwanzigsten', 23: 'dreiundzwanzigsten', 24: 'vierundzwanzigsten',
                    25: 'fünfundzwanzigsten', 26: 'sechsundzwanzigsten', 27: 'siebenundzwanzigsten', 28: 'achtundzwanzigsten',
                    29: 'neunundzwanzigsten', 30: 'dreißigsten', 31: 'einunddreißigsten', 32: 'zweiunddreißigsten'}
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'am':
                    am_index = ind
                    day_index = ind + 1
                    dayy = satz.get(day_index)
                    if dayy in tage.values():
                        for ind, w in tage.items():
                            if w == dayy:
                                day = ind
                                if day <= 9:
                                    day = '0' + str(day)
                                else:
                                    day = str(day)
                    else:
                        try:
                            if int(dayy) >= 1:
                                tag = int(dayy)
                        except ValueError:
                            tag = dayy[0:2]
                            try:
                                if int(tag) >= 1:
                                    tag = int(tag)
                            except ValueError:
                                tag = tag[0]
                                try:
                                    if int(tag) >= 1:
                                        tag = int(tag)
                                except ValueError:
                                    tag = 'None'
                                    break
                        if tag <= 9:
                            day = '0' + str(tag)
                        else:
                            day = str(tag)
        return day

    def get_year_abs(self, text): #checked
        text = text.lower()
        satz = self.get_text(text)
        year = 'None'
        if 'am ' not in text:
            year = 'None'
        else:
            for ind, word in satz.items():
                if word == 'am':
                    am_index = ind
                    year_index = ind + 3
                    if year_index in satz.keys():
                        year = satz.get(year_index)
                        try:
                            if int(year) >= 1000:
                                year = str(year)
                        except ValueError:
                            year = 'None'
                    else:
                        year_index = ind + 2
                        if year_index in satz.keys():
                            year = satz.get(year_index)
                            try:
                                if int(year) >= 1000:
                                    year = str(year)
                            except ValueError:
                                year = 'None'
        return year

    def get_hour_abs(self, text): #checked
        hour = ''
        text = text.lower()
        satz = self.get_text(text)
        if 'um ' not in text:
            hour = 'None'
        else:
            for ind, word in satz.items():
                if word == 'um':
                    um_index = ind
                    hour_index = ind + 1
                    hour = satz.get(hour_index)
                    if len(hour) <= 2:
                        try:
                            if int(hour) <= 23 and int(hour) >= 0:
                                hour = int(hour)
                        except ValueError:
                            hour = default
                        if hour >= 0 and hour <= 23:
                            hour = str(hour)
                            if len(hour) <= 1:
                                hour = '0' + hour
                    else:
                        ho = hour[0]
                        ur = hour[1]
                        try:
                            if int(ur) <= 9 and int(ur) >= 0:
                                hour = ho + ur
                        except ValueError:
                            hour = '0' + ho
        if hour != 'None' and hour != '12':
            if ' abend' in text or ' nachmittag' in text:
                stunde = int(hour) + 12
                hour = str(stunde)
        return hour

    def get_minute_abs(self, text): #checked
        minute = '00'
        text = text.lower()
        satz = self.get_text(text)
        if 'um ' not in text:
            minute = 'None'
        else:
            for ind, word in satz.items():
                if word == 'um':
                    um_index = ind
                    minute1_index = ind + 3
                    mi = satz.get(minute1_index)
                    if len(satz)<= minute1_index + 1:
                        try:
                            if int(mi) <= 59 and int(mi) >= 0:
                                minute = mi
                        except TypeError:
                            for ind, word in satz.items():
                                if word == 'um':
                                    um_iindex = ind
                                    uhr_index = um_iindex + 1
                                    uhr = satz.get(uhr_index)
                                    lang = len(uhr)
                                    if lang >= 2:
                                        mi = uhr[lang - 2]
                                        nute = uhr[lang - 1]
                                        minute = mi + nute
                    else:
                        try:
                            if int(mi) <= 59 and int(mi) >= 0:
                                minute = mi
                        except ValueError:
                            for ind, word in satz.items():
                                if word == 'um':
                                    um_iindex = ind
                                    uhr_index = um_iindex + 1
                                    uhr = satz.get(uhr_index)
                                    lang = len(uhr)
                                    if lang >= 2:
                                        mi = uhr[lang - 2]
                                        nute = uhr[lang - 1]
                                        minute = mi + nute
            if int(minute) <= 9:
                minute = '0' + minute
            else:
                minute = str(minute)
            if len(minute) >= 3:
                minute = minute[1:]
        return minute


    def get_year_rel(self, text): #checked
        text = text.lower()
        now = datetime.datetime.now()
        year = now.year
        if 'übernächstes jahr' in text:
            year = year + 2
        elif 'nächstes jahr' in text:
            year = year + 1
        elif 'in' in text and 'jahren' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'jahren':
                    j_index = ind
                    myind = j_index - 1
                    year = now.year
                    y = satz.get(myind)
                    try:
                        if int(y) >= 1:
                            year = year + int(y)
                    except TypeError:
                        year = year

        else:
            s = str.split(text)
            for w in s:
                try:
                    if int(w) >= 1000:
                        year = w
                except ValueError:
                    year = year
        jahr = str(year)
        return jahr


    def get_month_rel(self, text): #checked
        text = text.lower()
        now = datetime.datetime.now()
        month = now.month
        if 'monaten' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'monaten':
                    m_index = ind
                    myind = m_index - 1
                    add_monat = satz.get(myind)
                    try:
                        if int(add_monat) <= 12:
                            month = now.month
                            month = month + int(add_monat)
                    except TypeError:
                        month = month
        elif 'übernächsten monat' in text:
            month = now.month + 2
        elif 'nächsten monat' in text:
            month = now.month + 1
        elif 'in einem monat' in text:
            month = now.month + 1
        else:
            month = 0
        if int(month) <= 9:
            month = '0' + str(month)
        else:
            month = str(month)
        if month == '00':
            month = 'None'
        return month

    def get_wochentag_rel(self, text): #checked, but subject to change
        now = datetime.datetime.now()
        wochentag = datetime.datetime.today().weekday()
        text = text.lower()
        t = 0
        if 'übernächste woche' in text or 'übernächsten' in text:
            if 'montag' in text:
                t = 7 - wochentag
            elif 'dienstag' in text:
                if wochentag <= 0:
                    t = 1 - wochentag
                else:
                    t = 8 - wochentag
            elif 'mittwoch' in text:
                if wochentag <= 1:
                    t = 2 - wochentag
                else:
                    t = 9 - wochentag
            elif 'donnerstag' in text:
                if wochentag <= 2:
                    t = 3 - wochentag
                else:
                    t = 10 - wochentag
            elif 'freitag' in text:
                if wochentag <= 3:
                    t = 4 - wochentag
                else:
                    t = 11 - wochentag
            elif 'samstag' in text:
                if wochentag <= 4:
                    t = 5 - wochentag
                else:
                    t = 12 - wochentag
            elif 'sonntag' in text:
                if wochentag <= 5:
                    t = 6 - wochentag
                else:
                    t = 13 - wochentag
            day = now.day + t + 7 #/+14
        elif 'nächste woche' in text or 'nächsten' in text:
            if 'montag' in text:
                t = 7 - wochentag
            elif 'dienstag' in text:
                if wochentag <= 0:
                    t = 1 - wochentag
                else:
                    t = 8 - wochentag
            elif 'mittwoch' in text:
                if wochentag <= 1:
                    t = 2 - wochentag
                else:
                    t = 9 - wochentag
            elif 'donnerstag' in text:
                if wochentag <= 2:
                    t = 3 - wochentag
                else:
                    t = 10 - wochentag
            elif 'freitag' in text:
                if wochentag <= 3:
                    t = 4 - wochentag
                else:
                    t = 11 - wochentag
            elif 'samstag' in text:
                if wochentag <= 4:
                    t = 5 - wochentag
                else:
                    t = 12 - wochentag
            elif 'sonntag' in text:
                if wochentag <= 5:
                    t = 6 - wochentag
                else:
                    t = 13 - wochentag
            day = now.day + t #+7
        else:
            if 'montag' in text:
                t = 7 - wochentag
            elif 'dienstag' in text:
                if wochentag <= 0:
                    t = 1 - wochentag
                else:
                    t = 8 - wochentag
            elif 'mittwoch' in text:
                if wochentag <= 1:
                    t = 2 - wochentag
                else:
                    t = 9 - wochentag
            elif 'donnerstag' in text:
                if wochentag <= 2:
                    t = 3 - wochentag
                else:
                    t = 10 - wochentag
            elif 'freitag' in text:
                if wochentag <= 3:
                    t = 4 - wochentag
                else:
                    t = 11 - wochentag
            elif 'samstag' in text:
                if wochentag <= 4:
                    t = 5 - wochentag
                else:
                    t = 12 - wochentag
            elif 'sonntag' in text:
                if wochentag <= 5:
                    t = 6 - wochentag
                else:
                    t = 13 - wochentag
            day = now.day + t
        if day <= 9:
            day = '0' + str(day)
        else:
            day = str(day)
        return day

    def get_day_rel(self, text): #checked    #incl. get_wochentag_rel()
        day = 'None'
        text = text.lower()
        now = datetime.datetime.now()
        day = now.day
        wochentag = datetime.datetime.today().weekday()
        if 'übermorgen in' in text and 'woche' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'woche' or word == 'wochen':
                    w_ind = ind
                    myind = w_ind - 1
                    w = satz.get(myind)
                    try:
                        if int(w) >= 1:
                            day = day + int(w) * 7 + 2
                    except TypeError:
                        day = day
        elif 'morgen in' in text and 'woche' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'woche' or word == 'wochen':
                    w_ind = ind
                    myind = w_ind - 1
                    w = satz.get(myind)
                    try:
                        if int(w) >= 1:
                            day = day + int(w) * 7 + 1
                    except TypeError:
                        day = day
        elif 'übermorgen' in text:
            day = now.day + 2
        elif ' morgen' in text:
            day = now.day + 1
        elif 'übernächstes wochenende' in text:
            w = 5 - wochentag
            day = now.day + w + 14
        elif 'nächstes wochenende' in text:
            w = 5 - wochentag
            day = now.day + w + 7
        elif 'am wochenende' in text or 'dieses wochenende' in text:
            w = 5 - wochentag
            day = now.day + w
        elif 'montag' or 'dienstag' or 'mittwoch' or 'donnerstag' or 'freitag' or 'samstag' or 'sonntag' in text:
            day = self.get_wochentag_rel(text)
        day = int(day)
        if day >= 29:
            if now.month == 2 and now.year % 4 != 0:
                t = day - 28
                if t >= 32:
                    u = t - 31
                    day = u
                else:
                    day = t
            elif now.month == 2 and now.year % 4 == 0:
                if day >= 30:
                    t = day - 29
                    if t >= 32:
                        u = t - 31
                        day = u
                    else:
                        day = t
            elif now.month == 1 or now.month == 3 or now.month == 5 or now.month == 8 or now.month == 10:
                if day >= 32:
                    t = day - 31
                    if t >= 31:
                        u = t - 30
                        day = u
                    else:
                        day = t
            elif now.month == 7 or now.month == 12:
                if day >= 32:
                    t = day - 31
                    if t >= 32:
                        u = t - 31
                        day = u
                    else:
                        day = t
            else:
                if day >= 31:
                    t = day - 30
                    if t >= 32:
                        u = t - 31
                        day = u
                    else:
                        day = t
        if day <= 9:
            day = '0' + str(day)
        else:
            day = str(day)
        return day

    def getmonth_fromday(self, text):
        text = text.lower()
        now = datetime.datetime.now()
        m = now.month
        day = now.day
        wochentag = datetime.datetime.today().weekday()
        if 'übermorgen in' in text and 'woche' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'woche' or word == 'wochen':
                    w_ind = ind
                    myind = w_ind - 1
                    w = satz.get(myind)
                    try:
                        if int(w) >= 1:
                            day = day + int(w) * 7 + 2
                    except TypeError:
                        day = day
        elif 'morgen in' in text and 'woche' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'woche' or word == 'wochen':
                    w_ind = ind
                    myind = w_ind - 1
                    w = satz.get(myind)
                    try:
                        if int(w) >= 1:
                            day = day + int(w) * 7 + 1
                    except TypeError:
                        day = day
        elif 'übermorgen' in text:
            day = now.day + 2
        elif 'morgen' in text:
            day = now.day + 1
        elif 'übernächstes wochenende' in text:
            w = 5 - wochentag
            day = now.day + w + 14
        elif 'nächstes wochenende' in text:
            w = 5 - wochentag
            day = now.day + w + 7
        elif 'am wochenende' in text or 'dieses wochenende' in text:
            w = 5 - wochentag
            day = now.day + w
        elif 'montag' or 'dienstag' or 'mittwoch' or 'donnerstag' or 'freitag' or 'samstag' or 'sonntag' in text:
            day = self.get_wochentag_rel(text)
        if int(day) >= 29:
            if now.month == 2 and now.year % 4 != 0:
                t = day - 28
                m = now.month + 1
                if t >= 32:
                    m = now.month + 2
                else:
                    m = m
            elif now.month == 2 and now.year % 4 == 0:
                if day >= 30:
                    t = day - 29
                    m = now.month + 1
                    if t >= 32:
                        m = now.month + 2
                    else:
                        m = m
            elif now.month == 1 or 3 or 5 or 8 or 10:
                if day >= 32:
                    t = day - 31
                    m = now.month + 1
                    if t >= 31:
                        m = now.month + 2
                    else:
                        m = m
            elif now.month == 7 or 12:
                if day >= 32:
                    t = day - 31
                    m = now.month + 1
                    if t >= 32:
                        m = now.month + 2
                    else:
                        m = m
            else:
                if day >= 31:
                    t = day - 30
                    m = now.month + 1
                    if t >= 32:
                        m = now.month + 2
                    else:
                        m = m
        month = m
        if month <= 9:
            month = '0' + str(month)
        else:
            month = str(month)

        if month == '00':
            month = 'None'
        return month









    def analyze(self, text):
        r = self.get_room(text) #checked
        t = self.get_town(text) #checked
        m = self.get_month_abs(text) #checked
        if m == 'None':
            m = self.get_month_rel(text) #checked
            if m == 'None':
                m = self.getmonth_fromday(text) #checked
        d = self.get_day_abs(text) #checked
        if d == 'None':
            d = self.get_day_rel(text) #checked      #incl. self.get_wochentag_rel(text)
        y = self.get_year_abs(text) #checked
        if y == 'None':
            y = self.get_year_rel(text) #checked
        h = self.get_hour_abs(text) #checked
        mi = self.get_minute_abs(text) #checked
        dic = {}
        dic['town'] = t
        dic['room'] = r
        dic['time'] = ti_dic = {}
        ti_dic['month'] = m
        ti_dic['day'] = d
        ti_dic['year'] = y
        ti_dic['hour'] = h
        ti_dic['minute'] = mi
        return dic


def main():
    Analyzer = Sentence_Analyzer(room_list=['Küche', 'Wohnzimmer', 'Bad'])
    eingabe = 'Erinner mich morgen Nachmittag um 3'
    print (Analyzer.analyze(eingabe))

if __name__ == '__main__':
    main()
