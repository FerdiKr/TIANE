import subprocess

PRIORITY = -1
SECURE = False # Verstößt gegen Punk 1

# Nutzt das fortunes-de package verfügbar auf debian und ubuntu.
# Das paket stellt irgendwelche sätze oder zitate bereit.
# Das Modul wird nur aktiv, wenn `fortunes-de` installiert ist.

def isValid(text):
    if ('erzähl' in text.lower() or 'sag' in text.lower()) and ('irgendwas' in text.lower() or 'irgendetwas' in text.lower()):
        try:
            installedStr = subprocess.check_output("dpkg-query --show --showformat='${db:Status-Status}\n' 'fortunes-de'", shell=True).decode('utf-8').lower()
            if 'installed' in installedStr and 'not' not in installedStr:
                return True
        except subprocess.CalledProcessError:
            return False
    return False

def handle(text, tiane, profile):
    try:
        fortune = subprocess.check_output("fortune", shell=True).decode('utf-8').strip().lower()
        if (fortune != ''):
            tiane.say(fortune)
        elif 'irgendetwas' in text.lower():
            tiane.say('irgendetwas')
        else:
            tiane.say('irgendwas')
    except subprocess.CalledProcessError:
        if 'irgendetwas' in text.lower():
            tiane.say('irgendetwas')
        else:
            tiane.say('irgendwas')
