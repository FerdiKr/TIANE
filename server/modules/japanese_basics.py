PRIORITY = 2

import random
import datetime


def handle(text, tiane, profile):
    zahlen = {1: 'itschi', 2: 'ni', 3: 'san', 4: 'jonn', 5: 'go', 6: 'rokü', 7: 'nanna', 8: 'ha', 9: 'kjüü', 10: 'shiuu', 77: 'tchiiji', 88: 'hatschi', 99: 'kü'}
    n = datetime.datetime.now()
    text = text.lower()
    translation = ''
    if 'hallo' in text:
        translation = 'konnitchiwa!'
    elif 'guten morgen' in text:
        translation = 'ohaioogosaimas!'
    elif 'dich zu treffen' in text or 'dich kennenzulernen' in text or 'dich kennen zu lernen' in text:
        translation = random.choice(['hashimemashtee!', 'joroschkü onegaischimas'])
    elif 'danke' in text:
        translation = 'doomoarigato!'
    elif 'deinen namen' in text or 'dich vorstellen' in text or 'stell dich vor' in text:
        translation = random.choice(['wataschiwa Tiane des.', 'Tiane tooiiimas.'])
    elif 'frag' in text and 'name' in text or 'was ist' in text and 'name' in text or 'wie' in text and 'heiß' in text:
        translation = 'onamaee wa nandeska?'
    elif 'wie alt' in text and 'du' in text:
        translation = 'itschi sai des'
    elif 'klara' in text and 'alt' in text:
        translation = 'Klara san wa shiu hatschi sai des'
    elif 'ferdi' in text and 'alt' in text:
        translation = 'Ferdi san wa ni shiu sai des'
    elif 'fragen' in text or 'befinden' in text or 'wie geht es dir' in text or 'geht es dir gut' in text or 'gut geht' in text:
        translation = 'genkideska?'
    elif 'deutsch' in text or 'sprache' in text:
        translation = 'doitsugo ohanashimas'
    elif 'herkomm' in text or 'aus deutschland' in text:
        translation = 'doitsu schushindes'
    elif 'uhr' in text or 'zeit' in text:
        if n.hour >= 13:
            h = n.hour - 12
        else:
            h = n.hour
        if h == 7:
            h = 77
        elif h == 8:
            h = 88
        elif h == 9:
            h == 99
        if n.minute == 0:
            translation = 'iima wa ' + zahlen[h] + 'tshii des'
        else:
            if n.minute <= 10:
                translation = 'iima wa ' + zahlen[h] + 'tshii ' + zahlen[n.minute] + ' pünn des'
            elif n.minute == 30:
                translation = 'iima wa ' + zahlen[h] + 'tshii hann des'
            else:
                m = str(n.minute)
                if m[0] == '1':
                    m_a = 'shiuu '
                else:
                    m_a = zahlen[int(m[0])] + ' shiuu '
                m_b = zahlen[int(m[1])]
                translation = 'iima wa ' + m_a + m_b + ' pünn des'
    tiane.say(translation)


def isValid(text):
    text = text.lower()
    if 'japanisch' in text or 'japan' in text:
        return True

def main():
    Tiane = TIANE()
    handle('Uhrzeit auf japanisch', Tiane, {})

class TIANE:
    def __init__(self):
        pass
    def say(self, text):
        print(text)

if __name__ == '__main__':
    main()
