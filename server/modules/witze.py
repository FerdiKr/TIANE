import random
import datetime

def isValid(text):
    text = text.lower()
    if 'witz' in text and ('kennst' in text or 'erzähl' in text):
        return True

def handle(text, tiane, profile):
    now = datetime.datetime.now()
    year = now.year - 1
    jokes = ['Anruf bei der Hotline. Kunde: "Ich benutze Windows." Hotline: "Ja." Kunde: "Mein Computer funktioniert nicht richtig." Hotline: "Das sagten Sie bereits ..."',
             'Behauptung: Jedes Programm läßt sich um eine Anweisung kürzen. Jedes Programm hat mindestens einen Fehler. Durch Induktion können wir schließen: Jedes Programm ist reduzierbar auf eine Anweisung, die nicht funktioniert.',
             'Wie viele Programmierer braucht man, um eine Glühbirne zu wechseln? Keinen, das ist ein Hardwareproblem!',
             'Wie viele Informatik-Studentinnen braucht man, um eine Glühbirne zu wechseln? Alle beide!',
             'Mein größter Neujahrsvorsatz für das Jahr ' + str(year) + ' ist, dass ich keine Off-By-One-Fehler mehr mache.',
             'Windows ist wie ein U-Boot. Kaum macht man ein Fenster auf, gehen die Probleme los.',
             'Wo ist der beste Ort, um eine Leiche zu verstecken? Seite 2 bei Google.',
             'Wie zieht ein Informatiker seine Freundin aus? getStringFromObject();',
             'Was ist die Lieblingsbeschäftigung von Bits? Busfahren!',
             'Was antwortet ein Informatiker, wenn man ihn fragt, ob sein Kind ein Mädchen oder ein Junge ist? Wahr!',
             'Chuck Norris\' Bits haben drei Zustände.',
             'Du machst mein int zum long.',
             'Es gibt 10 Arten von Menschen, die, die Binär verstehen und die, die bis 9 zählen.',
             'Warum mögen Frauen objektorientierte Programmierung? Weil sie Klasse haben.',
             '2b||!2b',
             'Was schreit ein ertrinkender Informatiker? F1! F1! F1!',
             'Was sind acht Hobbits? Ein Hobbyte!',
             '/* no comment */',
             'Was sind die drei natürlichen Feinde eines Informatikers? 0. Licht 1. Luft 2. Vogellärm 3. Off-by-one-errors',
             'Wir haben drei Informatiker gefragt, ob sie drei Bier wollen. Sagt der erste "Weiß ich nicht", sagt der zweite "Weiß ich nicht", sagt der dritte "Ja, bitte!"',
             'Was isst ein Informatiker zum Film? Mikrochips.',
             'Warum verwechseln Informatiker Halloween und Weihnachten? oct(31)=dec(25)',
             '1337*Pi/100 = 42',
             'Was macht eine Ente auf dem Router? NAT NAT NAT NAT NAT!',
             'H T M L ist eine ernstzunehmende Programmiersprache.']
    tiane.say(random.choice(jokes))
