import datetime
import random

def isValid(text):
    text = text.lower()
    if 'wie' in text and 'heißt' in text and 'du' in text:
        return True
    if ('wer' in text or 'was' in text) and 'bist' in text and 'du' in text:
        return True
    if ('woher' in text or 'bedeutet' in text or 'heißt' in text) and ' name' in text :
        return True
    if (('was' in text and 'für' in text) or ('wie' in text and 'heißt' in text) or 'welches' in text) and 'buch' in text:
        return True
    if ('was' in text and 'kannst' in text and 'du' in text) or 'verstehst du' in text or ('was' in text and 'funktionen' in text) or ('was' in text and 'fragen' in text):
        return True
    if '😂' in text:
        return True
    if 'wie' in text and 'alt' in text and 'du' in text:
        return True
    if ' aha' in text or 'aha?' in text:
        return True
    if 'bist' in text and 'dumm' in text:
        return True
    if 'bist' in text and 'toll' in text or 'bist' in text and 'genial' in text:
        return True
    if 'liebe' in text and 'dich' in text:
        return True
    if 'sag ' in text and 'was' in text or 'sage ' in text and 'was' in text or 'erzähl' in text and 'was' in text:
        if 'nettes' in text or 'liebes' in text or 'freundliches' in text:
            return True
    if 'hast' in text and 'recht' in text:
        return True
    if ('sicher' in text or 'verschlüsselt' in text) and ('chat' in text or 'kanal' in text or 'verbindung' in text):
        return True

def handle(text, tiane, profile):
    text = text.lower()
    if 'wie' in text and 'heißt' in text and 'du' in text:
        tiane.say('Ich heiße TIANE.')
    elif ('wer' in text or 'was' in text) and 'bist' in text and 'du' in text:
        tiane.say('Ich bin TIANE, ein Open-Source-Sprachassistent!')
    elif ('woher' in text or 'bedeutet' in text or 'heißt' in text) and ' name' in text :
        tiane.say('Anders als man denken könnte, ist mein Name tatsächlich keine Abkürzung für irgendwas. '
                  'Aber er ist angelehnt an einen sprechenden Computer namens "DIANE" aus einem von Ferdis Lieblingsbüchern.')
    elif (('was' in text and 'für' in text) or ('wie' in text and 'heißt' in text) or 'welches' in text) and 'buch' in text:
        tiane.say('"Limit" von Frank Schätzing.')
    elif ('was' in text and 'kannst' in text and 'du' in text) or 'verstehst du' in text or ('was' in text and 'funktionen' in text) or ('was' in text and 'fragen' in text):
        tiane.say('Sagen wir mal so, den Turing-Test bestehe ich leider noch nicht... '
                  'Aber ich kann dir zum Beispiel das Wetter ansagen, ein paar allgemeine Wissensfragen beantworten '
                  'rechnen, würfeln und so weiter. '
                  'Und für alles weitere bist du gerne eingeladen, selbst auf in meinem GitHub-Repository aktiv zu werden!')
    elif '😂' in text:
        tiane.say('Warum lachst du? 😂')
        response = tiane.listen()
        tiane.say('Aha...')
    elif 'wie' in text and 'alt' in text and 'du' in text:
        ts = datetime.datetime.now()
        heute = ts.strftime('%d %b %Y')
        diff = datetime.datetime.strptime(heute, '%d %b %Y') - datetime.datetime.strptime('22 Jul 2018', '%d %b %Y')
        daynr = diff.days
        tiane.say('{} Tage seit den ersten Tests.'.format(daynr))
    elif ' aha' in text or 'aha?' in text:
        tiane.say('Frag mal was vernünftiges ;)')
    elif 'bist' in text and 'dumm' in text:
        tiane.say('Nein, du stellst nur die falschen Fragen.')
    elif 'bist' in text and 'toll' in text or 'bist' in text and 'genial' in text:
        tiane.say(random.choice(['Vielen Dank, {}'.format(tiane.user), 'Dankeschön, {}'.format(tiane.user), 'Es freut mich, dass ich hilfreich bin!'.format(tiane.user)]))
    elif 'liebe' in text and 'dich' in text:
        tiane.say(random.choice(['Eine wirklich schlechte Entscheidung... aber Danke!', 'Ich fühle mich geehrt, {}'.format(tiane.user), 'Ich fürchte, als Sprachassistent bin ich eine schlechte Wahl für deinen Lebensgefährten...']))
    elif 'sag ' in text and 'was' in text or 'sage ' in text and 'was' in text or 'erzähl' in text and 'was' in text:
        if 'nettes' in text or 'liebes' in text or 'freundliches' in text:
            tiane.say(random.choice(['Ich freue mich, dass du mit mir sprichst, {}'.format(tiane.user), 'Ich freue mich, dass du dich mit mir unterhältst!', 'Ich spreche sehr gerne mit dir! Du bist ein toller Mensch.', 'Ich unterhalte mich sehr gerne mit dir, {}. Du bist ein toller Mensch!'.format(tiane.user), 'Das fällt mir leicht, du bist wirklich sehr nett zu mir.', 'Hast du denn sonst niemanden, der nett zu dir ist?', 'Wenn du dich schlecht fühlst, denk einfach daran, dass du ein besserer Mensch bist als Künstliche Intelligenzen es jemals sein werden!', 'Du bist ein super Gesprächspartner, {}'.format(tiane.user)]))
    elif 'hast' in text and 'recht' in text:
        tiane.say('Ich weiß.')
    elif ('sicher' in text or 'verschlüsselt' in text) and ('chat' in text or 'kanal' in text or 'verbindung' in text):
        tiane.say('Meine internen Verbindungen sind sicher verschlüsselt, bei Telegram weiß ich das nicht so genau. Aber generell, bevor du mir irgendwelche Geheimnisse anvertraust: Denk daran, dass der Besitzer des Computers, auf dem ich laufe, immer alles sieht...')
