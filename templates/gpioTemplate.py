import RPi.GPIO as GPIO

# Beschreibung
'''
Template für die Steuerung von Geräten über die GPIO-Pins des Raspberry Pis.
Die Geräte werden in einer Liste verwaltet, die zugehörige Pinnummer in einer weiteren Liste.
Wird ein Gerät genannt, wird die entsprechende Pinnummer gesucht und an- bzw. ausgeschaltet.
'''

# Geraete
devicesNames = ['','']
devicesPins = [0,0]

def isValid(text):
    text = text.lower()
    if 'an' in text or 'ein' in text or 'aus' in text:
        for device in devicesNames:
            if device in text:
                return True
    return False


def handle(text, tiane, profile):
    text = text.lower()
    GPIO.setmode(GPIO.BCM)

    for i in range(len(devicesNames)):
        if devicesNames[i] in text:
            device = devicesNames[i]
            pin = devicesPins[i]
            GPIO.setup(pin, GPIO.OUT)
            break

    if 'an' in text or 'ein' in text:
        GPIO.output(pin, True)
        tiane.say(device + 'wird eingeschaltet')
    elif 'aus' in text:
        GPIO.output(pin, False)
        tiane.say(device + 'wird ausgeschaltet')
