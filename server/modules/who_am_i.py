import random

def handle(text, tiane, profile):
    if tiane.user is not None:
        if not tiane.user == 'Unknown':
            responses = ['Wenn mich nicht alles täuscht bist du {}',
                         'Ich glaube du bist {}',
                         'Weißt du etwa nicht mehr wer du bist, {}?',
                         'Soweit ich das sehen kann bist du {}']
            response = random.choice(responses)
            tiane.say(response.format(tiane.user))
            return
    responses = ['Das kann ich gerade leider nicht sehen',
                 'Das musst du aktuell leider selbst wissen',
                 'Entschuldige, aber das kann ich leider gerade nicht beurteilen']
    tiane.say(random.choice(responses))

def isValid(text):
    text = text.lower()
    if 'wer' in text and 'bin' in text and 'ich' in text:
        return True
    if 'wie' in text and 'heiße' in text and 'ich' in text:
        return True
