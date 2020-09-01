import datetime
import json
import re
from urllib.request import urlopen, Request

# Wir brauchen mindestens 3, weil hanoi 2 hat und bereits auf das Wort platz reagiert.
PRIORITY = 3


numberDotPattern = re.compile('\s*(\d+)\s*\.?\s*', re.I)

platz1Pattern = re.compile(r'wer führt in (.+)', re.I)
platz18Pattern = re.compile(r'wer ist letzter? in (.+)', re.I)
platzX1Pattern = re.compile(r'wer ist (auf)? (platz|rang|position) (.+?) in (.+)', re.I)
platzX2Pattern = re.compile(r'wer ist auf (dem|der) (.+?) (platz|rang|platzierung) in (.+)', re.I)
vereinPattern = re.compile(r'auf (welchem platz|welchem rang|welcher platzierung|welcher position) ist (.+?) in (.+)', re.I)

def getNumber(text):
    numberMap = {
        'ein': 1,
        'eins': 1,
        'zwei': 2,
        'drei': 3,
        'vier': 4,
        'fünf': 5,
        'sechs': 6,
        'sieben': 7,
        'acht': 8,
        'neun': 9,
        'zehn': 10,
        'elf': 11,
        'zwölf': 12,
        'ersten': 1,
        'zweiten': 2,
        'dritten': 3,
        'vierten': 4,
        'fünften': 5,
        'sechsten': 6,
        'siebten': 7,
        'achten': 8,
        'neunten': 9,
        'zehnten': 10,
        'elften': 11,
        'zwölften': 12,
        'dreizehnten': 13,
        'vierzehnten': 14,
        'fünfzehnten': 15,
        'sechzehnten': 16,
        'siebzehnten': 17,
        'achtzehnten': 18,
        'erste': 1,
        'zweite': 2,
        'dritte': 3,
        'vierte': 4,
        'fünfte': 5,
        'sechste': 6,
        'siebte': 7,
        'achte': 8,
        'neunte': 9,
        'zehnte': 10,
        'elfte': 11,
        'zwölfte': 12,
        'dreizehnte': 13,
        'vierzehnte': 14,
        'fünfzehnte': 15,
        'sechzehnte': 16,
        'siebzehnte': 17,
        'achtzehnte': 18,
    }
    match = numberDotPattern.match(text)
    if match is not None:
        return int(match.group(1))
    else:
        return numberMap.get(text.strip().lower(), None)

def getLigaId(txt):
    # Es wird leider nur Fußball halbwegs regelmäßig eingetragen...
    text = txt.lower()
    if 'bundesliga' in text:
        if 'zweite' in text:
            return 'bl2'
        elif 'dritte' in text:
            return 'bl3'
        else:
            return 'bl1'
    elif 'champions league' in text:
        year = str(datetime.datetime.now().year)
        return ['cl', 'cl-' + year, 'cl' + year, 'cl-' + year[2:], 'cl' + year[2:], 'ucl-' + year, 'ucl' + year, 'ucl-' + year[2:], 'ucl' + year[2:]]
    elif 'fußball' in text or 'fussball' in text:
        if 'weltmeisterschaft' in text or ' wm ' in text:
            year = str(datetime.datetime.now().year)
            return ['wm-' + year, 'wm' + year, 'wm-' + year[2:], 'wm' + year[2:]]
        elif 'europameisterschaft' in text or 'europa meisterschaft' in text or ' em ' in text:
            year = str(datetime.datetime.now().year)
            return ['em-' + year, 'em' + year, 'em-' + year[2:], 'em' + year[2:], 'uefa-euro--' + year, 'uefa-euro-' + year]
    else:
        return None

def getMatch(text):
    match = platz1Pattern.match(text)
    if match is not None:
        return 1, getLigaId(match.group(1)), None
    match = platz18Pattern.match(text)
    if match is not None:
        return -1, getLigaId(match.group(1)), None
    match = platzX1Pattern.match(text)
    if match is not None:
        return getNumber(match.group(3)), getLigaId(match.group(4)), None
    match = platzX2Pattern.match(text)
    if match is not None:
        return getNumber(match.group(4)), getLigaId(match.group(4)), None
    match = vereinPattern.match(text)
    if match is not None:
        return None, getLigaId(match.group(3)), match.group(2)
    return None, None, None

def ligaResult(rangRaw, liga, verein, hasTriedLastYear=False):
    if (hasTriedLastYear):
        year = str(datetime.datetime.now().year - 1)
    else:
        year = str(datetime.datetime.now().year)

    if rangRaw is not None and rangRaw >= 0:
        rang = rangRaw - 1
    else:
        rang = rangRaw

    request = Request('https://www.openligadb.de/api/getbltable/' + liga + '/' + year)
    request.add_header('Accept', 'application/json,text/json,application/x-json,text/x-json')
    try:
        response = urlopen(request)
    except:
        return None

    js = json.load(response)
    if (len(js) == 0):
        if not hasTriedLastYear:
            return ligaResult(rangRaw, liga, verein, hasTriedLastYear=True)
        else:
            return None

    team = None
    teamRang = None
    if rang is not None:
        try:
            team = js[rang]
            teamRang = ((rang + len(js)) % len(js)) + 1
        except IndexError or KeyError:
            return 'So viele Vereine spielen nicht in dieser Liga.'
    elif verein is not None:
        hadExc = False
        for t in range(len(js)):
            try:
                if js[t]['TeamName'].lower() in verein.lower() or ('ShortName' in js[t] and js[t]['ShortName'] is not None and js[t]['ShortName'].lower() in verein.lower()):
                    team = js[t]
                    teamRang = t + 1
            except IndexError or KeyError:
                hadExc = True
        if team is None:
            if (hadExc):
                return None
            else:
                return 'Den Verein kenne ich nicht.'

    if team is not None:
        try:
            shortName = team['TeamName']
            if 'ShortName' in team  and team['ShortName'] is not None:
                shortName = team['ShortName']
            return team['TeamName'] + ' ist mit ' + str(team['Points']) + ' Punkten auf Platz ' + str(teamRang) + ' . '\
                   + shortName + ' konnte ' + str(team['Won']) + ' Siege erzielen und musste ' + str(team['Lost'])\
                   + ' Niederlagen einstecken.'
        except IndexError or KeyError:
            return None
    else:
        return None


def isValid(text):
    text = text.lower()
    return 'bundesliga' in text or \
        (('fussball' in text or 'fußball' in text) and ('weltmeisterschaft' in text or ' wm ' in text or 'europameisterschaft' in text or 'europa meisterschaft' in text or ' em ' in text)) or \
        'champions league' in text

def handle(text, tiane, profile):
    rang, liga, verein = getMatch(text)

    if liga is None:
        tiane.say('Das kann ich dir nicht sagen, Sportsfreund.')
    elif isinstance(liga, list):
        for l in list(liga):
            out = ligaResult(rang, l, verein)
            if out is not None:
                tiane.say(out)
                return
    else:
        out = ligaResult(rang, liga, verein)
        if out is not None:
            tiane.say(out)
            return

    tiane.say('Das kann ich dir nicht sagen, Sportsfreund.')


