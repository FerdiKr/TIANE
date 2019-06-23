import datetime

class Sentence_Analyzer:
    def __init__(self, room_list=[], default_location=''):
        self.raumliste = room_list
        self.default_location = default_location


    def get_text(self, eingabe):
        sonst = 'der dem den einer'
        tt = eingabe.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        satz = {}
        mind = 0
        falsches_in = 0
        i = str.split(tt)
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


    def get_town(self, x):
        satz = self.get_text(x)
        town = 'None'
        in_index = 0
        nope = 'der dem einem einer drei zwei vier fünf sechs sieben acht neun zehn Der Dem Einem Einer Drei Zwei Vier Fünf Sechs Sieben Acht Neun Zehn 1 2 3 4 5 6 7 8 9 10'
        two_words = 'los new old bad ober unter west ost nord süd south north east Los New Old Bad Ober Unter West Ost Nord Süd South North East'
        if 'in ' not in x:
            if 'zu hause' in x or 'hier' in x:
                if not self.default_location == '':
                    town = self.default_location
                else:
                    town = 'None'
            else:
                town = 'None'
        else:
            for iindex, word in satz.items():
                if word == 'in':
                    in_index = iindex
                    town_ind = in_index + 1
                    town = satz.get(town_ind)
                    if town in two_words:
                        try:
                            second_word = satz.get(town_ind + 1)
                            town = town + ' ' + second_word
                        except KeyError:
                            town = town


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



    def get_room(self, text):
        room = ''
        raum = str(self.raumliste)
        tt = text.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        i = str.split(tt)
        for r in raum:
            if r not in i:
                room = 'None'
        for w in i:
            if w in raum and len(w) >= 3:
                room = w
        return room


    def get_month_abs(self, txt):
        now = datetime.datetime.now()
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
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
                        if tagindex in satz.keys():
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
                        else:
                            month = 'None'
        return month

    def get_month_by_name(self, txt):
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
        month = 'None'
        Monate = {'januar': '01', 'februar': '02', 'märz': '03', 'april': '04', 'mai': '05', 'juni': '06',
                  'juli': '07', 'august': '08', 'september': '09', 'oktober': '10', 'november': '11', 'dezember': '12'}
        s = str.split(text)
        x = ''
        for w in s:
            if w in Monate.keys():
                x = w
                month = Monate.get(x)
                break
        day = 'None'
        mind = 0
        if month != 'None':
            satz = {}
            i = str.split(text)
            ind = 1
            for w in i:
                satz[ind] = w
                ind += 1
            for iindex, word in satz.items():
                if word == x:
                    mind = iindex - 1
            if mind >= 1:
                try:
                    day = satz.get(mind)
                except ValueError:
                    day = 'None'
        if day != 'None':
            tage = {1: 'ersten', 2: 'zweiten', 3: 'dritten', 4: 'vierten', 5: 'fünften',
                    6: 'sechsten', 7: 'siebten', 8: 'achten', 9: 'neunten', 10: 'zehnten',
                    11: 'elften', 12: 'zwölften', 13: 'dreizehnten', 14: 'vierzehnten', 15: 'fünfzehnten',
                    16: 'sechzehnten', 17: 'siebzehnten', 18: 'achtzehnten', 19: 'neunzehnten', 20: 'zwanzigsten',
                    21: 'einundzwanzigsten', 22: 'zweiundzwanzigsten', 23: 'dreiundzwanzigsten', 24: 'vierundzwanzigsten',
                    25: 'fünfundzwanzigsten', 26: 'sechsundzwanzigsten', 27: 'siebenundzwanzigsten', 28: 'achtundzwanzigsten',
                    29: 'neunundzwanzigsten', 30: 'dreißigsten', 31: 'einunddreißigsten', 32: 'zweiunddreißigsten'}
            for i, w in tage.items():
                if day == w:
                    day = i
                    break
            day = int(day)
            if day <= 9:
                day = '0' + str(day)
            else:
                day = str(day)
        m_and_d = [month, day]
        return m_and_d


    def get_day_abs(self, txt):
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
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
                    if day_index in satz.keys():
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

    def get_year_abs(self, text):
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

    def get_hour_abs(self, text):
        hour = ''
        text = text.lower()
        satz = self.get_text(text)
        if 'um ' not in text and 'uhr ' not in text:
            hour = 'None'
        elif 'um ' in text:
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
        elif 'uhr ' in text:
            for ind, word in satz.items():
                if word == 'uhr':
                    uhr_index = ind
                    hour_index = ind - 1
                    minute_index = ind + 1
                    hour = satz.get(hour_index)
                    minute = satz.get(minute_index)
                    if len(hour) <= 2 and len(minute) <= 2:
                        try:
                            if int(hour) <= 23 and int(hour) >= 0:
                                hour = int(hour)
                                break
                        except ValueError:
                            hour = default
                        if hour >= 0 and hour <= 23:
                            hour = str(hour)
                            if len(hour) <= 1:
                                hour = '0' + hour
                    elif len(hour) <= 2:
                        try:
                            minute = int(hour)
                        except ValueError:
                            minute = 'None' ###################
        if hour != 'None' and hour != '12':
            if ' abend' in text or ' nachmittag' in text:
                stunde = int(hour) + 12
                hour = str(stunde)
        return hour

    def get_minute_abs(self, text):
        minute = '00'
        text = text.lower()
        satz = self.get_text(text)
        if 'um ' not in text and 'uhr' not in text:
            minute = 'None'
        elif 'um ' in text:
            for ind, word in satz.items():
                if word == 'um':
                    um_index = ind
                    minute1_index = ind + 3
                    mi = satz.get(minute1_index)
                    if len(satz)<= minute1_index + 1:
                        try:
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
                                        if lang >= 3:
                                            mi = uhr[lang - 2]
                                            nute = uhr[lang - 1]
                                            minute = mi + nute
                        except ValueError:
                            minute = 0
                    else:
                        try:
                            try:
                                if int(mi) <= 59 and int(mi) >= 0:
                                    minute = mi
                                    break
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
                        except TypeError:
                            minute = 0
        elif 'uhr' in text:
            f = False
            for i, w in satz.items():
                if w == 'uhr':
                    uhr_index = i
                    m_index = i + 1
                    try:
                        minu = satz.get(m_index)
                        try:
                            if int(minu) <= 59 and int(minu) >= 0:
                                minute = minu
                                break
                        except TypeError:
                            minute = 'None'
                            break
                    except TypeError:
                        minu = 'None'
                        satz1 = satz.remove(uhr_index)
                        f = True
                        break
            if f == True:
                for i, w in satz1.items():
                    if w == 'uhr':
                        uhr_index = i
                        m_index = i + 1
                        try:
                            minu = satz.get(m_index)
                            try:
                                if int(minu) <= 59 and int(minu) >= 0:
                                    minute = minu
                                    break
                            except TypeError:
                                minute = 'None'
                                break
                        except TypeError:
                            minute = 'None'
                            break
        if minute != 'None':
            if int(minute) <= 9:
                minute = '0' + str(minute)
            else:
                minute = str(minute)
            if len(minute) >= 3:
                minute = minute[1:]
        return minute


    def get_minute_rel(self, text):
        text = text.lower()
        now = datetime.datetime.now()
        satz = self.get_text(text)
        minute = '01'
        zeit = 0
        if 'in einer minute' in text:
            minute = now.minute + 1
        elif ' in ' in text and ' minuten' in text:
            for i, w in satz.items():
                if w == 'minuten':
                    m_ind = i
                    try:
                        if int(satz.get(m_ind - 1)) >= 0:
                            zeit = int(satz.get(m_ind - 1))
                    except TypeError:
                        minute = '00'
        else:
            hour = 'None'
            minute = 'None'
        if minute != 'None':
            add = now.minute + zeit
            if add >= 60:
                ubertrag = add - 60
                hour = now.hour + 1
                if ubertrag <= 9:
                    minute = '0' + str(ubertrag)
                else:
                    minute = str(ubertrag)
            else:
                minute = add
                if minute <= 9:
                    minute = '0' + str(minute)
                else:
                    minute = str(minute)
                hour = now.hour
            if hour <= 9:
                hour = '0' + str(hour)
            else:
                hour = str(hour)
        dictionary = {'minute': minute, 'hour': hour}
        return dictionary




    def get_year_rel(self, txt):
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
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
            year = 'None'
        jahr = str(year)
        return jahr


    def get_month_rel(self, txt):
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
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

    def get_wochentag_rel(self, txt): #subject to change
        now = datetime.datetime.now()
        wochentag = datetime.datetime.today().weekday()
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
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

    def get_day_rel(self, txt):  #incl. get_wochentag_rel()
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
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
        elif ' in ' in text and ' tag' in text:
            satz = self.get_text(text)
            for ind, word in satz.items():
                if word == 'tag' or word == 'tagen':
                    t_ind = ind
                    try:
                        if satz.get(t_ind - 2) == 'in':
                            myind = t_ind - 1
                            day = satz.get(myind)
                    except KeyError:
                        day = day

        elif 'übermorgen' in text:
            day = now.day + 2
        elif ' morgen' in text:
            day = now.day + 1
        elif 'heute' in text:
            day = now.day
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
        ub = int(day)
        if day > 1234:
            day = 'None'
        elif day >= 29:
            if now.month == 2 and now.year % 4 != 0:
                t = day - 28
                if t >= 32:
                    u = t - 31
                    if u >= 31:
                        v = u - 30
                        if v >= 32:
                            w = v - 31
                            if w >= 31:
                                x = w - 30
                                if x >= 32:
                                    y = x - 31
                                    if y >= 32:
                                        z = y - 31
                                        day = z
                                    else:
                                        day = y
                                else:
                                    day = x
                            else:
                                day = w
                        else:
                            day = v
                    else:
                        day = u
                else:
                    day = t
            elif now.month == 2 and now.year % 4 == 0:
                if day >= 30:
                    t = day - 29
                    if t >= 32:
                        u = t - 31
                        if u >= 31:
                            v = u - 30
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 32:
                                            z = y - 31
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else:
                        day = t
            elif now.month == 1:
                if day >= 32:
                    t = day - 31
                    if t >= 29 and now.year % 4 != 0:
                        u = t - 28
                        if u >= 31:
                            v = u - 30
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 32:
                                            z = y - 31
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    elif t >= 30 and now.year % 4 == 0:
                        u = t - 29
                        if u >= 31:
                            v = u - 31
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 32:
                                            z = y - 31
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else: day = t
            elif now.month == 3:
                if day >= 32:
                    t = day - 31
                    if t >= 31:
                        u = t - 30
                        if u >= 32:
                            v = u - 31
                            if v >= 31:
                                w = v - 30
                                if w >= 32:
                                    x = w - 31
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 31:
                                            z = y - 30
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else:
                        day = t
            elif now.month == 8:
                if day >= 32:
                    t = day - 31
                    if t >= 31:
                        u = t - 30
                        if u >= 32:
                            v = u - 31
                            if v >= 31:
                                w = v - 30
                                if w >= 32:
                                    x = w - 31
                                    if x >= 32:
                                        y = x - 31
                                        if (now.year + 1) % 4 == 0 and y >= 30:
                                            z = y - 29
                                            day = z
                                        elif (now.year + 1) % 4 != 0 and y >= 29:
                                            z = y - 28
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else:
                        day = t
            elif now.month == 5:
                if day >= 32:
                    t = day - 31
                    if t >= 31:
                        u = t - 30
                        if u >= 32:
                            v = u - 31
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 31:
                                            z = y - 30
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else:
                        day = t
            elif now.month == 10:
                if day >= 32:
                    t = day - 31
                    if t >= 31:
                        u = t - 30
                        if u >= 32:
                            v = u - 31
                            if v >= 32:
                                w = v - 31
                                if (now.year + 1) % 4 == 0 and w >= 30:
                                    x = w - 29
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 31:
                                            z = y - 30
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                elif (now.year + 1) % 4 != 0 and w >= 30:
                                    x = w - 28
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 31:
                                            z = y - 30
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else:
                        day = t
            elif now.month == 7:
                if day >= 32:
                    t = day - 31
                    if t >= 32:
                        u = t - 31
                        if u >= 31:
                            v = u - 30
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 32:
                                            z = y - 31
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
                            day = u
                    else:
                        day = t
            elif now.month == 12:
                if day >= 32:
                    t = day - 31
                    if t >= 32:
                        u = t - 31
                        if (now.year + 1) % 4 == 0 and u >= 30:
                            v = u - 29
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 31:
                                            z = y - 30
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        elif (now.year + 1) % 4 != 0 and u >= 29:
                            v = u - 28
                            if v >= 32:
                                w = v - 31
                                if w >= 31:
                                    x = w - 30
                                    if x >= 32:
                                        y = x - 31
                                        if y >= 31:
                                            z = y - 30
                                            day = z
                                        else:
                                            day = y
                                    else:
                                        day = x
                                else:
                                    day = w
                            else:
                                day = v
                        else:
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
        if day != 'None':
            if day <= 9:
                day = '0' + str(day)
            else:
                day = str(day)
        dic = {}
        dic['Daily'] = day
        dic['Monthly'] = ub
        return dic

    def getmonth_fromday(self, txt):
        tt = txt.replace('.', (''))
        tt = tt.replace('?', (''))
        tt = tt.replace('!', (''))
        tt = tt.replace('.', (''))
        tt = tt.replace(',', (''))
        tt = tt.replace('"', (''))
        tt = tt.replace('(', (''))
        tt = tt.replace(')', (''))
        tt = tt.replace('€', ('Euro'))
        tt = tt.replace('%', ('Prozent'))
        tt = tt.replace('$', ('Dollar'))
        text = tt.lower()
        now = datetime.datetime.now()
        m = now.month
        d = self.get_day_rel(text)
        day = 0
        if d.get('Daily') == 'None':
            month = '00'
        else:
            day = d.get('Monthly')
        if int(day) >= 29:
            if now.month == 2 and now.year % 4 != 0:
                t = day - 28
                m = now.month + 1
                if t >= 32:
                    u = t - 31
                    m = now.month + 2
                    if u >= 31:
                        v = u - 30
                        m = now.month + 3
                        if v >= 32:
                            m = now.month + 4
            elif now.month == 2 and now.year % 4 == 0:
                if day >= 30:
                    t = day - 29
                    m = now.month + 1
                    if t >= 32:
                        u = t - 31
                        m = now.month + 2
                        if u >= 31:
                            v = u - 30
                            m = now.month + 3
                            if v >= 32:
                                m = now.month + 4
            elif now.month == 1:
                if day >= 32:
                    t = day - 31
                    m = now.month + 1
                    if t >= 29 and now.year % 4 != 0:
                        u = t - 28
                        m = now.month + 2
                        if u >= 31:
                            v = u - 30
                            m = now.month + 3
                            if v >= 32:
                                m = now.month + 4
                    elif t >= 30 and now.year % 4 == 0:
                        u = t - 29
                        m = now.month + 2
                        if u >= 31:
                            v = u - 31
                            m = now.month + 3
                            if v >= 32:
                                m = now.month + 4
            elif now.month == 3 or now.month == 8:
                if day >= 32:
                    t = day - 31
                    m = now.month + 1
                    if t >= 31:
                        u = t - 30
                        m = now.month + 2
                        if u >= 32:
                            v = u - 31
                            m = now.month + 3
                            if v >= 31:
                                m = now.month + 4
            elif now.month == 5 or now.month == 10:
                if day >= 32:
                    t = day - 31
                    m = now.month + 1
                    if t >= 31:
                        u = t - 30
                        m = now.month + 2
                        if u >= 32:
                            v = u - 31
                            m = now.month + 3
                            if v >= 32:
                                m = now.month + 4
            elif now.month == 7 or now.month == 12:
                if day >= 32:
                    t = day - 31
                    m = now.month + 1
                    if t >= 32:
                        u = t - 31
                        m = now.month + 2
                        if u >= 31:
                            v = u - 30
                            m = now.month + 3
                            if v >= 32:
                                m = now.month + 4
            else:
                if day >= 31:
                    m = now.month + 1
                    t = day - 30
                    if t >= 32:
                        m = now.month + 2

        month = m
        if month == now.month:
            month = 0
        if month <= 9:
            month = '0' + str(month)
        else:
            month = str(month)

        if month == '00':
            month = 'None'
        return month



    def analyze(self, text):
        now = datetime.datetime.now()
        r = self.get_room(text)
        t = self.get_town(text)
        m_a_d = self.get_month_by_name(text)
        m = m_a_d[0]
        if m == 'None':
            m = self.get_month_abs(text)
            if m == 'None':
                m = self.get_month_rel(text)
                if m == 'None':
                    m = self.getmonth_fromday(text)
        d = m_a_d[1]
        if d == 'None':
            d = self.get_day_abs(text)
            if d == 'None':
                day = self.get_day_rel(text)
                d = day.get('Daily')     #incl. self.get_wochentag_rel(text)
        y = self.get_year_abs(text)
        if y == 'None':
            y = self.get_year_rel(text)
        h = self.get_hour_abs(text)
        mi = self.get_minute_abs(text)
        if mi == 'None':
            minute = self.get_minute_rel(text)
            hour = minute.get('hour')
            mi = minute.get('minute')
            if mi != 'None':
                if h == 'None':
                    stunde = now.hour
                    if hour != 'None':
                        h = int(stunde) + int(hour)
                        if int(h) <= 9:
                            h = '0' + str(h)
                        else:
                            h = str(h)
            else:
                if h == 'None':
                    mi = 'None'
                    h = 'None'
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
    eingabe = 'Erinner mich in 2 Minuten ans putzen'
    print (Analyzer.analyze(eingabe))

if __name__ == '__main__':
    main()
