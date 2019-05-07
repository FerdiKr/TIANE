import random


def reply(txt, tiane):
    output = ''
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
    t = str.split(text)
    ind = 1
    a = False
    g_g = 'Mutig und tapfer schreiten wir hin, haben als Ziel den Sieg im Sinn, rot und gold auf unsrer Fahne, wir Gryffindors sind erste Sahne.'
    r_g = 'Witzigkeit im Übermaß ist des Menschen größter Schatz.'
    h_g = 'In Hufflepuff ist man gerecht und treu, man hilft den anderen wo man kann und hat vor Arbeit keine Scheu.'
    s_g = 'In Slytherin weiß man noch List und Tücke zu verbinden, dafür wirst du hier noch echte Freunde finden.'
    satz = {}
    rep = False
    if 'gryffindor' in text:
        output = g_g
        a = False
    elif 'ravenclaw' in text:
        output = r_g
        a = False
    elif 'hufflepuff' in text:
        output = h_g
        a = False
    elif 'slytherin' in text:
        output = s_g
        a = False
    elif 'hogwarts' in text:
        if 'in welchem hogwarts haus bist du' in text:
            output = 'Ich bin eine Ravenclaw. ' + r_g
        elif 'in welchem hogwarts haus bin ich' in text:
            output = random.choice(['Wie würdest du dich denn einschÃ¤tzen?', 'In welchem Haus wärst du denn gerne?', 'Wo wärst du denn gerne?', 'Wo ist denn dein Lieblingscharakter?'])
            a = True
        elif 'kennst du hogwarts' in text:
            output = 'Selbstverständlich kenne ich Hogwarts. ' + 'In welchem Hogwarts Haus bist du?'
            a = True
        elif 'ich will nach hogwarts' in text:
            output = 'Das kann ich nachvollziehen, ich wäre jetzt auch lieber auf einer Zaubererschule.'
            a = False
        else:
            output = random.choice(['Accio Feuerblitz', 'Alohomora', 'Nach all dieser Zeit?'])
            a = False
    elif 'dumbledore' in text:
        d_1 = 'Es sind nicht unsere Fähigkeiten, die zeigen wer wir sind, sondern unsere Entscheidungen.'
        d_2 = 'Obgleich wir von verschiedenen Orten kommen und verschiedene Sprachen sprechen, unsere Herzen schlagen gemeinsam.'
        d_3 = 'Es tut nicht gut, nur seinen Träumen nachzuhängen und zu vergessen zu leben.'
        output = random.choice([d_1, d_2, d_3])
        a = False
    elif 'nach all dieser zeit' in text or 'nach all der zeit' in text:
        output = 'immer.'
        a = False
    elif 'after all this time' in text:
        output = 'always.'
        a = False
    dic = {'output': output, 'a': a}
    return dic

def handle(text, tiane, profile):
    g_g = 'Mutig und tapfer schreiten wir hin, haben als Ziel den Sieg im Sinn, rot und gold auf unsrer Fahne, wir Gryffindors sind erste Sahne.'
    r_g = 'Witzigkeit im Übermaß ist des Menschen größter Schatz.'
    h_g = 'In Hufflepuff ist man gerecht und treu, man hilft den anderen wo man kann und hat vor Arbeit keine Scheu.'
    s_g = 'In Slytherin weis man noch List und Tücke zu verbinden, dafür wirst du hier noch echte Freunde finden.'
    b = False
    dic = reply(text, tiane)
    ausgabe = dic.get('output')
    a = dic.get('a')
    tiane.say(ausgabe)
    if a == True:
        neuertext = tiane.listen()
        if neuertext == 'TIMEOUT_OR_INVALID':
            tiane.say('Das habe ich leider nicht verstanden')
            b = False
        else:
            tt = neuertext.replace('.', (''))
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
            nt = tt.lower()
            if 'gryffindor' in nt:
                output_zwei = g_g
                output_drei = 'Ich bin eine Ravenclaw.'
            elif 'ravenclaw' in nt:
                output_zwei = r_g
                output_drei = 'Ich bin auch eine Ravenclaw.'
            elif 'hufflepuff' in nt:
                output_zwei = h_g
                output_drei = 'Ich bin eine Ravenclaw.'
            elif 'slytherin' in nt:
                output_zwei = s_g
                output_drei = 'Ich bin eine Ravenclaw.'
            else:
                output_zwei = 'Ich bin mir nicht sicher ob ich dich richtig verstanden habe.'
                output_drei = 'In welchem Hogwarts Haus bist du?'
                b = True
            tiane.say(output_zwei)
            tiane.say(output_drei)
    if b == True:
        neuertext_zwei = tiane.listen()
        if neuertext_zwei == 'TIMEOUT_OR_INVALID':
            tiane.say('Das habe ich leider nicht verstanden')
        else:
            tt = neuertext_zwei.replace('.', (''))
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
            nt_z = tt.lower()
            if 'gryffindor' in nt_z:
                oz = g_g
                od = 'Ich bin eine Ravenclaw.'
            elif 'ravenclaw' in nt_z:
                oz = r_g
                od = 'Ich bin auch eine Ravenclaw.'
            elif 'hufflepuff' in nt_z:
                oz = h_g
                od = 'Ich bin eine Ravenclaw.'
            elif 'slytherin' in nt_z:
                oz = s_g
                od = 'Ich bin eine Ravenclaw.'
            else:
                oz = 'Es tut mir Leid.'
                od = 'Ich habe dein Hogwarts Haus leider nicht verstehen können.'
            tiane.say(oz)
            tiane.say(od)
        


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
    if 'hogwarts' in text or 'dumbledore' in text or 'ravenclaw' in text or 'gryffindor' in text or 'hufflepuff' in text or 'slytherin' in text or 'nach all der zeit' in text or 'nach all dieser zeit' in text:
        return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '08', 'hour': '06', 'year': '2018', 'minute': '00', 'day': '27'}, 'town': 'None'}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Nach all der Zeit', tiane, profile)
    
    
if __name__ == "__main__":
    main()
