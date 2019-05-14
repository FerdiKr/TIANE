import random

def handle(text, tiane, profile):
    user = tiane.user
    farewells = ['Auf wiedersehen, {}!',
                 'Bis bald {}',
                 'Machs gut {}',
                 'Viel Spaß!']
    farewell = random.choice(farewells)
    if '{}' in farewell:
        farewell = farewell.format(user)
    tiane.say(farewell)

    # Erst den User aus allen Räumen entfernen...
    for raum in profile['rooms'].values():
        try:
            if user in raum['users']:
                raum['users'].remove(user)
        except KeyError:
            raum['users'] = []
            continue
    for raum in tiane.rooms.values():
        if user in raum.users:
            raum.users.remove(user)
    # ...Und den Raum aus dem User!
    try:
        if not profile['users'][user]['telegram_id'] == 0:
            profile['users'][user]['room'] = 'Telegram'
        else:
            profile['users'][user]['room'] = ''
    except:
        pass


def isValid(text):
    text = text.lower()
    if 'tschüss' in text or ('auf' in text and 'wiedersehen' in text) or ('ich' in text and 'bin' in text and 'weg' in text) or ('mach' in text and 'gut' in text):
        return True
    else:
        return False
