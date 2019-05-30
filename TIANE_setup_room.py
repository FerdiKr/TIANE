#!/usr/bin/env python3
from distutils.dir_util import copy_tree
import shutil
import time
import json
import sys
import os
from TIANE_setup-TIANE_setup_wrapper import *

def configure_camera(cam_config_data, picam_already_used):
    if not picam_already_used:
        if not cam_config_data == {}:
            default = cam_config_data['PiCam']
        else:
            default = False
        antwort = ja_nein_frage('\nIst diese Kamera eine PiCam (angeschlossen per Flachbandkabel am entsprechenden Port eines Raspberry Pi) [Ja / Nein]? [Standard ist "{}"]: '.format(tf2jn(default)), default)
        if antwort == True:
            print('Okay, für diese Kamera wird eine PiCam erwartet.')
            cam_config_data = {'PiCam':True}
            return cam_config_data, True
        else:
            print('Okay, für diese Kamera wird eine USB-Webcam erwartet.')
            cam_config_data['PiCam'] = False
            time.sleep(1)

    try:
        default = cam_config_data['width']
    except KeyError:
        default = 0
    antwort = frage_nach_zahl('\nSoll die horizontale Auflösung dieser Kamera angepasst werden? Wenn ja, gib die gewünschte Bildbreite (in Pixeln) ein.\n'
                              'Achtung: Nicht alle Webcams unterstützen alle Auflösungen, du wirst hier wahrscheinlich experimentieren müssen.\n'
                              '"0" bedeutet "keine Anpassung". [Standard ist "{}"]:  '.format(default), default)
    if antwort == 0:
        print('Okay, die horizontale Auflösung dieser Kamera wird nicht angepasst.\n')
        try:
            del cam_config_data['width']
        except:
            pass
    else:
        print('Okay, für diese Kamera wird eine horizontale Auflösung von {} Pixeln verwendet.\n'.format(antwort))
        cam_config_data['width'] = antwort
    time.sleep(1)

    try:
        default = cam_config_data['height']
    except KeyError:
        default = 0
    antwort = frage_nach_zahl('Soll die vertikale Auflösung dieser Kamera angepasst werden? Wenn ja, gib die gewünschte Bildhöhe (in Pixeln) ein.\n'
                              'Achtung: Nicht alle Webcams unterstützen alle Auflösungen, du wirst hier wahrscheinlich experimentieren müssen.\n'
                              '"0" bedeutet "keine Anpassung". [Standard ist "{}"]:  '.format(default), default)
    if antwort == 0:
        print('Okay, die vertikale Auflösung dieser Kamera wird nicht angepasst.\n')
        try:
            del cam_config_data['height']
        except:
            pass
    else:
        print('Okay, für diese Kamera wird eine vertikale Auflösung von {} Pixeln verwendet.\n'.format(antwort))
        cam_config_data['height'] = antwort
    time.sleep(1)

    return cam_config_data, picam_already_used

def end_config(config_data, system_name):
    if not os.path.exists(config_data['Room_name']):
        os.mkdir(config_data['Room_name'])
    try:
        copy_tree('room', config_data['Room_name'])
    except:
        print(color.RED + '[ERROR]' + color.END + ' Fehler beim kopieren der Dateien. Bitte versuche, den Setup-Assistent mit Root-Rechten auszuführen.')
        sys.exit()
    bedingt_kopieren('room/resources/optional_modules/cameras.py', config_data['Room_name'] + '/modules/continuous/cameras.py', room_config_data['use_cameras'])
    print('Die Konfiguration deines {}-Raumclients ist abgeschlossen. Sobald du diesen Assistenten beendest, '
          'kannst du den Ordner "{}" auf dein entsprechendes Raum-Gerät übertragen.\n'
          'Als nächstes kannst du einen weiteren Raum einrichten '
          'oder mit dem entsprechenden Assistenten Nutzer hinzufügen, sofern nicht bereits geschehen.'.format(system_name, config_data['Room_name']))
    text = input('[ENTER drücken zum beenden]')
    print('\nDie neuen Daten werden gespeichert...')
    with open(config_data['Room_name'] + '/TIANE_config.json', 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print('\n[{}] Auf wiedersehen!\n'.format(system_name.upper()))
    sys.exit()

########################### ANFANG ###########################
if not os.path.exists('room/TIANE_config.json'):
    print('\n' + color.RED + '[ERROR]' + color.END + ' Die nötigen Dateien (Ordner "room") für diesen Setup-Schritt konnten nicht gefunden werden.\n'
          'Hast du die Dateien heruntergeladen?\n'
          'Befindet sich das Setup-Skript im richtigen Ordner?')
    text = input('[ENTER drücken zum beenden]')
    sys.exit()

if not os.path.exists('server/TIANE_config.json'):
    print('\n' + color.RED + '[ERROR]' + color.END + ' Die nötigen Dateien (Ordner "server") für diesen Setup-Schritt konnten nicht gefunden werden.\n'
          'Hast du die Dateien heruntergeladen?\n'
          'Befindet sich das Setup-Skript im richtigen Ordner?')
    text = input('[ENTER drücken zum beenden]')
    sys.exit()

with open('server/TIANE_config.json', 'r') as config_file:
    server_config_data = json.load(config_file)
system_name = server_config_data['System_name']

print('Willkommen zum Setup-Assistenten für deinen neuen Sprachassistenten.\n'
      'In diesem Schritt Kannst du einen {}-Raumclient einrichten.\n'
      'Dieser Setup-Assistent wird dich mit Fragen durch die Einrichtung führen.\n'
      'Bitte gib deine Antworten ein und bestätige sie mit [ENTER].\n'
      'Wenn du bei einer Frage die vorgegebene Standard-Antwort übernehmen willst, reicht es, wenn du einfach [ENTER] drückst, ohne etwas einzugeben.'.format(system_name))
time.sleep(1)
text = input('[ENTER drücken zum fortfahren]')

if server_config_data['TNetwork_Key'] == '':
    print('\n' + color.RED + '[ERROR]' + color.END + ' Es konnte keine fertige Server-Konfiguration gefunden werden (TNetwork-Schlüssel fehlt).\n'
          'Du musst zuerst deinen {}-Server konfigurieren (mit "TIANE_server_setup.py"), bevor du Räume hinzufügen kannst.'.format(system_name))
    text = input('[ENTER drücken zum beenden]')
    sys.exit()

print('\n')
room_name = frage_erfordert_antwort('Bitte gib einen Namen für diesen {}-Raumclient ein (z.B. "Küche" oder "Wohnzimmer"): '.format(system_name))
print('Okay, dieser {}-Raum wird {} heißen.\n'.format(system_name, room_name))
time.sleep(1)

if os.path.exists(room_name + '/TIANE_config.json'):
    print('Es wurde eine bestehende Konfiguration für den Raum {} gefunden.'.format(room_name))
    antwort = ja_nein_frage('Soll diese Konfiguration als Standardantworten geladen werden [Ja / Nein]? [Standard ist "Ja"]: ', True)
    if antwort == True:
        print('Konfiguration wird geladen...\n')
        with open(room_name + '/TIANE_config.json', 'r') as config_file:
            room_config_data = json.load(config_file)
    else:
        with open('room/TIANE_config.json', 'r') as config_file:
            room_config_data = json.load(config_file)
else:
    with open('room/TIANE_config.json', 'r') as config_file:
        room_config_data = json.load(config_file)

room_config_data['Room_name'] = room_name
room_config_data['TNetwork_Key'] = server_config_data['TNetwork_Key']

print('Als nächstes musst du die lokale IP-Adresse deines {}-Servers eingeben, damit dieser Raum ihn später erreichen kann.\n'
      'Du kannst die Adresse zum Beispiel in den Netzwerkeinstellungen im Informations-Fenster zu deiner derzeitigen Verbindung unter "IPv4-Adresse" finden '
      'oder sie dir mit dem Konsolenbefehl "ifconfig -a" anzeigen lassen.\n'
      'Bitte stell sicher, dass du die Adresse im richtigen Format eingibst (z.B. 192.168.1.101)!'.format(system_name))
if not room_config_data['Server_IP'] == '':
    default_ip = room_config_data['Server_IP']
    server_ip = input('Bitte gib die lokale IP-Adresse deines {}-Servers ein [Standard ist {}]: '.format(system_name, default_ip))
    if server_ip == '' or server_ip == ' ':
        room_config_data['Server_IP'] = default_ip
        server_ip = default_ip
    else:
        room_config_data['Server_IP'] = server_ip
else:
    server_ip = frage_erfordert_antwort('Bitte gib die lokale IP-Adresse deines {}-Servers ein: '.format(system_name))
    room_config_data['Server_IP'] = server_ip
print('Okay, dieser Raumclient wird deinen Server unter {} suchen.\n'.format(server_ip))
time.sleep(1)

print('Die folgenden beiden Parameter betreffen die Erkennung des Schlüsselwortes und allgemein die Spracheingabe von {}.\n'
      'Da sich die optimalen Werte für diese Einstellungen leider von Fall zu Fall stark unterscheiden, sind die vorgeschlagenen Standardantworten nur sehr grobe Richtwerte.\n'
      'Wenn bei dir die Schlüsselworterkennung unzuverlässig oder im Gegenteil zu oft anspringt, solltest du diese Parameter auf jeden Fall noch einmal bearbeiten.\n'
      'Du kannst sie dann entweder durch erneuten Durchlauf dieses Setup-Assistenten oder direkt in der Datei "TIANE_config.json" im Ordner des entsprechenden Raumes ändern.'.format(system_name))
time.sleep(1)
text = input('[ENTER drücken zum fortfahren]')

default_hotword_sensitivity = room_config_data['Hotword_sensitivity']
print('\nDer erste Parameter, "Hotword_sensitivity", gibt an, wie stark dein Sprachassistent auf sein Schlüsselwort (z.B. "Hey TIANE") reagiert.\n'
      'Je höher der Wert, desto höher die Wahrscheinlichkeit, dass in einem Satz oder Geräusch das Schlüsselwort erkannt wird.\n'
      'Demnach solltest du den Wert erhöhen, wenn dein Sprachassistent dein Schlüsselwort zu selten versteht, und senken, wenn er zu oft '
      'fälschlicherweise Gesprächsfetzen oder Umgebungsgeräusche für sein Schlüsselwort hält.')
hotword_sensitivity = frage_nach_float_zahl('Bitte gib einen Wert für "Hotword_sensitivity" ein [Standard ist {}]: '.format(default_hotword_sensitivity), default_hotword_sensitivity)
room_config_data['Hotword_sensitivity'] = hotword_sensitivity
print('Okay, der Wert für "Hotword_sensitivity" beträgt jetzt {}.\n'.format(hotword_sensitivity))
time.sleep(1)

default_hotword_audio_gain = room_config_data['Hotword_Audio_gain']
print('Der zweite Parameter, "Hotword_Audio_gain", gibt an, wie stark dein Sprachassistent die vom Mikrofon aufgenommenen Audiosignale verstärkt.\n'
      'Diese Verstärkung gilt sowohl für die Schlüsselworterkennung als auch für die allgemeine Spracheingabe.\n'
      'Wenn dein Assistent dich schlechter versteht, wenn du dich weiter vom Mikrofon entfernst, kann es helfen, diesen Wert zu erhöhen.')
hotword_audio_gain = frage_nach_float_zahl('Bitte gib einen Wert für "Hotword_Audio_gain" ein [Standard ist {}]: '.format(default_hotword_audio_gain), default_hotword_audio_gain)
room_config_data['Hotword_Audio_gain'] = hotword_audio_gain
print('Okay, der Wert für "Hotword_Audio_gain" beträgt jetzt {}.\n'.format(hotword_audio_gain))
time.sleep(1)

print('Im letzten Schritt kannst du festlegen, welche der mitgelieferten optionalen Module dieser Raum verwenden soll.\n'
      'Du kannst die verwendeten Module jederzeit im Ordner "modules(/continuous)" im {}-Ordner des Raumclients einsehen und bearbeiten, '
      'optionale Module, die du bei dieser Einrichtung noch nicht auswählst, finden sich im Ordner "resources/optional_modules"'.format(system_name))
text = input('[ENTER drücken zum fortfahren]')

default = room_config_data['use_cameras']
use_cameras = ja_nein_frage('\nSollen an dieses {}-Raum-Gerät Kameras angeschlossen werden (Voraussetzung: OpenCV installiert) [Ja / Nein]? [Standard ist "{}"]: '.format(system_name, tf2jn(default)), default)
room_config_data['use_cameras'] = use_cameras
if use_cameras == True:
    print('Okay, dieser Raumclient wird mit dem Modul "cameras.py" Kamerabilder aufnehmen und an deinen {}-Server senden können.\n'
          'Dafür musst du allerdings zunächst im Folgenden die zu verwendenden Kameras konfigurieren:\n'.format(system_name))
    time.sleep(1)

    picam_already_used = False
    new_cam_config = {}
    cam_src = 0
    cam_index = 1
    antwort = ja_nein_frage('Möchtest du jetzt eine Kamera konfigurieren [Ja / Nein]? [Standard ist "Ja"]: ', True)
    if antwort == True:
        camname = frage_mit_default('\nBitte gib einen Namen für diese Kamera ein (z.B. "Türkamera" oder "Cam1") [Standard ist "Cam{}"]: '.format(cam_index), 'Cam{}'.format(str(cam_index)))
        print('Okay, diese Kamera wird "{}" heißen.'.format(camname))
        try:
            default_cam_config = room_config_data['Cameras'][camname]
        except KeyError:
            default_cam_config = {}
        cam_config_data, picam_already_used = configure_camera(default_cam_config, picam_already_used)
        if not cam_config_data['PiCam']:
            cam_config_data['src'] = cam_src
            cam_src += 1
        cam_index += 1
        new_cam_config[camname] = cam_config_data

        while True:
            antwort = ja_nein_frage('Möchtest du eine weitere Kamera hinzufügen [Ja / Nein]? [Standard ist "Nein"]: ', False)
            if antwort == True:
                camname = frage_mit_default('\nBitte gib einen Namen für diese Kamera ein (z.B. "Türkamera" oder "Cam1") [Standard ist "Cam{}"]: '.format(cam_index), 'Cam{}'.format(str(cam_index)))
                print('Okay, diese Kamera wird "{}" heißen.'.format(camname))
                try:
                    default_cam_config = room_config_data['Cameras'][camname]
                except KeyError:
                    default_cam_config = {}
                cam_config_data, picam_already_used = configure_camera(default_cam_config, picam_already_used)
                if not cam_config_data['PiCam']:
                    cam_config_data['src'] = cam_src
                    cam_src += 1
                cam_index += 1
                new_cam_config[camname] = cam_config_data
            else:
                print('Okay, es wird keine weitere Kamera hinzugefügt.\n')
                room_config_data['Cameras'] = new_cam_config
                break
    else:
        print('Achtung: Es wurden keine Kameras konfiguriert!')
else:
    print('Okay, dieser Raumclient wird keine Kamera-Funktionen verwenden.\n')

end_config(room_config_data, system_name)
