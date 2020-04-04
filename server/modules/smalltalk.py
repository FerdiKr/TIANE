import datetime
import random

has_dateutil = True # Wenn `python_dateutil` installiert ist gibt TIANE eine Altersangabe in jahren, monaten und tagen an.
try:
    from dateutil import relativedelta
except ImportError:
    has_dateutil = False

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
    if '😂' in text or 'haha' in text:
        return True
    if 'wie' in text and 'alt' in text and 'du' in text:
        return True
    if ' aha' in text or 'aha?' in text:
        return True
    if 'bist' in text:
        if 'dumm' in text or 'doof' in text or 'schlecht' in text or 'behindert' in text:
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
    if ('wieso' in text or 'warum' in text) and 'stroh' in text and 'liegt' in text:
        return True
    if ('was' in text or 'welchen preis' in text or 'welchen platz' in text) and ('ihr' in text or 'wir' in text or 'du' in text) and ('gewonnen' in text or 'gemacht' in text):
        return True

def handle(text, tiane, profile):
    text = text.lower()
    if 'wie' in text and 'heißt' in text and 'du' in text:
        sys_name = tiane.system_name
        if sys_name.lower() == 'tiane':
            tiane.say('Ich heiße TIANE.')
        else:
            tiane.say('Ich heiße ' + sys_name + ', aber eigentlich bin ich TIANE.')
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
        if tiane.telegram_call:
            tiane.say('Hier der Link: https://github.com/FerdiKr/TIANE')
    elif '😂' in text or 'haha' in text:
        tiane.say('Warum lachst du? 😂')
        response = tiane.listen()
        tiane.say('Aha...')
    elif 'wie' in text and 'alt' in text and 'du' in text:
        ts = datetime.datetime.now()
        if not has_dateutil:
            heute = ts.strftime('%d %b %Y')
            diff = datetime.datetime.strptime(heute, '%d %b %Y') - datetime.datetime.strptime('22 Jul 2018', '%d %b %Y')
            daynr = diff.days
            tiane.say('{} Tage seit den ersten Tests.'.format(daynr))
        else:
            geburtsdatum = datetime.datetime.strptime('22 Jul 2018', '%d %b %Y')
            heute = datetime.datetime.strptime(ts.strftime('%d %b %Y'), '%d %b %Y')
            diff = relativedelta.relativedelta(heute, geburtsdatum)
            output_year = ''
            if diff.years == 1:
                output_year = 'Ein Jahr'
            elif diff.years > 0:
                output_year = '{} Jahre'.format(diff.years)

            output_month = ''
            if diff.months == 1:
                output_month = 'Einen Monat'
            elif diff.months > 0:
                output_month = '{} Monate'.format(diff.months)

            output_days = ''
            if diff.days == 1:
                output_days = 'Einen Tag'
            elif diff.days > 0:
                output_days = '{} Tage'.format(diff.days)

            output = ''
            if output_year != '':
                output = output + output_year

            if output_month != '':
                if output != '':
                    if (output_days == ''):
                        output = output + ' und '
                    else:
                        output = output + ', '
                output = output + output_month

            if output_days != '':
                if output != '':
                    output = output + ' und '
                output = output + output_days

            if (output == ''):
                tiane.say('Hast du deine Systemzeit verstellt? Heute sind ncht die ersten Tests.')
            else:
                tiane.say('{} seit den ersten Tests.'.format(output))

    elif ' aha' in text or 'aha?' in text:
        tiane.say('Frag mal was vernünftiges ;)')
    elif 'bist' in text:
        if 'dumm' in text or 'doof' in text or 'schlecht' in text or 'behindert' in text:
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
    elif ('wieso' in text or 'warum' in text) and 'stroh' in text and 'liegt' in text:
        tiane.say('Und warum hast du eine Maske auf?')
    elif ('was' in text or 'welchen preis' in text or 'welchen platz' in text) and ('ihr' in text or 'wir' in text or 'du' in text) and ('gewonnen' in text or 'gemacht' in text):
        tiane.say('Wir haben im Bundeswettbewerb Jugend forscht 2019 den 2. Preis in der Kategorie Mathematik/Informatik gewonnen.')
