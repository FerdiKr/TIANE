import datetime

INTERVALL = 2

def run(tiane, profile):
    now = datetime.datetime.now()
    if 'Erinnerungen' in tiane.local_storage.keys():
        erinnerungen = tiane.local_storage.get('Erinnerungen')
        for item in erinnerungen:
            benutzer = item['Benutzer']
            output = item['Text']
            zeit = item['Zeit']
            zeit = datetime.datetime.strptime(zeit, '%Y-%m-%d %H:%M:%S.%f')
            ausgabe = 'Ich sollte dich ans ' + output + ' erinnern'
            differenz = zeit - now
            dic = {'Text': ausgabe, 'Benutzer': benutzer}
            if differenz.total_seconds() <= 0:
                tiane.start_module(name='erinnerungsausgabe', text=dic)
                erinnerungen.remove(item)
                tiane.local_storage['Erinnerungen'] = erinnerungen
