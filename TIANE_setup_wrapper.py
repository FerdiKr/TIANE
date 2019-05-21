#!/usr/bin/env python3

from Crypto import Random
import base64
import shutil
import os
import sys


class color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"

def generate_key(length):
    key = Random.get_random_bytes(length)
    key_encoded = base64.b64encode(key)
    key_string = key_encoded.decode('utf-8')
    return key_string

def ja_nein_frage(fragentext, default):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            return default
        elif 'j' in eingabe.lower() or 'y' in eingabe.lower():
            return True
        elif 'n' in eingabe.lower():
            return False
        else:
            print(color.YELLOW + 'Das habe ich leider nicht verstanden.' + color.END)

def frage_erfordert_antwort(fragentext):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            print(color.YELLOW + 'Bitte gib etwas ein.' + color.END)
        else:
            return eingabe

def frage_mit_default(fragentext, default):
    eingabe = input(fragentext)
    if eingabe == '' or eingabe == ' ':
        return default
    else:
        return eingabe

def frage_nach_zahl(fragentext, default, allowed_answers=None):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            return default
        try:
            eingabe = int(eingabe)
        except TypeError:
            print(color.YELLOW + 'Bitte gib eine Zahl ein.' + color.END)
            continue
        if not allowed_answers == None:
            if not eingabe in allowed_answers:
                print('Bitte gib eine dieser Zahlen ein: {}'.format(allowed_answers))
                continue
        return eingabe

def frage_nach_float_zahl(fragentext, default, allowed_answers=None):
    while True:
        eingabe = input(fragentext)
        if eingabe == '' or eingabe == ' ':
            return default
        try:
            eingabe = float(eingabe)
        except:
            print('Bitte gib eine Zahl ein.')
            continue
        if not allowed_answers == None:
            if not eingabe in allowed_answers:
                print('Bitte gib eine dieser Zahlen ein: {}'.format(allowed_answers))
                continue
        return eingabe

def bedingt_kopieren(ursprung, ziel, copy):
    if copy:
        if os.path.exists(ziel):
            return
        else:
            shutil.copy(ursprung, ziel)
    else:
        if os.path.exists(ziel):
            os.remove(ziel)

def tf2jn(tf):
    return "Ja" if tf else "Nein"

def enterContinue():
    t = input(color.BLUE + '[ENTER drücken zum fortfahren]' + color.END)

def enterFinalize():
    t = input(color.BLUE + '[ENTER drücken zum beenden]' + color.END)
