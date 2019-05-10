import json

def isValid(text):
    text = text.lower()
    if ('erstell' in text or 'mach' in text or 'sicher' in text) and ('backup' in text or 'speicher' in text or 'date' in text):
        return True

def check(thing):
    if type(thing) == type({'test':'test'}):
        thing = check_dict(thing)
    elif type(thing) == type(['test']):
        thing = check_list(thing)
    else:
        thing = str(thing)
    return thing

def check_list(liste):
    out = []
    for value in liste:
        try:
            x = json.dumps(value)
        except:
            value = check(value)
        out.append(value)
    return out

def check_dict(c_dict):
    o_dict = {}
    for key, value in c_dict.items():
        try:
            x = json.dumps(key)
        except:
            key = str(key)
        try:
            x = json.dumps(value)
        except:
            value = check(value)
        o_dict[key] = value
    return o_dict

def check_iter(iter):
    liste = []
    for value in iter:
        try:
            x = json.dumps(value)
        except:
            value = check(value)
        liste.append(value)
    liste = tuple(liste)
    return liste

def handle(text, tiane, profile):
    tiane.asynchronous_say('Okay, ich erstelle eine Kopie meiner temporären Daten.')
    backup_json = {}
    backup_json = check(profile)
    with open(tiane.path + '/TIANE_LOG.json','w') as json_file:
        json.dump(backup_json, json_file, indent=4, ensure_ascii=False)
    tiane.say('Die Daten wurden gespeichert.')
