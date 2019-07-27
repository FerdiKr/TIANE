import datetime
import re

class Sentence_Analyzer:
    def __init__(self, room_list=[], default_location=''):
        self.room_list = room_list
        self.default_location = default_location
        self.zahlwörter = ['null', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'elf', 'zwölf']
        self.zahlwörter_eins = ['einem', 'ein', 'einer', 'eine', 'nem', 'nen', 'ne', 'ner']
        self.zahlwörter_bruchteile = {'viertel':0.25, 'viertelstunde':0.25, 'halb':0.5, 'halbe':0.5, 'halben':0.5, 'einhalb':0.5, 'dreiviertel':0.75, 'dreiviertelstunde':0.75, 'anderthalb':1.5, 'zweieinhalb':2.5, 'dreieinhalb':3.5, 'viereinhalb':4.5}
        self.zahlwörter_reihenfolge = ['nullten', 'ersten', 'zweiten', 'dritten', 'vierten', 'fünften', 'sechsten', 'siebten', 'achten', 'neunten', 'zehnten', 'elften', 'zwölften', 'dreizehnten', 'vierzehnten', 'fünfzehnten', 'sechzehnten',
                                       'siebzehnten', 'achtzehnten', 'neunzehnten', 'zwanzigsten', 'einundzwanzigsten', 'zweiundzwanzigsten', 'dreiundzwanzigsten', 'vierundzwanzigsten', 'fünfundzwanzigsten', 'sechsundzwanzigsten',
                                       'siebenundzwanzigsten', 'achtundzwanzigsten', 'neunundzwanzigsten', 'dreißigsten', 'einunddreißigsten']
        self.zahlwörter_sonstige = {'mitternacht':0}
        self.weekdays = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag']
        self.months = ['platzhaltar', 'januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember']
        self.daytime_clues_pm = ['nachmittags', 'abends', 'spät']
        self.daytime_clues_am = ['morgens', 'früh']
        self.two_word_town_clues = ['los', 'las', 'san', 'sankt', 'new', 'old', 'neu', 'alt', 'bad', 'ober', 'unter', 'west', 'ost', 'nord', 'süd', 'south', 'north' 'east']
        self.böse_wörter_nach_in = ['dem', 'den', 'diesem', 'diesen', 'welchem', 'welchen', 'jenem', 'jenen', 'der', 'dieser', 'welcher', 'jener', 'die', 'diese', 'welche', 'jene', 'diese', 'das', 'welches', 'jenes', 'einem', 'einer',
                                    'meinem', 'deinem', 'seinem', 'ihrem', 'unserem', 'eurem', 'ihrem', 'meinen', 'deinen', 'seinen', 'ihren', 'unseren', 'euren', 'meiner', 'deiner', 'seiner', 'ihrer', 'unserer', 'eurer', 'meine', 'deine', 'seine', 'ihre',
                                    'unsere', 'eure', 'mein', 'dein', 'sein', 'ihr', 'unser', 'euer', 'ihr',
                                    'egal', 'anderen', 'dubio', 'zu', 'gefahr', 'wie']
        self.default_false = None

    def prepare_text(self, text):
        # sämtliche Satz- und Sonderzeichen entfernen, Text bereinigen
        text = text.replace('€', (' Euro'))
        text = text.replace('%', (' Prozent'))
        text = text.replace('$', (' Dollar'))
        text = (" ".join(re.findall(r"[A-Za-z0-9üäöÜÄÖß]*", text))).replace("  "," ")
        # Fügt an Übergängen zwischen Buchstaben und Zahlen immer ein Leerzeichen ein
        int_char = False
        cleared_text = ''
        i = 0
        for char in text:
            if self.to_int(char) is not None:
                if i == 0 or int_char == True:
                    cleared_text = cleared_text + char
                else:
                    cleared_text = cleared_text + ' ' + char
                int_char = True
            else:
                if int_char == False:
                    cleared_text = cleared_text + char
                else:
                    cleared_text = cleared_text + ' ' + char
                int_char = False
            i += 1
        text = cleared_text
        # Weitere Bereinigungen
        while '  ' in text:
            text = text.replace('  ', ' ')
        if text.startswith(' '):
            text = text[1:]
        if text.endswith(' '):
            text = text[:-1]
        return text

    def split_text(self, text):
        return(text.split(' '))

    def lower_split_text(self, text_split):
        return[word.lower() for word in text_split]

    def to_int(self, word):
        # Wandelt so ziemlich alles in eine Zahl um oder gibt 'None' aus, wenn nicht möglich.
        # Achtung, nicht vom Namen trügen lassen: Diese Funktion gibt meistens floats aus!
        if word is None:
            return None
        number = None
        try:
            number = float(word)
        except:
            word = word.lower()
            try:
                number = self.zahlwörter.index(word)
            except:
                try:
                    number = self.zahlwörter_bruchteile[word]
                except:
                    try:
                        number = self.zahlwörter_reihenfolge.index(word)
                    except:
                        try:
                            number = self.months.index(word)
                        except:
                            try:
                                number = self.weekdays.index(word)
                            except:
                                try:
                                    number = self.zahlwörter_sonstige[word]
                                except:
                                    if word in self.zahlwörter_eins:
                                        number = 1
        return number

    def to_time_unit(self, word):
        # Vereinheitlicht Zeiteinheiten, oder gibt 'None' aus, wenn nicht möglich
        if word.lower() in ['s', 'sec', 'secs', 'second', 'seconds', 'sek', 'sekunde', 'sekunden']:
            return 'seconds'
        elif word.lower() in ['min', 'minute', 'minutes', 'minuten']:
            return 'minutes'
        elif word.lower() in ['h', 'hour', 'hours', 'std', 'stunde', 'stunden']:
            return 'hours'
        elif word.lower() in ['d', 'day', 'days', 'tag', 'tage', 'tagen']:
            return 'days'
        elif word.lower() in ['week', 'weeks', 'woche', 'wochen']:
            return 'weeks'
        elif word.lower() in ['month', 'months', 'monat', 'monate', 'monaten']:
            return 'months'
        elif word.lower() in ['y', 'year', 'years', 'jahr', 'jahre', 'jahren']:
            return 'years'
        else:
            return None

    def get_town(self, text, text_split, text_split_lower):
        town = self.default_false
        offset = 0
        try:
            while True:
                # Sucht das nächste "in" im Text
                in_index = text_split_lower[offset:].index('in')
                try:
                    # Versucht, den Ort zu extrahieren
                    town = text_split[offset:][in_index+1]
                except IndexError:
                    raise ValueError
                if town.lower() in self.two_word_town_clues:
                    try:
                        town = town + ' ' + text_split[offset:][in_index+2]
                    except IndexError:
                        town = town
                # Checkt den erhaltenen Ort
                if self.to_int(town) is not None or town.lower() in self.böse_wörter_nach_in or town in self.room_list:
                    town = self.default_false
                    offset = offset + in_index + 1
                else:
                    break
        except ValueError:
            # Kein weiteres "in" mehr gefunden
            if 'zu hause' in text.lower() or 'daheim' in text.lower() or 'hier' in text_split_lower:
                town = self.default_location
        return town

    def get_room(self, text_split_lower):
        rooms = [self.default_false]
        for room in self.room_list:
            if room.lower() in text_split_lower:
                rooms.append(room)
        return rooms[0], rooms

    def get_time_after_in(self, text_split_lower):
        add_times = []
        offset = 0
        time_amount = None
        time_unit = None
        try:
            while True:
                # Sucht das nächste "in" im Text
                in_index = text_split_lower[offset:].index('in')
                try:
                    # Versucht, die Zeit inkl. Einheit zu extrahieren
                    time_amount = text_split_lower[offset:][in_index+1]
                    time_unit = text_split_lower[offset:][in_index+2]
                except IndexError:
                    raise ValueError

                # Checkt die erhaltene Zeit und Zeiteinheit
                if self.to_int(time_amount) is not None and self.to_time_unit(time_unit) is not None:
                    # z.B. "in einem Jahr"
                    add_times.append((self.to_int(time_amount), self.to_time_unit(time_unit)))
                    offset = offset + in_index + 3
                    # Geht es vielleicht mit Konstruktionen wie "in 12 Stunden, 40 Minuten und 10 Sekunden" noch weiter?
                    offset, add_times = self.get_time_after_und_after_in(text_split_lower, offset, add_times)

                elif self.to_int(time_amount) is not None and time_unit in self.zahlwörter_bruchteile.keys():
                    # z.B. "in einer dreiviertel Stunde"...
                    time_factor = time_unit
                    try:
                        time_unit = text_split_lower[offset:][in_index+3]
                    except IndexError:
                        if time_factor not in ['viertelstunde', 'dreiviertelstunde']:
                            raise ValueError
                        else:
                            pass
                    if time_factor in ['viertelstunde', 'dreiviertelstunde']:
                        time_unit = 'hour'
                        offset = offset + in_index + 3
                    else:
                        offset = offset + in_index + 4
                    if self.to_time_unit(time_unit) is not None:
                        add_times.append((self.to_int(time_amount)*self.to_int(time_factor), self.to_time_unit(time_unit)))
                        # Geht es vielleicht mit Konstruktionen wie "in 12 Stunden, 40 Minuten und 10 Sekunden" noch weiter?
                        offset, add_times = self.get_time_after_und_after_in(text_split_lower, offset, add_times)
                    else:
                        time_amount = None
                        time_unit = None
                        offset = offset + in_index + 1

                else:
                    time_amount = None
                    time_unit = None
                    offset = offset + in_index + 1
        except ValueError:
            # Kein weiteres "in" mehr gefunden
            return add_times

    def get_time_after_und_after_in(self, text_split_lower, offset, add_times):
        # Geht es vielleicht mit Konstruktionen wie "in 12 Stunden, 40 Minuten und 10 Sekunden" noch weiter?
        try:
            while True:
                if text_split_lower[offset:][0] in ['und', 'and']:
                    offset += 1
                    continue
                time_amount = text_split_lower[offset:][0]
                time_unit = text_split_lower[offset:][1]
                if self.to_int(time_amount) is not None and self.to_time_unit(time_unit) is not None:
                    add_times.append((self.to_int(time_amount), self.to_time_unit(time_unit)))
                    offset += 2
                    continue
                elif self.to_int(time_amount) is not None and time_unit in self.zahlwörter_bruchteile.keys():
                    # z.B. "in einer Dreiviertelstunde"...
                    time_factor = time_unit
                    try:
                        time_unit = text_split_lower[offset:][2]
                    except IndexError:
                        if time_factor not in ['viertelstunde', 'dreiviertelstunde']:
                            break
                        else:
                            pass
                    if time_factor in ['viertelstunde', 'dreiviertelstunde']:
                        time_unit = 'hour'
                        offset += 2
                    else:
                        offset += 3
                    if self.to_time_unit(time_unit) is not None:
                        add_times.append((self.to_int(time_amount)*self.to_int(time_factor), self.to_time_unit(time_unit)))
                    else:
                        break
                else:
                    break
        except IndexError:
            pass
        return offset, add_times

    def get_time_after_um(self, text_split_lower):
        set_hours = None
        set_minutes = None
        tag_übertrag = 0 ### z.Zt. ungenutzt, aber ich kann mir vorstellen, dass man es braucht...
        daytime = None
        possible_daytime_clues = []
        offset = 0
        # löscht das "Füllwort" "Uhr" aus dem Text, das brauchen wir hier nicht ;)
        while 'uhr' in text_split_lower:
            text_split_lower.remove('uhr')
        try:
            while set_hours is None and set_minutes is None:
                # Sucht das nächste "um" im Text
                um_index = text_split_lower[offset:].index('um')

                # Fall 1: "Um 5 Uhr"
                add_offset = 0
                try:
                    hours = text_split_lower[offset:][um_index+1]
                except IndexError:
                    raise ValueError
                if self.to_int(hours) is not None and hours not in self.zahlwörter_bruchteile and 0 <= self.to_int(hours) < 24:
                    add_offset += 1
                    set_hours = self.to_int(hours)
                    set_minutes = 0
                    try:
                        minutes = text_split_lower[offset:][um_index+2]
                    except IndexError:
                        raise ValueError
                    # Fall 1.1: "Um 5 Uhr 45"
                    if self.to_int(minutes) is not None and 0 <= self.to_int(minutes) < 60:
                        add_offset += 1
                        set_minutes = self.to_int(minutes)
                    # Fall nicht-1 (weil 2): "Um 5 vor 10"
                    elif minutes in ['vor', 'nach']:
                        # ...und ich versuche mit diesem ganzen Konstrukt auch eher notdürftig, Fälle wie "wir treffen uns um 5 vor der Tür" aufzufangen
                        try:
                            word_after_vornach = text_split_lower[offset:][um_index+3]
                        except IndexError:
                            word_after_vornach = '0'
                        if word_after_vornach not in self.böse_wörter_nach_in:
                            # ...Aber ansonsten gehen wir halt davon aus, dass eigentlich Fall 2 gemeint ist
                            set_hours = None
                            set_minutes = None
                            add_offset = 0
                    else:
                        possible_daytime_clues.append(minutes)
                    try:
                        possible_daytime_clues.append(text_split_lower[offset + um_index-1])
                    except:
                        pass

                    offset += add_offset

                # Fall 2: "Um 20 vor 5"
                try:
                    minutes = text_split_lower[offset:][um_index+1]
                    vor_nach = text_split_lower[offset:][um_index+2]
                    add_offset = 2
                except IndexError:
                    raise ValueError
                try:
                    hours = text_split_lower[offset:][um_index+3]
                    add_offset = 3
                except IndexError:
                    hours = None
                    pass
                if self.to_int(minutes) is not None and vor_nach in ['vor', 'nach']:
                    if vor_nach == 'vor':
                        if minutes == 'viertel':
                            set_minutes = 45
                        else:
                            set_minutes = 60 - self.to_int(minutes)
                        if hours is not None and self.to_int(hours) is not None and 0 <= self.to_int(hours) < 24:
                            set_hours = self.to_int(hours) - 1
                    elif vor_nach == 'nach':
                        if minutes == 'viertel':
                            set_minutes = 15
                        else:
                            set_minutes = self.to_int(minutes)
                        if hours is not None and self.to_int(hours) is not None and 0 <= self.to_int(hours) < 24:
                            set_hours = self.to_int(hours)
                    try:
                        possible_daytime_clues.append(text_split_lower[offset:][um_index-1])
                    except:
                        pass
                    try:
                        possible_daytime_clues.append(text_split_lower[offset:][um_index+add_offset+1])
                    except:
                        pass
                else:
                    add_offset = 0
                offset += add_offset

                # Fall 3: "Um halb 6"
                try:
                    halb = text_split_lower[offset:][um_index+1]
                    add_offset = 1
                except IndexError:
                    raise ValueError
                try:
                    hours = text_split_lower[offset:][um_index+2]
                    add_offset = 2
                except IndexError:
                    hours = None
                    pass
                if halb == 'halb':
                    set_minutes = 30
                    if self.to_int(hours) is not None and 0 <= self.to_int(hours) < 24:
                        set_hours = self.to_int(hours) - 1
                    try:
                        possible_daytime_clues.append(text_split_lower[offset:][um_index-1])
                    except:
                        pass
                    try:
                        possible_daytime_clues.append(text_split_lower[offset:][um_index+add_offset+1])
                    except:
                        pass
                    offset += add_offset

                if set_hours is None and set_minutes is None:
                    offset += 1

        except ValueError:
            # Kein weiteres "um" mehr gefunden
            pass
        # Hier finden wir noch raus, ob die Tageszeit explizit festgelegt wurde, und rechnen ggf. schon mal 6 Uhr in 18 Uhr um...
        if set_hours is not None:
            if set_hours >= 12:
                daytime = 'pm'
            elif [x for x in possible_daytime_clues if x in self.daytime_clues_pm]:
                set_hours += 12
                daytime = 'pm'
            elif [x for x in possible_daytime_clues if x in self.daytime_clues_am]:
                daytime = 'am'
        return set_hours, set_minutes, daytime

    def get_time_after_am(self, text_split_lower):
        set_month = None
        set_day = None
        set_year = None
        set_weekday = None
        offset = 0
        try:
            while set_month is None and set_day is None and set_weekday is None:
                # Sucht das nächste "am" im Text
                am_index = text_split_lower[offset:].index('am')

                # Fall 1: "Am 23.""
                try:
                    day = text_split_lower[offset:][am_index+1]
                except IndexError:
                    raise ValueError
                try:
                    month = text_split_lower[offset:][am_index+2]
                except IndexError:
                    month = None
                    pass
                try:
                    year = text_split_lower[offset:][am_index+3]
                except IndexError:
                    year = None
                    pass
                # "Am 12."...
                if self.to_int(day) is not None and day not in self.weekdays and 0 < self.to_int(day) <= 31:
                    set_day = self.to_int(day)
                    offset += 1
                    # ..."3./März"...
                    if self.to_int(month) is not None and month not in self.weekdays and 1 <= self.to_int(month) <= 12:
                        set_month = self.to_int(month)
                        offset += 1
                        # ..."45/2045"!
                        if self.to_int(year) is not None and year not in self.weekdays and year not in self.months:
                            set_year = self.to_int(year)
                            offset += 1

                # Fall 2: "Am Mittwoch"
                elif [x for x in text_split_lower if x in self.weekdays]:
                    weekday = [x for x in text_split_lower if x in self.weekdays][0]
                    set_weekday = self.to_int(weekday)
                    # Den sehr speziellen Fall "Mittwoch, den 23.4." berücksichtigen:
                    weekday_index = text_split_lower.index(weekday)
                    try:
                        den = text_split_lower[weekday_index+1]
                    except IndexError:
                        den = None
                        pass
                    try:
                        day = text_split_lower[weekday_index+2]
                    except IndexError:
                        day = None
                        pass
                    try:
                        month = text_split_lower[weekday_index+3]
                    except IndexError:
                        month = None
                        pass
                    try:
                        year = text_split_lower[weekday_index+4]
                    except IndexError:
                        year = None
                        pass
                    # "den 12."...
                    if den == 'den' and self.to_int(day) is not None and day not in self.weekdays and 0 < self.to_int(day) <= 31:
                        set_day = self.to_int(day)
                        # ..."3./März"...
                        if self.to_int(month) is not None and month not in self.weekdays and 1 <= self.to_int(month) <= 12:
                            set_month = self.to_int(month)
                            # ..."45/2045"!
                            if self.to_int(year) is not None and year not in self.weekdays and year not in self.months:
                                set_year = self.to_int(year)

                else:
                    offset += 1
        except ValueError:
            # Kein weiteres "am" mehr gefunden
            pass
        # Das Jahr müssen wir noch ein bisschen vereinheitlichen...
        if set_year is not None:
            if set_year < 100:
                set_year = 2000 + set_year
        return set_day, set_month, set_year, set_weekday

    def get_time_after_der(self, text_split_lower):
        set_month = None
        set_day = None
        set_year = None
        set_weekday = None
        offset = 0
        try:
            while set_month is None and set_day is None and set_weekday is None:
                # Sucht das nächste "der" im Text
                der_index = text_split_lower[offset:].index('der')

                # Fall 1: "der 23.""
                try:
                    day = text_split_lower[offset:][der_index+1]
                except IndexError:
                    raise ValueError
                try:
                    month = text_split_lower[offset:][der_index+2]
                except IndexError:
                    month = None
                    pass
                try:
                    year = text_split_lower[offset:][der_index+3]
                except IndexError:
                    year = None
                    pass
                # "der 12."...
                if self.to_int(day) is not None and day not in self.weekdays and 0 < self.to_int(day) <= 31:
                    set_day = self.to_int(day)
                    offset += 1
                    # ..."3./März"...
                    if self.to_int(month) is not None and month not in self.weekdays and 1 <= self.to_int(month) <= 12:
                        set_month = self.to_int(month)
                        offset += 1
                        # ..."45/2045"!
                        if self.to_int(year) is not None and year not in self.weekdays and year not in self.months:
                            set_year = self.to_int(year)
                            offset += 1

                # Fall 2: "der Mittwoch"
                elif [x for x in text_split_lower if x in self.weekdays]:
                    weekday = [x for x in text_split_lower if x in self.weekdays][0]
                    set_weekday = self.to_int(weekday)

                else:
                    offset += 1
        except ValueError:
            # Kein weiteres "der" mehr gefunden
            pass
        # Das Jahr müssen wir noch ein bisschen vereinheitlichen...
        if set_year is not None:
            if set_year < 100:
                set_year = 2000 + set_year
        return set_day, set_month, set_year, set_weekday

    def get_other_relative_times(self, text_split_lower):
        add_times = []
        if 'morgen' in text_split_lower:
            add_times.append((1, 'days'))
        if 'übermorgen' in text_split_lower:
            add_times.append((2, 'days'))
        return add_times

    def zeit_setzen(self, start_time, microsecond=None, second=None, minute=None, hour=None, day=None, month=None, year=None):
        # Setzt bei einer gegebenen Zeit gegebene Werte
        microsecond = int(microsecond) if microsecond is not None else start_time.microsecond
        second = int(second) if second is not None else start_time.second
        minute = int(minute) if minute is not None else start_time.minute
        hour = int(hour) if hour is not None else start_time.hour
        day = int(day) if day is not None else start_time.day
        month = int(month) if month is not None else start_time.month
        year = int(year) if year is not None else start_time.year
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond)

    def zeiten_addieren(self, start_time, time, unit):
        # Addiert zu einer gegebenen Zeit eine Zeitmenge mit entsprechender Einheit dazu
        if unit == 'seconds':
            return start_time + datetime.timedelta(seconds=time)
        elif unit == 'minutes':
            return start_time + datetime.timedelta(minutes=time)
        elif unit == 'hours':
            return start_time + datetime.timedelta(hours=time)
        elif unit == 'days':
            return start_time + datetime.timedelta(days=time)
        elif unit == 'weeks':
            return start_time + datetime.timedelta(days=7*time)
        elif unit == 'months':
            while start_time.month + time > 12:
                if not start_time.year + 1 >= datetime.MAXYEAR:
                    start_time = self.zeit_setzen(start_time, year=start_time.year+1)
                    time -= 12
                else:
                    start_time = self.zeit_setzen(start_time, year=datetime.MAXYEAR)
                    time -= 12
            start_time = self.zeit_setzen(start_time, month=start_time.month+time)
            return start_time
        elif unit == 'years':
            if not start_time.year + time >= datetime.MAXYEAR:
                start_time = self.zeit_setzen(start_time, year=start_time.year+time)
                return start_time
            else:
                start_time = self.zeit_setzen(start_time, year=datetime.MAXYEAR)
                return start_time

    def analyze(self, text):
        time = datetime.datetime.now()
        now = time
        add_times = []

        # Die verschiedenen "Versionen" des Eingabetextes sammeln
        text = self.prepare_text(text)
        text_split = self.split_text(text)
        text_split_lower = self.lower_split_text(text_split)

        # Ortsinformationen extrahieren
        town = self.get_town(text, text_split, text_split_lower)
        room, rooms = self.get_room(text_split_lower)

        # Zeitinformationen extrahieren
        set_hours, set_minutes, daytime = self.get_time_after_um(text_split_lower)
        set_day, set_month, set_year, set_weekday = self.get_time_after_am(text_split_lower)
        set_day_2, set_month_2, set_year_2, set_weekday_2 = self.get_time_after_der(text_split_lower)

        set_day = set_day if set_day is not None else set_day_2
        set_month = set_month if set_month is not None else set_month_2
        set_year = set_year if set_year is not None else set_year_2
        set_weekday = set_weekday if set_weekday is not None else set_weekday_2

        for add_time in self.get_time_after_in(text_split_lower):
            add_times.append(add_time)
        for add_time in self.get_other_relative_times(text_split_lower):
            add_times.append(add_time)

        # Zeiten verrechnen
        # Erst relative Zeitangaben ("in 3 Wochen") addieren...
        for time_amount, time_unit in add_times:
            time = self.zeiten_addieren(time, time_amount, time_unit)
        # ...dann von der Zielzeit ausgehend die explizit angegebenen Werte setzen
        if set_year is not None:
            time = self.zeit_setzen(time, year=set_year)
        if set_month is not None:
            time = self.zeit_setzen(time, month=set_month)
        if set_day is not None:
            time = self.zeit_setzen(time, day=set_day)
        elif set_weekday is not None:
            # Man beachte, dass das hier ein ELif ist. Der Wochentag wird nur hinzugezogen,
            # wenn keine viel explizitere Angabe gemacht wurde.
            current_weekday = time.weekday()
            difference = set_weekday - current_weekday
            time = self.zeiten_addieren(time, difference, 'days')
            while time.year < now.year or time.month < now.month or time.day < now.day:
                time = self.zeiten_addieren(time, 1, 'weeks')
        if set_minutes is not None:
            time = self.zeit_setzen(time, minute=set_minutes)
        if set_hours is not None:
            time = self.zeit_setzen(time, hour=set_hours)
            if daytime is not None:
                while (time - now).total_seconds() <= 0:
                    time = self.zeiten_addieren(time, 1, 'days')
            else:
                while (time - now).total_seconds() <= 0:
                    time = self.zeiten_addieren(time, 12, 'hours')
        if set_minutes is not None or set_hours is not None:
            time = self.zeit_setzen(time, second=0)
            time = self.zeit_setzen(time, microsecond=0)
        return {'town':town, 'room':room, 'rooms':rooms, 'datetime':time, 'time':{'day':time.day, 'month':time.month, 'year':time.year, 'hour':time.hour, 'minute':time.minute, 'second':time.second}}

def main():
    Analyzer = Sentence_Analyzer(room_list=['Wohnzimmer', 'Schlafzimmer'], default_location='Weitersburg')
    print(Analyzer.analyze('Welcher Tag ist der 23.12.?'))

if __name__ == '__main__':
    main()
