import json
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

_PATTERNS = [
    (re.compile(r'^wo (ist|liegt|befindet sich) (.+?)[.?]?$', re.I), 2),
    (re.compile(r'^(.+?) (liegt|ist) wo[.?]?$', re.I), 1)
]

def isValid(txt):
    text = txt.lower()
    for pattern, groupId in _PATTERNS:
            match = pattern.match(text)
            if match is not None:
                return True
    return False

def handle(text, tiane, local_storage):
    # Wenn es ein direkter aufruf von wo_ist.py ist, muss der prefix
    # entfernt werden. Grund dafür ist Issue #142
    if (text.startswith('§DIRECTCALL_FROM_WO_IST§')):
        text = text[len('§DIRECTCALL_FROM_WO_IST§'):]

    ort = None
    if 'town' in tiane.analysis:
        ort = tiane.analysis['town']
        if ort == '':
            ort = None
    for pattern, groupId in _PATTERNS:
        if ort is None:
            match = pattern.match(text)
            if match is not None:
                ort = match.group(groupId)
                break
    if ort is None:
        tiane.say('Entschuldigung, das habe ich nicht verstanden.')
    else:
        request = Request('https://nominatim.openstreetmap.org/search?q=' + quote(ort) + '&format=json&addressdetails=1&extratags=1&namedetails=1&accept-language=de-DE&dedupe=1')
        response = urlopen(request)
        answer = json.loads(response.read())
        print('DER ORT IST {}'.format(ort))
        if (len(answer) == 0):
            tiane.say('Diesen Ort kenne ich nicht. Wenn du weißt, wo er liegt, hilf mir doch und trage ihn auf Open Street Map ein.')
        else:
            strMap = {
                # Format values:
                # 0: Der vom Nutzer angegebene Name.
                # 1: Name
                # 2: First available of: island, city, town, city_district, suburb, peak
                # 3: First available of: city, town
                # 4: county
                # 5: state
                # 6: country
                # 7: capital
                # 8: Nomen für state (Länderspezifisch). Standard: 'eine Region'
                # 9: Nomen für county (Länderspezifisch, ohne Artikel). Standard: 'Bezirk'
                'continent': '{1} ist ein Kontinent.',
                'country': '{1} ist ein Land.',
                'country_with_capital': '{1} ist ein Land mit der Hauptstadt {7}.',
                'state': '{1} ist {8} in {4}.',
                'administrative': '{1} ist {8} in {4}.',
                'region': '{1} ist ein Gebiet in {5}, {6}.',
                'province': '{1} ist ein Gebiet in {5}, {6}.',
                'county': '{1} ist ein {9} in {5}, {6}.',
                'city': '{1} ist eine Stadt in {5}, {6}.',
                'town': '{1} ist eine Stadt in {5}, {6}.',
                'village': '{1} ist ein Ort im {9} {4} in {5}, {6}.',
                'hamlet': '{1} ist ein kleiner Ort im {9} {4} in {5}, {6}.',
                'isolated_dwelling': ' {1} ist eine kleine Siedlung im {9} {4} in {5}, {6}.',
                'farm': '{1} ist ein Bauernhof im {9} {4} in {5}, {6}.',
                'island': '{1} ist eine Insel in {5} bei {6}.',
                'archipelago': '{1} ist eine Inselgruppe in {5} bei {6}.',
                'islet': '{1} ist eine kleine Insel in {5} bei {6}.',
                'sea': '{1} ist ein Ozean.',
                'ocean': '{1} ist ein Weltmeer.',
                'borough': '{1} ist ein größerer Stadtteil von {3} in {5}, {6}.',
                'suburb': '{1} ist ein Stadtteil von {3} in {5}, {6}.',
                'quarter': '{1} ist ein Stadtviertel von {3} in {5}, {6}.',
                'neighbourhood': '{1} ist ein kleines Stadtviertel von {3} in {5}, {6}.',
                'municipality': '{1} ist eine Gemeinde im {9} {4} in {5}, {6}.'
            }
            try:
                answer = answer[0]
                data = answer['address']

                type = answer['type']
                if type.lower() == 'administrative' and 'linked_place' in answer['extratags']:
                    type = answer['extratags']['linked_place']
                elif (type.lower() == 'city' or type.lower() == 'town' or type.lower() == 'administrative') and 'place' in answer['extratags']:
                    type = answer['extratags']['place']
                elif type.lower() == 'administrative' and len(data) == 2 and 'country' in data and 'country_code' in data:
                    type = 'country'
                elif type.lower() == 'administrative' and len(data) == 1 and 'country' in data:
                    type = 'country'

                if not type.lower() in strMap:
                    tiane.say('Da fällt mir etwas zu ein, aber es ist besser du suchst es selbst. Ich vermute mein Ergebnis ist nicht das, was du suchst.')
                    return

                f1 = answer['namedetails']['name']
                if 'name:de' in answer['namedetails']:
                    f1 = answer['namedetails']['name:de']

                f2 = ''
                if 'island' in data:
                    f2 = data['island']
                elif 'city' in data:
                    f2 = data['city']
                elif 'town' in data:
                    f2 = data['town']
                elif 'city_district' in data:
                    f2 = data['city_district']
                elif 'suburb' in data:
                    f2 = data['suburb']
                elif 'peak' in data:
                    f2 = data['peak']

                f3 = ''
                if 'city' in data:
                    f3 = data['city']
                elif 'town' in data:
                    f3 = data['town']

                f4 = ''
                if 'county' in data:
                    f4 = data['county']

                f5 = ''
                if 'state' in data:
                    f5 = data['state']

                f6 = ''
                if 'country' in data:
                    f6 = data['country']

                f7 = ''
                if 'capital_city' in answer['extratags']:
                    f7 = answer['extratags']['capital_city']

                f8 = 'eine Region'
                f9 = 'Bezirk'
                if ('country_code' in data):
                    cc = data['country_code'].lower()
                    if cc == 'de':
                        f8 = 'ein Bundesland'
                        f9 = 'Landkreis'
                    elif cc == 'at':
                        f8 = 'ein Bundesland'
                    elif cc == 'ch':
                        f8 = 'ein Kanton'
                    elif cc == 'us':
                        f8 = 'ein Bundestaat'
                    elif cc == 'es':
                        f8 = 'eine Provinz'

                if type.lower() == 'administrative' and 'name:prefix' in answer['extratags']:
                    f8 = 'ein {}'.format(answer['extratags']['name:prefix'])

                if type == 'country' and f7 != '':
                    type = 'country_with_capital'

                tiane.say(strMap[type.lower()].format(ort, f1, f2, f3, f4, f5, f6, f7, f8, f9))
            except KeyError:
                tiane.say('Es ist ein Fehler aufgetreten.')



