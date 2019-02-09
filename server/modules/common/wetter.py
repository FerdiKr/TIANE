from urllib.request import urlopen, Request
import time
import urllib.parse
import ast
import re



def get_weather(place):
    place = place.lower()
    w = ''
    if 'overcast' in place:
        w = w + 'bedeckt'
    elif 'cloud' in place or 'cloudy' in place or 'clouds' in place:
        if 'scattered' or 'broken' or 'few' in place:
            w = w + 'teils wolkig'
        else:
            w = w + 'wolkig'
    elif 'drizzle' in place:
        w = w + 'leichten Nieselregen'
    elif 'clear' in place:
        w = w + 'klar'
    elif 'rain' or 'rainy' in place:
        if 'light' in place:
            w = w + 'leichter Regen'
        elif 'heavy' in place:
            w = w + 'starker Regen'
        else:
            w = w + 'regnerisch'
    elif 'mist' or 'misty' in place:
        w = w + 'neblig'
    elif 'haze' in place:
        w = w + 'leichter Dunst'
    elif 'hail' in place:
        w = w + 'Heil Hydra'
    elif 'smoke' in place:
        w = w + 'Waldbrand'
    elif 'storm' or 'stormy' in place:
        w = w + 'stuermisch'
    elif 'thunderstorm' in place:
        w = w + 'Gewitter'
    elif 'snow' or 'snowy' or 'snowfall' in place:
        if 'heavy' in place:
            w = w + 'starker Schneefall'
        elif 'light' in place:
            w = w + 'leichter Schneefall'
        else:
            w = w + 'Schneefall'
    else:
        w = w + place
    return w



def get_temperature(pl):
    t = pl - 273.15
    t = str(t)[:2]
    return t


def handle(text, tiane, profile):
    o = tiane.analysis['town']
    if o == 'None':
        tiane.say('Für welchen Ort möchtest du das Wetter erfahren?')
        antwort = tiane.listen()
        if antwort == 'TIMEOUT_OR_INVALID':
            tiane.say('Ich konnte den Ort leider nicht verstehen')
        else:
            antwort = antwort.lower()
            if len(antwort.split()) == 1:
                o = antwort 
            elif 'hier' in antwort or 'zu hause' in antwort:
                o = 'weitersburg'
            else:
                sonst = 'der dem den einer'
                satz = {}
                mind = 0
                falsches_in = 0
                i = str.split(antwort)
                ind = 1 
                for w in i:
                    satz[ind] = w 
                    ind += 1 
                for iindex, word in satz.items():
                    if word in sonst:
                        mind = mind + iindex
                for iindex, word in satz.items():
                    if iindex == mind - 1:
                        falsches_in = falsches_in + iindex
                if falsches_in >= 1:
                    del satz[falsches_in]
                for iindex, word in satz.items(): #findet Wort 'in''s key 
                    if word == 'in':
                        in_index = iindex
                        myind = in_index + 1
                        o = satz.get(myind)
                    elif word == 'für':
                        für_index = iindex
                        myind = für_index + 1
                        o = satz.get(myind)
    else:
        o = o
    ort = o.lower()
    web = 'http://api.openweathermap.org/data/2.5/weather?q=' + ort + '&appid=bd4d17c6eedcff6efc70b9cefda99082'
    request = Request(web)
    try:
        response = urlopen(request)
    except:
        tiane.say('Ich konnte das Wetter für den Ort {} leider nicht aufrufen.'.format(o))
        return
    html = response.read()
    html = str(html)
    ohneb = html[2:len(html)-1]
    dictionary = ast.literal_eval(ohneb)
    
    line = dictionary.get("weather")
    des = line[0].get("description")
    line2 = dictionary.get("main")
    des2 = line2.get("temp")
    weatherdescription = get_weather(des)
    temperature = get_temperature(int(des2))
    if temperature[1] == '.':
        temperature = temperature[0]
    if weatherdescription == 'bedeckt' or weatherdescription == 'teils wolkig' or weatherdescription == 'wolkig' or weatherdescription == 'klar' or weatherdescription == 'regnerisch' or weatherdescription == 'neblig' or weatherdescription == 'einen Waldbrand geben' or weatherdescription == 'stürmisch':
        wetter = 'Es ist ' + weatherdescription + ' bei ' + temperature + ' Grad Celsius.'
    else:
        wetter = 'Es gibt ' + weatherdescription + ' bei ' + temperature + ' Grad Celsius.'
    tiane.say(wetter)

    response.close()

def isValid(text):
    text = text.lower()
    if 'ist ' in text or 'haben ' in text:
        if 'wetter' in text or 'temperatur' in text or ' warm' in text or ' kalt' in text:
            return True

class Tiane:
    def __init__(self):
        self.local_storage = {}
        self.user = 'Baum'
        self.analysis = {'room': 'None', 'time': {'month': '10', 'hour': '10', 'year': '2018', 'minute': '00', 'day': '09'}, 'town': 'Stockholm'}

    def say(self, text):
        print (text)
    def listen(self):
        neuertext = input()
        return neuertext

def main():
    profile = {}
    tiane = Tiane()
    handle('Wie ist das Wetter', tiane, profile)
    
    
if __name__ == "__main__":
    main()
    
