import random

def isValid(text):
    text = text.lower()
    if 'witz' in text and ('kennst' in text or 'erzähl' in text):
        return True

def handle(text, tiane, profile):
    jokes = ['Anruf bei der Hotline. Kunde: "Ich benutze Windows." Hotline: "Ja." Kunde: "Mein Computer funktioniert nicht richtig." Hotline: "Das sagten Sie bereits ..."',
             'Behauptung: Jedes Programm läßt sich um eine Anweisung kürzen. Jedes Programm hat mindestens einen Fehler. Durch Induktion können wir schließen: Jedes Programm ist reduzierbar auf eine Anweisung, die nicht funktioniert.',
             'Wie viele Informatiker braucht man, um eine Glühbirne zu wechseln? Keinen, das ist ein Hardwareproblem!']
    tiane.say(random.choice(jokes))
