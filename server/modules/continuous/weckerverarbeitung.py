import datetime

INTERVALL = 2

def run(tiane, profile):
    now = datetime.datetime.now()
    if 'Wecker' in tiane.local_storage.keys():
        erinnerungen = tiane.local_storage.get('Wecker')
        for item in erinnerungen:
            benutzer = item['Benutzer']
            zeit = item['Zeit']
            '''zeit = datetime.datetime.strptime(zeit, '%Y-%m-%d %H:%M:%S.%f')'''
            differenz = zeit - now
            if differenz.total_seconds() <= 0:

                ausgabe = 'Guten Morgen {}. Ich hoffe, du hast gut geschlafen'.format(benutzer)
                try:
                    geburtsdatum = tiane.local_storage['users'][tiane.user]['date_of_birth']
                    month = int(geburtsdatum['month'])
                    day = int(geburtsdatum['day'])
                    now = datetime.datetime.now()
                    if now.month == month and now.day == day:
                        ausgabe = 'Herzlichen Glückwunsch zum Geburtstag {}. Ich hoffe, du hast einen großartigen Tag.'.format(
                            benutzer)
                except KeyError:
                    '''Do nothing'''

                dic = {'Benutzer': benutzer, 'Text': ausgabe}

                tiane.start_module(user=benutzer, name='weckerausgabe', text=dic)
                erinnerungen.remove(item)
                tiane.local_storage['Wecker'] = erinnerungen
