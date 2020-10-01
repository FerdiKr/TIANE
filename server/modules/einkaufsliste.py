import traceback
import random
import traceback

# Priorität gesetzt, da ansonsten manchmal das modul reload_modules.py aufgerufen wurde.
PRIORITY = 2
SECURE = True


def isValid(text):
    text = text.lower()
    if 'to' in text and 'do' in text and 'liste' in text:
        return False
    elif 'setz' in text or 'setzte' in text or 'schreib' in text or 'schreibe' in text or 'füg' in text or 'füge' in text:
        return True
    elif ('was' in text and 'steht' in text and 'auf' in text) or ('gib' in text and 'aus' in text):
        return True
    elif ('lösch' in text or 'leere' in text) and 'einkaufsliste' in text:
        return True
    elif ('send' in text or 'schick' in text or 'schreib' in text) and 'einkaufsliste' in text:
        return True
    elif 'räum' in text and 'auf' in text and 'einkaufsliste' in text:
        return True
    else:
        return False
        

def get_item(text, tiane):
    text = tiane.text
    text = text.replace('Und',
                        'und')  # einfach nur zur Sicherheit, damit die Item-Trennung später auch sicher funktioniert
    text = text.replace(' g ', 'g ')
    text = text.replace(' gram ', 'g ')
    text = text.replace(' kg ', 'kg ')
    text = text.replace(' kilogram ', 'kg ')
    text = text.replace('eine ', '')
    text = text.replace('einen ', '')
    text = text.replace('ein ', '')
    item = []
    index = 0

    # es wird ermittel, wo die Nennung der items beginnt und wo sie endet
    if 'setz auf die einkaufsliste ' in text:
        text.replace('setz auf die Einkaufsliste ', (''))
        text = text.split(' ')
        index = 0

    elif 'setz' in text or 'setzte' in text or 'schreib' in text or 'schreibe' in text:
        text = text.split(' ')
        founded = False
        i = 0
        while i <= len(text) and founded is False:
            if text[i] == 'setz' or text[i] == 'setzte' or text[i] == 'schreib' or text[i] == 'schreibe':
                index = i + 1
                founded = True
            i += 1

    elif 'füg' in text or 'füge' in text:
        text = text.split(' ')
        founded = False
        i = 0
        while i <= len(text) and founded is False:
            if text[i] == 'füg' or text[i] == 'füge':
                index = i + 1
                founded = True
            i += 1

    elif 'lösch' in text:
        text = text.split(' ')
        founded = False
        i = 0
        while i <= len(text) and founded is False:
            if text[i] == 'lösch' or text[i] == 'lösche':
                index = i + 1
                founded = True
            i += 1

    else:
        index = -1
        tiane.say('Ich habe leider nicht verstanden, was ich auf die Liste setzen soll. '
                 'Versuch es doch Mal mit der Syntax: Setz Milch auf die Liste.')

    """
    Dieser Algorithmus trennt nicht die genannten Items nach dem Wort 'und', sondern filtert sie heraus. Probleme gibt es hier nur, wenn
    ein item aus mehreren Wörtern besteht, wie zum Beispiel 'Creme legere'
    #text = text.replace('und', '')
    if index != -1:
        stop = False
        point = index
        while stop is False:
            if text[point] is 'auf' or text[point] is 'zu' or text[point] is 'zur':
                stop = True
            elif text[point + 1] is 'g' or text[point + 1] is 'kilo':
                item.append(text[point] + ' ' + text[point + 1] + ' ' + text[point + 2])
                point += 2
            elif text[point] is 'ein' or text[point] is 'einen' or text[point] is 'eine' or text[point] is 'zwei' or \
                    text[point] is 'drei' or text[point] is 'vier' or text[point] is 'fünf' or text[point] is 'sechs' or \
                    text[point] is 'sieben' or text[point] is 'acht' or text[point] is 'neun' or text[point] is 'zehn':
                item.append(text[point] + ' ' + text[point + 1])
                point += 1
            elif text[point] is 'und':
                continue
            else:
                item.append(text[point])
            point += 1
    """

    # Der folgende Alorithmus trennt die genannten Items ganz stumpf bei jedem 'und'
    if index != -1:
        aussage_item = ''
        position = index
        stop = False
        while stop == False:
            if text[position] == 'auf' or text[position] == 'zu' or text[position] == 'zur' or text[
                position] == 'aus' or text[position] == 'von':

                item.append(aussage_item.strip())
                stop = True
            elif text[position] == 'und':
                item.append(aussage_item.strip())
                aussage_item = ''
            else:
                aussage_item += text[position] + ' '

            position += 1
    duplicates_in_items = [item[i] for i in range(len(item)) if not i == item.index(item[i])]
    if duplicates_in_items:
        item = assamble_array(item)
    return item


def get_aussage_gemeinsam(text, tiane):
    aussage = ''
    if 'einkaufsliste' in tiane.local_storage.keys():
        einkaufsliste = tiane.local_storage.get('einkaufsliste')
        aussage = get_enumerate(einkaufsliste)
    return aussage


def get_aussage(text, tiane):
    nutzer = tiane.user
    nutzerdictionary = tiane.local_storage.get('users')
    nd = nutzerdictionary.get(nutzer)
    aussage = ''
    if 'einkaufsliste' in nd.keys():
        einkaufsliste = nd['einkaufsliste']
        aussage = get_enumerate(einkaufsliste)

    return aussage


def handle(text, tiane, profile):
    text = text.lower()
    text = text.replace('setze', ('setz'))

    if 'setz' in text or 'schreib' in text or 'füg' in text:
        item = get_item(text, tiane)
        own_list = False
        if 'eigene' in text or 'meine' in text:
            nutzer = tiane.user
            nutzerdictionary = tiane.local_storage.get('users')
            nd = nutzerdictionary.get(nutzer)
            if 'einkaufsliste' not in nd.keys():
                nd['einkaufsliste'] = []
            einkaufsliste = nd['einkaufsliste']
            own_list = True
        else:
            if 'einkaufsliste' not in tiane.local_storage.keys():
                tiane.local_storage['einkaufsliste'] = []
            einkaufsliste = tiane.local_storage['einkaufsliste']
        if einkaufsliste:
            double_items = get_double_items(item, einkaufsliste, tiane)
            if double_items:
                if len(double_items) > 1:
                    tiane.say(
                        '{} befinden sich bereits auf der einkaufsliste. Soll ich sie dennoch auf die Einkaufsliste setzen?'.format(
                            get_enumerate(double_items)))
                else:
                    tiane.say(
                        '{} befindet sich bereits auf der einkaufsliste. Soll ich sie dennoch auf die Einkaufsliste setzen?'.format(
                            get_enumerate(double_items)))
                response = tiane.listen()
                if 'nur' in text and 'nicht' in text:
                    item.remove(get_item(get_text_beetween('nur', text, end_word='nicht', output='String')))
                elif 'ja' in response or 'gerne' in response or 'bitte' in response:
                    for i in item:
                        einkaufsliste.append(i)
                    neue_einkaufsliste = assamble_array(einkaufsliste)
                    einkaufsliste = neue_einkaufsliste
                else:
                    for i in double_items:
                        item.remove(i)
                    if not item:
                        tiane.say('Alles klar, ich setze nichts auf die Einkaufsliste.')
                        pass
                    else:
                        for i in item:
                            einkaufsliste.append(i)
                        neue_einkaufsliste = assamble_array(einkaufsliste)
                        einkaufsliste = neue_einkaufsliste
                        tiane.say('Alles klar, ich habe nur {} auf die Einkaufsliste gesetzt.'.format(
                            get_enumerate(item)))

            else:
                for i in item:
                    einkaufsliste.append(i)

        else:
            einkaufsliste = []
            for i in item:
                einkaufsliste.append(i)
        
        einkaufsliste = assamble_array(einkaufsliste)
        
        if own_list:
            tiane.say("Alles klar. Ich habe {} auf deine Einkaufsliste gesetzt.".format(get_enumerate(item)))
            nd['einkaufsliste'] = einkaufsliste
        else:
            tiane.say("Alles klar. Ich habe {} auf die gemeinsame Einkaufsliste gesetzt.".format(get_enumerate(item)))
            tiane.local_storage['einkaufsliste'] = einkaufsliste


    elif 'auf' in text and 'steht' in text and 'was' in text:
        if 'meiner' in text or 'eigenen' in text:
            aussage = get_aussage(text, tiane)
        else:
            aussage = get_aussage_gemeinsam(text, tiane)
        # wenn man den Befehl über Telegram aufruft, mach die schick-Funktion mehr Sinn
        if tiane.telegram_call:
            handle('schick einkaufsliste', tiane, profile)
        else:
            if aussage != '':
                ausgabe = 'Auf der Liste steht für dich {}.'.format(aussage)
            else:
                ausgabe = 'Für dich steht aktuell nichts auf der Einkaufsliste.'
            tiane.say(ausgabe)

    elif 'schick' in text and 'einkaufsliste' in text and 'und' in text and ('lösch' in text or 'leer' in text):
        i = ''
        if 'meine' in text or 'eigene' in text:
            i = 'meine'
        else:
            i = 'gemeinsame'

        text = "schick {} einkaufsliste".format(i)
        handle(text, tiane, profile)
        text = "leere {} einkaufsliste".format(i)
        handle(text, tiane, profile)

    elif 'lösch' in text and ('aus' in text or 'von' in text) and 'einkaufsliste' in text:
        items = get_item(text, tiane)
        own_list = False
        if 'eigene' in text or 'meine' in text:
            nutzer = tiane.user
            nutzerdictionary = tiane.local_storage.get('users')
            nd = nutzerdictionary.get(nutzer)
            if 'einkaufsliste' not in nd.keys():
                nd['einkaufsliste'] = []
                einkaufsliste = nd['einkaufsliste']
            own_list = True
        else:
            if 'einkaufsliste' not in tiane.local_storage.keys():
                tiane.local_storage['einkaufsliste'] = []
                einkaufsliste = tiane.local_storage['einkaufsliste']

        if einkaufsliste:
            deleted = []
            for item in items:
                try:
                    einkaufsliste.remove(item)
                    deleted.append(item)
                except:
                    traceback.print_exc()
                    tiane.say(
                        'Scheinbar ist {} nicht in der Einkaufsliste vorhanden und konnte daher nicht gelöscht werden.'.format(
                            item))
                if len(deleted) != -1:
                    tiane.say(get_enumerate(deleted) + ' wurde von deiner Einkaufsliste gelöscht.')
                else:
                    tiane.say(
                        'Da ist wohl was schief gelaufe. Ich konnte leider nichts aus der Einkaufsliste löschen.')
        else:
            tiane.say('Ich kann das leider nicht aus deiner Einkaufsliste löschen, da sie leer ist.')


    elif ('lösch' in text or 'leer' in text) and 'einkaufsliste' in text and not 'aus' in text:
        word = 'geleert'
        if 'lösche' in text:
            word = 'gelöscht'

        if 'eigene' in text or 'meine' in text:
            nutzer = tiane.user
            nutzerdictionary = tiane.local_storage.get('users')
            nd = nutzerdictionary.get(nutzer)
            if 'einkaufsliste' in nd.keys():
                empty = []
                nd['einkaufsliste'] = empty
                tiane.say('Deine Einkaufsliste wurde {}.'.format(word))
            else:
                tiane.say('Deine Einkaufsliste ist schon leer.')
        else:
            if 'einkaufsliste' in tiane.local_storage:
                empty = []
                tiane.local_storage['einkaufsliste'] = empty
                tiane.say('Die Einkaufsliste wurde {}.'.format(word))
            else:
                tiane.say('Die Einkaufliste ist schon leer.')

    elif 'send' in text or 'schick' in text or 'schreib' in text:
        user = ''
        if 'meine' in text or 'eigene' in text:
            nutzer = tiane.user
            nutzerdictionary = tiane.local_storage.get('users')
            nd = nutzerdictionary.get(nutzer)
            items = []
            if 'einkaufsliste' in nd.keys():
                user = tiane.user + ' '
                items = nd['einkaufsliste']
            else:
                user = tiane.user + ' '
        else:
            items = tiane.local_storage.get('einkaufsliste')
        send_to_telegram(items, user, tiane)

    elif 'räum' in text and 'auf' in text:
        # eigentlich sollte es nicht passieren, dass Sachen unordentlich
        # in der einkaufsliste stehen, aber sollte es doch sein, hat man
        # die möglichkeit manuell einzugreifen
        tiane.say('Einen Moment bitte.')
        if 'meine' in text:
            nutzer = tiane.user
            nutzerdictionary = tiane.local_storage.get('users')
            nd = nutzerdictionary.get(nutzer)
            nd['einkaufsliste'] = assamble_array(nd['einkaufsliste'])
            tiane.say('Deine Einkaufsliste wurde aufgeräumt!')
        else:
            tiane.local_storage['einkaufsliste'] = assamble_array(tiane.local_storage['einkaufsliste'])

            tiane.say('Die Einkaufsliste wurde aufgeräumt!')


def send_to_telegram(items, user, tiane):
    if items == None:
        items = []
    aussage = '--- Einkaufsliste: {}---\n'.format(user)
    for i in items:
        aussage = aussage + '- ' + i + '\n'
    aussage += '--------------------'
    tiane.say(aussage, output='telegram')


def get_double_items(items, einkaufsliste, tiane):
    double = []
    if einkaufsliste is None:
        double = []
    else:
        for item in items:
            anz = item.split(' ', 1)[0]
            try:
                anz = int(anz)
            except:
                pass
            if type(anz) is int:
                item = item.split(' ', 1)[1]
            if item in einkaufsliste:
                double.append(item)
    return double



def batchGen(batch):
    """
    With the batchGen-function you can generate fuzzed compare-strings
    with the help of a easy syntax:
        "Wann [fährt|kommt] [der|die|das] nächst[e,er,es] [Bahn|Zug]"
    is compiled to a list of sentences, each of them combining the words
    in the brackets in all different combinations.
    This list can then fox example be used by the batchMatch-function to
    detect special sentences.
    """
    outlist = []
    ct = 0
    while len(batch) > 0:
        piece = batch.pop()
        if "[" not in piece and "]" not in piece:
            outlist.append(piece)
        else:
            frontpiece = piece.split("]")[0]
            inpiece = frontpiece.split("[")[1]
            inoptns = inpiece.split("|")
            for optn in inoptns:
                rebuild = frontpiece.split("[")[0] + optn
                rebuild += "]".join(piece.split("]")[1:])
                batch.append(rebuild)
    return outlist

def batchMatch(batch, match):
    t = False
    if isinstance(batch, str):
        batch = [batch]
    for piece in batchGen(batch):
        if piece.lower() in match.lower():
            t = True
    return t


def get_enumerate(array):
    new_array = []  # array=['Apfel', 'Birne', 'Gemüse', 'wiederlich']
    for item in array:
        new_array.append(item.strip(' '))

    ausgabe = ''
    if len(new_array) == 0:
        pass
    elif len(new_array) == 1:
        ausgabe = array[0]
    else:
        for item in range(len(new_array) - 1):
            ausgabe += new_array[item] + ', '
        ausgabe = ausgabe.rsplit(', ', 1)[0]
        ausgabe = ausgabe + ' und ' + new_array[-1]
    return ausgabe
    
def assamble_new_items(array, new_items):
    new_array = []
    for item in new_items:
        # Name des items von der Anzahl trennen
        if len(item.split(' ')) > 1:
            # Durch die 1 in der runden Klammer, wird nur beim ersten Space
            # das Wort getrennt. Das ist daher von Vorteil, da wir so später
            # beim Zusammenfügen der Anzahl und des Namens nicht jedes Wort
            # einzeln hinzufügen müssen
            item_name = item.split(' ', 1)[1]
        else:
            item_name = item

        for field in array:
            if len(field.split(' ')) > 1:
                field_name = field.split(' ', 1)[1]
            else:
                field_name = field

            # Die folgende if-Abfrage ist notwendig, um auch "Banane" und "Bananen"
            # zusammen zu zählen
            if field_name.lower().rstrip(field_name.lower()[-1]) == item_name.lower():
                item_name = item_name + "n"
            if field_name.lower() == item_name.lower():
                # Festlegen der Anzahl des jeweiligen Feldes der beiden Arrays und
                # des letzten Buchstaben, den wir später noch brauchen werden
                n_anz = item.split(' ', 1)[0]
                try:
                    n_item = item.split(' ', 1)[1]
                except:
                    n_item = item
                a_anz = field.split(' ', 1)[0]
                last_letter = item[-1]
                # Bisher war die jeweilige Anzahl (z.B. 2) noch als String (also
                # Zeichen) und nicht als int (also Zahl) gespeichert. Man kann
                # aber nur mit Zahlen rechnen, daher versuche ich anschließend
                # die Strings in Integer zu konvertieren. "try" wird benötigt,
                # da zum Beispiel bei "Creme Legere" das 1. Feld nach dem split
                # keine Zahl, sondern ein Wort ist
                try:
                    n_anz = int(n_anz)
                except:
                    # keine Zahl? Dann gibt es von dem Item nur eines
                    n_anz = 1

                try:
                    a_anz = int(a_anz)
                except:
                    a_anz = 1

                if type(n_anz) != int:
                    n_item = item

                new_anz = n_anz + a_anz
                item = str(new_anz) + " " + n_item

                if last_letter == "e":
                    item = item + "n"

        new_array.append(item)
        # folgende Zeile löscht Dopplungen, die durch das Zusammenfügen von "Banane" und "Bananen" zu stande kommt
        new_array = delete_duplications(new_array)
    return new_array


def assamble_array(array):
    temp_array = []
    temp_array0 = array
    for item in temp_array0:
        item = item.replace('1', '')
        item = item.replace('2', '')
        item = item.replace('3', '')
        item = item.replace('4', '')
        item = item.replace('5', '')
        item = item.replace('6', '')
        item = item.replace('7', '')
        item = item.replace('8', '')
        item = item.replace('9', '')
        item = item.replace('0', '')
        item = item.strip()
        temp_array.append(item)
    duplications = delete_duplications(temp_array)
    temp3_array = []
    if len(duplications) >= 1:
        temp2_array = assamble_new_items(array, duplications)
        for item in temp2_array:
            try:
                anz = int(item.split(' ', 1)[0])
            except:
                anz = 1
            anz -= 1

            if anz == 1:
                item = item.split(' ')[1]
            else:
                item = str(anz) + " " + item.split(' ', 1)[1]
            temp3_array.append(item)

    return temp3_array
    
def delete_duplications(array):
    new_array = list(set(array))
    return new_array
    

def get_text_beetween(start_word, text, end_word='', output='array'):
    ausgabe = []
    index = -1
    text = text.split(' ')
    for i in range(len(text)):
        if text[i] is start_word:
            index = i + 1
    if index is not -1:
        if end_word is '':
            while index <= len(text):
                ausgabe.append(text[index])
                index += 1
        else:
            founded = False
            while index <= len(text) and not founded:
                if text[index] is end_word:
                    founded = True
                else:
                    ausgabe.append(text[index])
                    index += 1
    if output is 'array':
        return ausgabe
    elif output is 'String':
        ausgabe_neu = ''
        for item in ausgabe:
            ausgabe += item + ' '
        return ausgabe
