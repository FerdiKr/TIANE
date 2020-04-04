import math # Wird wegen eval gebraucht
import re

PRIORITY = 5

termFinder = re.compile(r'.*?((\d|\(|-|minus|sinus|pi|cosinus|kosinus|tangens|kubikwurzel|quadratwurzel|wurzel|ein|null|antwort|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf).*)', re.I)
bruchFinder = re.compile(r'^(.*?)(\d+|ein|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf) (ganzes|ganze|halbes|halbe|halb|drittel|viertel|fünftel|sechstel|siebtel|achtel|neuntel|zehntel|elftel|zwölftel|4tel|5tel|6tel|8tel|9tel|10tel|11tel|12tel)(.*?)$', re.I)
funktionsFinder = re.compile(r'^(.*?)(der tangens von|tangens von|tangens|der cosinus von|cosinus von|cosinus|der kosinus von|kosinus von|kosinus|der sinus von|sinus von|sinus|die kubikwurzel von|kubikwurzel von|die kubikwurzel aus|kubikwurzel aus|kubikwurzel|die quadratwurzel von|quadratwurzel von|die quadratwurzel aus|quadratwurzel aus|quadratwurzel|die wurzel von|wurzel von|die wurzel aus|wurzel aus|wurzel)\s+(-?\d+\.?\d*)(.*?)$', re.I)

numeratorMap = {
    'ein': '1',
    'zwei': '2',
    'drei': '3',
    'vier': '4',
    'fünf': '5',
    'sechs': '6',
    'sieben': '7',
    'acht': '8',
    'neun': '9',
    'zehn': '10',
    'elf': '11',
    'zwölf': 12
}

denomintorMap = {
    'ganze': '1',
    'ganzes': '1',
    'halb': '2',
    'halbe': '2',
    'halbes': '2',
    'drittel': '3',
    'viertel': '4',
    '4tel': '4',
    'fünftel': '5',
    '5tel': '5',
    'sechstel': '6',
    '6tel': '6',
    'siebtel': '7',
    'achtel': '8',
    '8el': '8',
    '8tel': '8',
    'neuntel': '9',
    '9tel': '9',
    'zehntel': '10',
    '10tel': '10',
    'elftel': '11',
    '11tel': '11',
    'zwölftel': '12',
    '12tel': '12',
}

def handle(txt, tiane, profile):
    tt = txt.replace('?', (''))
    tt = tt.replace('!', (''))
    tt = tt.replace('"', (''))
    tt = tt.replace('â‚¬', ('Euro'))
    tt = tt.replace('%', ('Prozent'))
    tt = tt.replace('$', ('Dollar'))
    text = tt.lower()
    match = termFinder.match(text)
    if (match is None):
        tiane.say("Ich kenne das Ergebnis nicht.")
        return
    text = match.group(1)
    text = text.replace('klammer auf', '(')
    text = text.replace('klammer zu', ')')
    text = text.replace(' x ', '*')
    text = text.replace('plus', '+')
    text = text.replace('und', '+')
    text = text.replace('minus', '-')
    text = text.replace('geteilt durch', '/')
    text = text.replace('durch', '/')
    text = text.replace('mal', '*')
    text = text.replace('hoch', '**')
    text = text.replace('zum quadrat', '**2')
    text = text.replace('quadrat', '**2')

    text = text.replace(' die antwort ', '42')
    text = text.replace(' antwort ', '42')

    text = text.replace('null', '0')

    match = bruchFinder.match(text)
    while match is not None:
        replacement = '(' + numeratorMap.get(match.group(2), match.group(2)) + '/' + denomintorMap.get(match.group(3), '1') + ')'
        text = match.group(1) + replacement + match.group(4)
        match = bruchFinder.match(text)

    text = text.replace('eins', '1')
    text = text.replace('zwei', '2')
    text = text.replace('drei', '3')
    text = text.replace('vier', '4')
    text = text.replace('fünf', '5')
    text = text.replace('sechs', '6')
    text = text.replace('sieben', '7')
    text = text.replace('acht', '8')
    text = text.replace('neun', '9')
    text = text.replace('zehn', '10')
    text = text.replace('elf', '11')
    text = text.replace('zwölf', '12')

    text = text.replace('pi', ' math.pi ')

    text = text.replace('komma', '.')
    text = text.replace(',', '.')
    while (' .' in text):
        text = text.replace(' .', '.')
    while ('. ' in text):
        text = text.replace('. ', '.')

    match = funktionsFinder.match(text)
    while match is not None:
        funktionRaw = match.group(2)
        funktion1 = ''
        funktion2 = ''
        if 'tangens' in funktionRaw:
            funktion1 = 'math.tan(math.radians'
            funktion2 = ')'
        elif 'kosinus' in funktionRaw or 'cosinus' in funktionRaw:
            funktion1 = 'math.cos(math.radians'
            funktion2 = ')'
        elif 'sinus' in funktionRaw:
            funktion1 = 'math.sin(math.radians'
            funktion2 = ')'
        elif 'kubikwurzel' in funktionRaw:
            funktion2 = '**(1.0/3.0)'
        elif 'wurzel' in funktionRaw:
            funktion2 = '**(0.5)'
        if funktion1 != '' or funktion2 != '':
            text = match.group(1) + funktion1 + '(' + match.group(3) + ')' + funktion2 + match.group(4)
            match = bruchFinder.match(text)
        else:
            match = None

    print(text)

    try:
        result = eval(text)
    except ZeroDivisionError:
        tiane.say('Möchtest du ein Wurmloch kreieren? Etwas durch null zu teilen beschwört Dämonen!')
        return
    except:
        tiane.say('Das kann ich nicht berechnen.')
        return

    resultStr = '{:.8f}'.format(result)
    while (resultStr.endswith('0')):
        resultStr = resultStr[:-1]
    if (resultStr.endswith('.')):
        resultStr = resultStr[:-1]
    if ('.' in resultStr):
        tokens = resultStr.split('.', 1)
        resultStr = tokens[0] + ' komma ' + (' '.join(tokens[1]))
    if (resultStr.startswith('-')):
        resultStr = 'minus ' + resultStr[1:]
    tiane.say(resultStr)

def isValid(text):
    text = text.lower()
    if not 'wie viel ist' in text and not 'wie viel ergibt' in text and not 'was ergibt' in text and not 'was macht' in text and not 'was ist' in text and not 'was sind' in text:
        return False
    if '+' in text or '*' in text or ' x ' in text or '- ' in text or ' / ' in text or ' geteilt ' in text or ' hoch ' in text or ' minus ' in text or ' plus ' in text or ' durch ' in text or 'wurzel ' in text or 'sinus ' in text or ' tangens ' in text or ' quadrat ' in text:
        return True
    if bruchFinder.match(text) is not None:
        return True
    return False

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '08', 'hour': '06', 'year': '2018', 'minute': '00', 'day': '27'}, 'town': 'None'}

    def say(self, text):
        print(text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('0 / 0', tiane, profile)

if __name__ == '__main__':
    main()
