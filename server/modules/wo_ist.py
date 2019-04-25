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
    if 'wo ' in text and 'ist' in text:
        return True

def handle(text, tiane, local_storage):
    for user in tiane.userlist:
        if user in text:
            try:
                room = local_storage['users'][user]['room']
                tiane.say('{} ist gerade im {}.'.format(user, room))
            except KeyError:
                tiane.say('Ich konnte {} gerade nicht finden'.format(user))
            return
