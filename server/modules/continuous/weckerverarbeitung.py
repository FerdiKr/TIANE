import datetime

INTERVALL = 2

def run(tiane, profile):
    now = datetime.datetime.now()
    if 'Wecker' in tiane.local_storage.keys():
        erinnerungen = tiane.local_storage.get('Wecker')
        for item in erinnerungen:
            benutzer = item['Benutzer']
            zeit = item['Zeit']
            zeit = datetime.datetime.strptime(zeit, '%Y-%m-%d %H:%M:%S.%f')
            ausgabe = 'Guten Morgen {}. Ich hoffe, du hast gut geschlafen'.format(benutzer)
            differenz = zeit - now
            dic = {'Benutzer': benutzer, 'Text': ausgabe}
            if differenz.total_seconds() <= 0:
                tiane.start_module(user=benutzer, name='weckerausgabe', text=dic)
                erinnerungen.remove(item)
                tiane.local_storage['Wecker'] = erinnerungen
