def isValid(text):
    return text.lower().startswith('wiederhole')

def handle(text, tiane, profile):
    tiane.say(str(' '.join(text.split(' ')[1:])), output='telegram_speech')
