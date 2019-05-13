def isValid(text):
    text = text.lower()
    if 'wie' in text and 'heißt' in text and 'du' in text:
        return True
    if ('wer' in text or 'was' in text) and 'bist' in text and 'du' in text:
        return True
    elif ('woher' in text or 'bedeutet' in text or 'heißt' in text) and ' name' in text and ('dein' in text or 'der' in text or 'tiane' in text):
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

def handle(text, tiane, profile):
    text = text.lower()
    if 'wie' in text and 'heißt' in text and 'du' in text:
        tiane.say('Ich heiße TIANE.')
    elif ('wer' in text or 'was' in text) and 'bist' in text and 'du' in text:
        tiane.say('Ich bin TIANE, ein Open-Source-Sprachassistent!')
    elif ('woher' in text or 'bedeutet' in text or 'heißt' in text) and ' name' in text and ('dein' in text or 'der' in text or 'tiane' in text):
        tiane.say('Anders als man denken könnte, ist mein Name tatsächlich keine Abkürzung für irgendwas. '
                  'Aber er ist angelehnt an einen sprechenden Computer namens "DIANE" aus einem von Ferdis Lieblingsbüchern.')
    elif (('was' in text and 'für' in text) or ('wie' in text and 'heißt' in text) or 'welches' in text) and 'buch' in text:
        tiane.say('"Limit" von Frank Schätzing.')
    elif ('was' in text and 'kannst' in text and 'du' in text) or 'verstehst du' in text or ('was' in text and 'funktionen' in text) or ('was' in text and 'fragen' in text):
        tiane.say('Sagen wir mal so, den Turing-Test bestehe ich leider noch nicht... '
                  'Aber ich kann dir zum Beispiel das Wetter ansagen, ein paar allgemeine Wissensfragen beantworten '
                  'rechnen, würfeln und so weiter. '
                  'Und für alles weitere bist du gerne eingeladen, selbst in meinem GitHub-Repository aktiv zu werden!')
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
