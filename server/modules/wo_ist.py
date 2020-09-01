
SECURE = True

PRIORITY = 1


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
        if user.lower() in text.lower():
            try:
                room = local_storage['users'][user]['room']
                tiane.say('{} ist gerade im {}.'.format(user, room))
            except KeyError:
                tiane.say('Ich konnte {} gerade nicht finden'.format(user))
            return
    # Es wurde nach keiner Person gefragt. Vielleicht nach einer Stadt, einem Land.
    # Starten wir lieber das wo_ist_welt Modul
    # Wir hängen noch ein '§DIRECTCALL_FROM_WO_IST§' an. Grund dafür ist issue #142
    tiane.start_module(user = tiane.user, name = "wo_ist_welt", text = '§DIRECTCALL_FROM_WO_IST§' + str(text))