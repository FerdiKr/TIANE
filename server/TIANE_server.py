from TNetwork import TNetwork_Connection_Server
import TWebsocket
from analyze import Sentence_Analyzer
from threading import Thread
import traceback
import random
import pkgutil
import socket
import base64
import time
import json
import os
import sys
from pathlib import Path
import pickle
from urllib.request import urlopen, Request
import urllib.parse
import pyjiane as jiane

def runMain(commandMap=None, feedbackMap=None):
    class Modules:
        def __init__(self):
            self.Modulewrapper = Modulewrapper
            self.Modulewrapper_continuous = Modulewrapper_continuous

            self.continuous_stopped = False
            self.continuous_threads_running = 0

            self.modules_defined_vocabulary = []

            self.load_modules()

        def load_modules(self):
            self.modules_defined_vocabulary = []
            Log.write('', '----- COMMON_MODULES -----', show=True)

            self.common_modules = self.get_modules('modules') + jiane.loadModules('modules')
            self.common_modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)

            if self.common_modules == []:
                Log.write('INFO', '-- (Keine vorhanden)', show=True)
            Log.write('', '------ CONTINUOUS', show=True)

            self.common_continuous_modules = self.get_modules('modules/continuous',continuous=True) + jiane.loadModulesContinuous('modules')
            self.common_continuous_modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)

            if self.common_continuous_modules == []:
                Log.write('INFO', '-- (Keine vorhanden)', show=True)

            Log.write('', '------ USER_MODULES ------', show=True)
            self.no_user_modules = True
            self.user_modules = self.get_user_modules()
            if self.no_user_modules == True:
                Log.write('INFO', '-- (Keine vorhanden)', show=True)
            Log.write('', '------ CONTINUOUS', show=True)
            self.no_user_continuous_modules = True
            self.user_continuous_modules = self.get_user_modules(continuous=True)
            if self.no_user_continuous_modules == True:
                Log.write('INFO', '-- (Keine vorhanden)', show=True)
            Local_storage['TIANE_Modules_defined_Vocabulary'] = self.modules_defined_vocabulary

        def get_modules(self, directory, continuous=False):
            dirname = os.path.dirname(os.path.abspath(__file__))
            locations = [os.path.join(dirname, directory)]
            modules = []
            if "modules" not in Local_storage:
                Local_storage["modules"] = {}
            for finder, name, ispkg in pkgutil.walk_packages(locations):
                try:
                    loader = finder.find_module(name)
                    mod = loader.load_module(name)
                except:
                    traceback.print_exc()
                    Log.write('WARNING', 'Modul {} ist fehlerhaft und wurde übersprungen!'.format(name), show=True)
                    Local_storage["modules"][name] = {"name": name, "status": "error", "type": "unknown"}
                    continue
                else:
                    if continuous == True:
                        Log.write('INFO', 'Fortlaufendes Modul {} geladen'.format(name), show=True)
                        mode = "continuous"
                        modules.append(mod)
                    else:
                        Log.write('INFO', 'Modul {} geladen'.format(name), show=True)
                        mode = "normal"
                        modules.append(mod)
                    Local_storage["modules"][name] = {"name": name, "status": "loaded", "type": mode}
                    words = mod.WORDS if hasattr(mod, 'WORDS') else []
                    for word in words:
                        if not word in self.modules_defined_vocabulary:
                            self.modules_defined_vocabulary.append(word)
            modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                         else 0, reverse=True)
            return modules

        def get_user_modules(self, continuous=False):
            usermodules = {}
            for username, userdata in Local_storage['users'].copy().items():
                usermodules[username] = []
                locations = [os.path.join(userdata['path'], 'modules')]
                if continuous == True:
                    locations = [os.path.join(userdata['path'], 'modules/continuous')]
                modules = []
                for finder, name, ispkg in pkgutil.walk_packages(locations):
                    try:
                        loader = finder.find_module(name)
                        mod = loader.load_module(name)
                    except:
                        traceback.print_exc()
                        Log.write('WARNING', 'Modul {} (Nutzer: {}) ist fehlerhaft und wurde übersprungen!'.format(name, username), show=True)
                        continue
                    else:
                        if continuous == True:
                            Log.write('INFO', 'Fortlaufendes Modul {} (Nutzer: {}) geladen'.format(name, username), show=True)
                            modules.append(mod)
                            self.no_user_continuous_modules = False
                        else:
                            Log.write('INFO', 'Modul {} (Nutzer: {}) geladen'.format(name, username), show=True)
                            modules.append(mod)
                            self.no_user_modules = False
                        words = mod.WORDS if hasattr(mod, 'WORDS') else []
                        for word in words:
                            if not word in self.modules_defined_vocabulary:
                                self.modules_defined_vocabulary.append(word)
                modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                             else 0, reverse=True)
                usermodules[username] = modules
            return usermodules

        def query_threaded(self, user, name, text, direct=False, origin_room=None, data=None, must_be_secure=False): #direct: True = Sprachaufruf
            if text == None or text == '':
                text = random.randint(0,1000000000)
                analysis = {}
            else:
                Log.write('ACTION', '--{}-- ({}): {}'.format(user.upper(), origin_room, text), conv_id=str(text), show=True)
                try:
                    analysis = Tiane.Analyzer.analyze(str(text))
                    Log.write('ACTION', 'Analyse: ' + str(analysis), conv_id=str(text), show=True)
                except:
                    traceback.print_exc()
                    Log.write('ERROR', 'Satzanalyse fehlgeschlagen!', conv_id=str(text), show=True)
                    analysis = {}

            if name is not None:
                # Modul wurde direkt aufgerufen
                for module in self.common_modules:
                    if module.__name__ == name and ((not must_be_secure) or (hasattr(module, 'SECURE') and getattr(module, 'SECURE'))):
                        Log.write('ACTION', '--Modul {} direkt aufgerufen (Parameter: {})--'.format(name, text), conv_id=str(text), show=True)
                        Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                        mt = Thread(target=self.run_threaded_module, args=(text,module,))
                        mt.daemon = True
                        mt.start()
                        if direct:
                            Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)

                        return True
                for module in self.user_modules[user]:
                    if module.__name__ == name and ((not must_be_secure) or (hasattr(module, 'SECURE') and getattr(module, 'SECURE'))):
                        Log.write('ACTION', '--Modul {} (Nutzer: {}) direkt aufgerufen (Parameter: {})--'.format(name, user, text), conv_id=str(text), show=True)
                        Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                        mt = Thread(target=self.run_threaded_module, args=(text,module,))
                        mt.daemon = True
                        mt.start()
                        if direct:
                            Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                        return True

            # Kein Direktaufruf? Ganz normal die Module durchgehen...
            # Bei Telegram-Aufrufen zuerst die entsprechenden telegram_isValids abklappern:
            if origin_room == 'Telegram':
                for module in self.common_modules:
                    try:
                        if module.telegram_isValid(data) and ((not must_be_secure) or (hasattr(module, 'SECURE') and getattr(module, 'SECURE'))):
                            Log.write('ACTION', '--Modul {} via telegram_isValid gestartet--'.format(module.__name__), conv_id=str(text), show=True)
                            Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                            mt = Thread(target=self.run_threaded_module, args=(text,module,))
                            mt.daemon = True
                            mt.start()
                            if direct:
                                Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                            return True
                    except:
                        continue
            # Ansonsten halt ohne spezielle Telegram-Features
            for module in self.common_modules:
                try:
                    if module.isValid(text) and ((not must_be_secure) or (hasattr(module, 'SECURE') and getattr(module, 'SECURE'))):
                        Log.write('ACTION', '--Modul {} gestartet--'.format(module.__name__), conv_id=str(text), show=True)
                        Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                        mt = Thread(target=self.run_threaded_module, args=(text,module,))
                        mt.daemon = True
                        mt.start()
                        if direct:
                            Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                        return True
                except:
                    traceback.print_exc()
                    Log.write('ERROR', 'Modul {} konnte nicht abgefragt werden!'.format(module.__name__), conv_id=str(text), show=True)

            if user is not None and user in Users.userlist:
                # ... Und wenn wir nen Nutzer haben, können wir auch noch in seinen Modulen suchen
                if not user == 'Unknown':
                    # Bei Telegram-Aufrufen zuerst die entsprechenden telegram_isValids abklappern:
                    if origin_room == 'Telegram':
                        for module in self.user_modules[user]:
                            try:
                                if module.telegram_isValid(data):
                                    Log.write('ACTION', '--Modul {} (Nutzer: {}) via telegram_isValid gestartet--'.format(module.__name__, user), conv_id=str(text), show=True)
                                    Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                                    mt = Thread(target=self.run_threaded_module, args=(text,module,))
                                    mt.daemon = True
                                    mt.start()
                                    if direct:
                                        Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                                    return True
                            except:
                                continue
                    for module in self.user_modules[user]:
                        try:
                            if module.isValid(text):
                                Log.write('ACTION', '--Modul {} (Nutzer: {}) gestartet--'.format(module.__name__, user), conv_id=str(text), show=True)
                                Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                                mt = Thread(target=self.run_threaded_module, args=(text,module,))
                                mt.daemon = True
                                mt.start()
                                if direct:
                                    Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                                return True
                        except:
                            traceback.print_exc()
                            Log.write('ERROR', 'Modul {} (Nutzer: {}) konnte nicht abgefragt werden!'.format(module.__name__, user), conv_id=str(text), show=True)

            # Hier ist die Lösung, die dafür sorgt, dass die Anfrage ggf. an einen bestimmten
            # Raum weitergeleitet wird... Das macht Sinn: So bleiben Direktaufrufe
            # über den Modulnamen auf jeden Fall unbehelligt und nur so können Sonderfälle wie "Erinner mich... wenn ich in der Küche bin"
            # korrekt interpretiert werden!
            if not analysis == {}:
                if analysis['room'] is not None:
                    return Tiane.route_query_modules(user, name, text, analysis['room'], direct=direct, origin_room=origin_room, data=data)

            return False

        def run_threaded_module(self, text, module):
            try:
                module.handle(text, Tiane.active_modules[str(text)], Tiane.local_storage)
                Log.write('ACTION', '--Modul {} beendet--'.format(module.__name__), conv_id=str(text), show=True)
            except:
                traceback.print_exc()
                Log.write('ERROR', 'Runtime-Error in Modul {}. Das Modul wurde beendet.\n'.format(module.__name__), show=True)
                Tiane.active_modules[str(text)].say('Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
            finally:
                try:
                    del Tiane.active_modules[str(text)]
                except KeyError:
                    pass
                Tiane.end_Conversation(text)
                return

        def start_continuous(self):
            # Startet den Thread, in dem die continuous_modules ausgeführt werden (siehe unten).
            Log.write('', '---- STARTE MODULE... ----', show=True)
            self.continuous_threads_running = 0
            no_modules = True
            if not self.common_continuous_modules == []:
                no_modules = False
                cct = Thread(target=self.run_continuous, args=(self.common_continuous_modules,None))
                cct.daemon = True
                cct.start()
                self.continuous_threads_running += 1

            for user, modules in self.user_continuous_modules.items():
                if not modules == []:
                    no_modules = False
                    uct = Thread(target=self.run_continuous, args=(modules,user))
                    uct.daemon = True
                    uct.start()
                    self.continuous_threads_running += 1
            if no_modules == True:
                Log.write('INFO', '-- (Keine vorhanden)', show=True)
            return

        def run_continuous(self,modules,user):
            # Führt die continuous_modules aus. Continuous_modules laufen immer im Hintergrund,
            # um auf andere Ereignisse als Sprachbefehle zu warten (z.B. Sensorwerte, Daten etc.).
            if user == None:
                # Wir müssen hier darauf achten, dass user_modules Namen haben dürfen, die bereits
                # von common_modules belegt sind, deshalb dürfen wir user- und common_modules nicht
                # einfach in derselben Liste speichern, sondern müssen zur eindeutigen Unterscheidung
                # Unterkeys für user einführen. Der key für common_modules ist 'common'.
                user = 'common'
            Tiane.continuous_modules[user] = {}
            for module in modules:
                intervalltime = module.INTERVALL if hasattr(module, 'INTERVALL') else 0
                Tiane.continuous_modules[user][module.__name__] = self.Modulewrapper_continuous(intervalltime,user)
                try:
                    module.start(Tiane.continuous_modules[user][module.__name__], Tiane.local_storage)
                    Log.write('INFO', 'Modul {} (Nutzer: {}) gestartet'.format(module.__name__, user), show=True)
                except:
                    #traceback.print_exc()
                    continue
            while True:
                for module in modules:
                    # Continuous_modules können ein Zeitintervall definieren, in dem sie gerne
                    # aufgerufen werden wollen, um Ressourcen zu sparen.
                    if time.time() - Tiane.continuous_modules[user][module.__name__].last_call >= Tiane.continuous_modules[user][module.__name__].intervall_time:
                        Tiane.continuous_modules[user][module.__name__].last_call = time.time()
                        try:
                            module.run(Tiane.continuous_modules[user][module.__name__], Tiane.local_storage)
                        except:
                            traceback.print_exc()
                            Log.write('ERROR', 'Runtime-Error in Continuous-Module {} (Nutzer "{}"). Das Modul wird nicht mehr ausgeführt.\n'.format(module.__name__, user), show=True)
                            del Tiane.continuous_modules[user][module.__name__]
                            modules.remove(module)
                if self.continuous_stopped:
                    break
                updateFeedback()  # injected update-local-storage-to-mmap-function
                time.sleep(0.01)
            self.continuous_threads_running -= 1
            return

        def stop_continuous(self):
            # Stoppt den Thread, in dem die continuous_modules ausgeführt werden, am Ende des Durchlaufs.
            # Gibt den Modulen aber danach noch eine Gelegenheit, aufzuräumen...
            if self.continuous_threads_running > 0:
                Log.write('', '------ Module werden beendet...', show=True)
                self.continuous_stopped = True
                # Warten, bis alle Threads zurückgekehrt sind
                while self.continuous_threads_running > 0:
                    time.sleep(0.01)
                self.continuous_stopped = False
                # Die stop() Funktion jedes Moduls aufrufen, sofern vorhanden
                no_stopped_modules = True
                for module in self.common_continuous_modules:
                    try:
                        module.stop(Tiane.continuous_modules['common'][module.__name__], Tiane.local_storage)
                        Log.write('INFO', 'Modul {} (Nutzer: {}) beendet'.format(module.__name__, 'common'), show=True)
                        no_stopped_modules = False
                    except:
                        continue
                for user, modules in self.user_continuous_modules.items():
                    for module in modules:
                        try:
                            module.stop(Tiane.continuous_modules[user][module.__name__], Tiane.local_storage)
                            Log.write('INFO', 'Modul {} (Nutzer: {}) beendet'.format(module.__name__, user), show=True)
                            no_stopped_modules = False
                        except:
                            continue
                # aufräumen
                Tiane.continuous_modules = {}
                if no_stopped_modules == True:
                    Log.write('INFO', '-- (Keine zu beenden)', show=True)
            return


    class Modulewrapper:
        # Diese Klasse ist wichtig: Module bekommen sie anstelle einer "echten" Tiane-Instanz
        # vorgesetzt. Denn es gibt nur eine Tiane-Instanz, um von dort aus alles regeln zu
        # können, aber Module brauchen verschiedene Instanzen, die Informationen über sie ent-
        # halten müssen, z.B. welcher Nutzer das Modul aufgerufen hat. Diese Informationen
        # ergänzt diese Klasse und schleift ansonsten einfach alle von Modulen aus aufrufbaren
        # Funktionen an die Hauptinstanz von Tiane durch.
        def __init__(self, text, analysis, user, origin_room, data):
            self.text = text # original_command
            self.analysis = analysis
            self.user = user
            self.room = origin_room

            self.telegram_data = data
            self.telegram_call = True if data is not None else False
            self.telegram = Tiane.telegram

            self.core = Tiane
            self.Analyzer = Tiane.Analyzer
            self.Users = Tiane.Users
            self.rooms = Tiane.rooms
            self.other_devices = Tiane.other_devices
            self.local_storage = Tiane.local_storage
            self.userlist = Users.userlist
            self.room_list = Tiane.room_list
            self.server_name = Tiane.server_name
            self.system_name = Tiane.system_name
            self.path = Tiane.path

        def say(self, text, room=None, user=None, output='auto'):
            if text == '' or not type(text) == type('test'):
                return
            if user == None or user == 'Unknown':
                user = self.user
            if user == None or user == 'Unknown': # Immer noch? Kann durchaus sein...
                room = self.room
            try:
                if self.local_storage['users'][user]['room'] == 'Telegram' and not 'telegram' in output.lower():
                    output = 'telegram'
            except KeyError:
                pass
            if output == 'auto':
                output = 'telegram' if self.room == 'Telegram' else 'speech'
            # Noch ne Variante: Der Nutzer ist nur über Telegram bekannt...
            if user not in self.userlist and user in self.local_storage['TIANE_telegram_name_to_id_table'].keys():
                if not 'telegram' in output.lower():
                    output = 'telegram'
            Tiane.route_say(self.text, text, room, user, output)
            
        def play(self, path=None, audiofile=None, room=None, user=None, priority=None, output='auto'):
            # gucken, ob ein Pfad angegeben wurde
            if path is not None:
                # Ja? Dann die Datei zum Pfad laden
                audiofile = wave.open(path, 'rb')
            if user == None or user == 'Unknown':
                user = self.user
            if user == None or user == 'Unknown':  # Immer noch? Kann durchaus sein...
                room = self.room
            try:
                if self.local_storage['users'][user]['room'] == 'Telegram' and not 'telegram' in output.lower():
                    output = 'telegram'
            except KeyError:
                print("KeyError")
            if output == 'auto':
                output = 'telegram' if self.room == 'Telegram' else 'speech'
            # Noch ne Variante: Der Nutzer ist nur über Telegram bekannt...
            if user not in self.userlist and user in self.local_storage['TIANE_telegram_name_to_id_table'].keys():
                if not 'telegram' in output.lower():
                    output = 'telegram'

            chunk = 4096
            frame_rate = audiofile.getframerate() * 2

            format = {'format': 8,
                      'channels': 1,
                      'rate': frame_rate,
                      'chunk': chunk}

            wav_data = audiofile.readframes(chunk)
            audio_buffer = []
            while wav_data:
                audio_buffer.append(wav_data)
                wav_data = audiofile.readframes(chunk)
            audio_buffer.append('Endederdurchsage')
            audio_data = {"buffer": audio_buffer, "format": format}
            Tiane.route_play(self.text, audio_data, room, user, output, priority)
            
        def listen(self, user=None, input='auto'):
            if user == None or user == 'Unknown':
                user = self.user
            if input == 'telegram' or (input == 'auto' and self.room == 'Telegram'):
                response = Tiane.route_listen(self.text, user, telegram=True)
                text = response['text']
            else:
                text = Tiane.route_listen(self.text, user)
            return text

        def asynchronous_say(self, text, room=None, user=None, output='auto'):
            if text == '' or not type(text) == type('test'):
                return
            if user == None or user == 'Unknown':
                user = self.user
            if user == None or user == 'Unknown': # Immer noch? Kann durchaus sein...
                room = self.room
            try:
                if self.local_storage['users'][user]['room'] == 'Telegram' and not 'telegram' in output.lower():
                    output = 'telegram'
            except KeyError:
                pass
            if output == 'auto':
                output = 'telegram' if self.room == 'Telegram' else 'speech'
            # Noch ne Variante: Der Nutzer ist nur über Telegram bekannt...
            if user not in self.userlist and user in self.local_storage['TIANE_telegram_name_to_id_table'].keys():
                if not 'telegram' in output.lower():
                    output = 'telegram'
            st = Thread(target=Tiane.route_say, args=(self.text, text, room, user, output))
            st.daemon = True
            st.start()

        def telegram_listen(self, user=None):
            if user == None or user == 'Unknown':
                user = self.user
            response = Tiane.route_listen(self.text, user, telegram=True)
            return response

        def end_Conversation(self):
            Tiane.end_Conversation(self.text)

        def start_module(self, user=None, name=None, text=None, room=None):
            if user == None or user == 'Unknown':
                user = self.user
            response = Tiane.start_module(user, name, text, room)

        def start_module_and_confirm(self, user=None, name=None, text=None, room=None):
            if user == None or user == 'Unknown':
                user = self.user
            return Tiane.start_module(user, name, text, room)

        def sendWebSocketEvent(self, event: str, data: dict):
            TWebsocket.sendEvent(event, data)

        def translate(self, ttext, targetLang='de'):
            return Tiane.translate(ttext, targetLang)


    class Modulewrapper_continuous:
        # Dieselbe Klasse für continuous_modules. Die Besonderheit: Die say- und listen-Funktionen
        # fehlen (also genau das, wofür der Modulewrapper eigentlich da war xD), weil continuous_-
        # modules ja nicht selbst nach außen telefonieren sollen. Dafür gibt es hier einen
        # Parameter für die Zeit zwischen zwei Aufrufen des Moduls.
        # Zusätzliche Besonderheit hier: Auch der continuous-Wrapper hat hier einen Parameter user,
        # der für user_continuous_modules auf den entsprechenden user gesetzt wird, um dessen user_modules
        # einfacher starten zu können.
        def __init__(self, intervalltime, user=None):
            self.intervall_time = intervalltime
            self.last_call = 0
            self.counter = 0
            self.user = user

            self.telegram = Tiane.telegram

            self.core = Tiane
            self.Analyzer = Tiane.Analyzer
            self.Users = Tiane.Users
            self.rooms = Tiane.rooms
            self.other_devices = Tiane.other_devices
            self.local_storage = Tiane.local_storage
            self.userlist = Users.userlist
            self.room_list = Tiane.room_list
            self.server_name = Tiane.server_name
            self.system_name = Tiane.system_name
            self.path = Tiane.path

        def start_module(self, user=None, name=None, text=None, room=None):
            if user == None or user == 'Unknown':
                user = self.user
            response = Tiane.start_module(user, name, text, room)

        def start_module_and_confirm(self, user=None, name=None, text=None, room=None):
            if user == None or user == 'Unknown':
                user = self.user
            return Tiane.start_module(user, name, text, room)

        def sendWebSocketEvent(self, event: str, data: dict):
            TWebsocket.sendEvent(event, data)

    class Users:
        def __init__(self):
            self.userlist = []
            self.userdict = {}

            self.load_users()

        def load_users(self):
            # Nutzer seperat aus dem users-Ordner laden
            Log.write('', '---------- USERS ---------', show=True)
            userdict = {}
            userlist = []
            telegram_id_table = {}
            telegram_name_to_id_table = {}
            telegram_id_to_name_table = {}

            location = os.path.join(absPath, 'users')
            subdirs = os.listdir(location)
            try:
                subdirs.remove("README.txt")
                subdirs.remove("README.md")
            except ValueError:
                pass
            # Wir gehen jetzt die einzelnen Unterordner von server/users durch, um die Nutzer
            # einzurichten. Die Unterordner tragen praktischerweise die Namen der Nutzer.
            for username in subdirs:
                userpath = os.path.join(location, username)
                with open(userpath + '/User_Info.json', 'r') as user_file:
                    user_data = json.load(user_file)
                user_data['User_Info']['path'] = userpath
                userdict[username] = user_data['User_Info']
                userlist.append(username)
                # Wenn der Nutzer Telegram eingerichtet hat, auch noch diese Formalitäten erledigen
                if not user_data['User_Info']['telegram_id'] == 0:
                    telegram_id_table[user_data['User_Info']['telegram_id']] = username
                    telegram_name_to_id_table[username] = user_data['User_Info']['telegram_id']
                    telegram_id_to_name_table[int(user_data['User_Info']['telegram_id'])] = username
                    userdict[username]['room'] = 'Telegram'
                Log.write('INFO', 'Nutzer {} geladen'.format(username), show=True)

            self.userlist = userlist
            self.userdict = userdict
            Local_storage['users'] = userdict
            Local_storage['TIANE_telegram_allowed_id_table'] = telegram_id_table
            Local_storage['TIANE_telegram_name_to_id_table'] = telegram_name_to_id_table
            Local_storage['TIANE_telegram_id_to_name_table'] = telegram_id_to_name_table

    class TIANE:
        def __init__(self):
            self.Modules = Modules
            self.Users = Users
            self.Log = Log
            self.Analyzer = Analyzer
            self.telegram = None

            self.active_modules = {}
            self.continuous_modules = {}
            self.rooms = Rooms
            self.other_devices = Other_devices
            self.devices_connecting = Devices_connecting
            self.telegram_queued_users = [] # Bei diesen Nutzern wird auf eine Antwort gewartet
            self.telegram_queue_output = {}

            self.local_storage = Local_storage
            self.userlist = Users.userlist
            self.room_list = Room_list
            self.server_name = Server_name
            self.system_name = System_name
            self.path = Local_storage['TIANE_PATH']
            self.open_mode = Open_mode
            self.presentation_mode = False

        def telegram_thread(self):
            # Verarbeitet eingehende Telegram-Nachrichten, weist ihnen Nutzer zu etc.
            while True:
                for msg in self.telegram.messages.copy():
                    #print(msg)

                    # Den TIANE-Nutzernamen aus der entsprechenden Tabelle laden
                    try:
                        user = self.local_storage['TIANE_telegram_allowed_id_table'][msg['from']['id']]
                    except KeyError:
                        # Nicht gefunden? Dürfen denn Nachrichten von Fremden angenommen werden?
                        if self.open_mode:
                            # Den Telegram-Nutzernamen als temporären Nutzernamen laden
                            try:
                                user = msg['from']['username']
                            except KeyError:
                                user = ''
                            if user == '':
                                # Gibt's auch nicht? Pech gehabt!
                                Log.write('WARNING', 'Telegram-Nutzer-ID {} kann nicht auf {} zugreifen. \n'
                                          'Unregistrierte Nutzer müssen einen Telegram-Benutzernamen eingerichtet haben!'.format(msg['from']['id'], self.system_name),
                                          conv_id=msg['text'], show=True)
                                self.telegram.say('Entschuldige bitte, ich kann leider nicht mit dir reden, weil du keinen Telegram-Benutzernamen eingerichtet hast.', msg['from']['id'], msg['text'])
                                self.telegram.messages.remove(msg)
                                continue
                            else:
                                self.local_storage['TIANE_telegram_name_to_id_table'][user] = msg['from']['id']
                                self.local_storage['TIANE_telegram_id_to_name_table'][int(msg['from']['id'])] = user
                        else:
                            # Wenn kein Zugriff erlaubt ist, legen wir die Nachricht trotzdem auf die Halde, vielleicht hat irgendein Modul Verwendung dafür...
                            self.local_storage['rejected_telegram_messages'].append(msg)
                            try:
                                Log.write('WARNING', 'Nachricht von unbekanntem Telegram-Nutzer {} ({}). Zugriff verweigert.'.format(msg['from']['username'], msg['from']['id']), conv_id=msg['text'], show=True)
                            except KeyError:
                                Log.write('WARNING', 'Nachricht von unbekanntem Telegram-Nutzer ({}). Zugriff verweigert.'.format(msg['from']['id']), conv_id=msg['text'], show=True)
                            self.telegram.say('Entschuldigung, aber ich darf leider zur Zeit nicht mit Fremden reden. Hat Papa gesagt :(', msg['from']['id'], msg['text'])
                            self.telegram.messages.remove(msg)
                            continue

                    response = True
                    # Wir erledigen hier noch einen Job, der eigentlich in assign_users gehören würde, hier aber einfacher einzubauen ist:
                    # Wer etwas per Telegram sendet, ist im Raum "Telegram" ;)
                    try:
                        if not self.presentation_mode:
                            self.local_storage['users'][user]['room'] = 'Telegram'
                    except KeyError:
                        pass
                    # Nachricht ist definitiv eine (ggf. eingeschobene) "neue Anfrage" ("Hey TIANE,...")
                    if msg['text'].lower().startswith(self.local_storage['activation_phrase'].lower()):
                        response = self.route_query_modules(user, text=msg['text'], direct=True, origin_room='Telegram', data=msg)
                    # Nachricht ist gar keine Anfrage, sondern eine Antwort (bzw. ein Modul erwartet eine solche)
                    elif user in self.telegram_queued_users:
                        self.telegram_queue_output[user] = msg
                    # Nachricht ist eine normale Anfrage
                    else:
                        response = self.route_query_modules(user, text=msg['text'], direct=True, origin_room='Telegram', data=msg)
                    if response == False:
                        self.telegram.say('Das habe ich leider nicht verstanden.', self.local_storage['TIANE_telegram_name_to_id_table'][user], msg['text'])
                    self.telegram.messages.remove(msg)
                time.sleep(0.5)

        def start_module(self, user, name, text, room):
            return self.route_query_modules(user, name=name, text=text, room=room)

        def route_say(self, original_command, text, raum, user, output):
            text = self.speechVariation(text) # Danke, Leon :)
            if self.presentation_mode and user in self.Users.userlist:
                output = 'speech'
            Log.write('DEBUG', {'Action':'route_say()', 'conv_id':original_command, 'text':text, 'raum':raum, 'user':user, 'output':output}, conv_id=original_command, show=False)
            if ('telegram' in output.lower()) or (user not in self.Users.userlist and user is not None):
                if self.telegram is not None:
                    # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, an wen der Text gesendet werden soll. Einfach beenden.
                    if user == None or user == 'Unknown':
                        Log.write('WARNING', 'Der Text "{}" konnte nicht gesendet werden, da kein Nutzer als Ziel angegeben wurde'.format(text), conv_id=original_command, show=True)
                        return
                    try:
                        self.telegram.say(text, self.local_storage['TIANE_telegram_name_to_id_table'][user], original_command, output=output)
                    except KeyError:
                        Log.write('WARNING', 'Der Text "{}" konnte nicht gesendet werden, da für den Nutzer "{}" keine Telegram-ID angegeben wurde'.format(text, user), conv_id=original_command, show=True)
                    return
                else:
                    Log.write('ERROR', 'Der Text "{}" sollte via Telegram gesendet werden, obwohl Telegram nicht eingerichtet ist!'.format(text), conv_id=original_command, show=True)
                    return
            # Vielleicht ist es ein WebSocket output type?
            if (TWebsocket.tellUserVia(user, output, text)):
                return
            if raum == None:
                # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, wo der Text gesagt werden soll. Einfach beenden.
                if user == None or user == 'Unknown':
                    Log.write('WARNING', 'Der Text "{}" konnte nicht gesagt werden, weil weder ein Raum noch ein Nutzer als Ziel angegeben wurden'.format(text), conv_id=original_command, show=True)
                    return
                #Vielleicht ist der user einem WebSocket-Raum zugeordnet?
                if TWebsocket.tellUser(user, text, self.local_storage):
                    return
                # Der Text soll zu einem bestimmten user gesagt werden
                current_waiting_room = ('',None)
                while True:
                    for name, room in self.rooms.items():
                        if user in room.users:
                            if current_waiting_room[0] == '':
                                current_waiting_room = (name,room)
                                room.request_say(original_command,text,raum,user,send=True)
                            if not name == current_waiting_room[0]:
                                # Der Benutzer hat gerade den Raum gewechselt, das Gespräch muss folgen!
                                current_waiting_room[1].request_say(original_command,text,raum,user,cancel=True,send=True)
                                while True:
                                    cancel_response = current_waiting_room[1].request_say(original_command, text, raum, user, cancel=True)
                                    if not cancel_response == 'ongoing':
                                        break
                                    time.sleep(0.03)
                                if cancel_response == False:
                                    # Konnte nicht abgebrochen werden, wurde bereits gesagt
                                    # Und Ja, das heißt wirklich "wurde bereits gesagt" und nicht "wird gerade gesagt",
                                    # weil in dem Fall im Raum die Requests gar nicht erst bearbeitet werden können...
                                    return
                                # Alles okay, wir fragen bei einem anderen Raum nach
                                current_waiting_room[1].request_end_Conversation(original_command)
                                current_waiting_room = (name,room)
                                room.request_say(original_command,text,raum,user,send=True)
                            if room.request_say(original_command, text, raum, user) == True:
                                return
                    time.sleep(0.03)
            else:
                # Der Text soll in einem bestimmten Raum gesagt werden
                # Zuerst mal WebSocket fragem, ob der Raum bekannt ist
                if TWebsocket.tellUserInRoom(user, raum, text):
                    # Der Raum war ein WebSocket-Raum und der Text wurde gesendet.
                    return
                for name, room in self.rooms.items():
                    if name.lower() == raum.lower():
                        # Dem Raum den Auftrag erteilen, es zu sagen
                        room.request_say(original_command, text, raum, user, send=True)
                        # Warten, bis der Raum bestätigt, es gesagt zu haben
                        while room.request_say(original_command, text, raum, user) == False:
                            time.sleep(0.03)
                        return
                    
        def route_play(self, original_command, audiofile, raum, user, output, priority):
            if self.presentation_mode and user in self.Users.userlist:
                output = 'speech'
            Log.write('DEBUG', {'Action': 'route_play()', 'conv_id': original_command, 'raum': raum, 'user': user,
                                'output': output, 'priority': priority}, conv_id=original_command, show=False)
            if ('telegram' in output.lower()) or (user not in self.Users.userlist and user is not None):
                if self.telegram is not None:
                    # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, an wen die Audio gesendet werden soll. Einfach beenden.
                    if user == None or user == 'Unknown':
                        Log.write('WARNING',
                                  'Eine Audiodatei konnte nicht abgespielt werden, da kein Nutzer als Ziel angegeben wurde',
                                  conv_id=original_command, show=True)
                        return
                    try:
                        uid = self.local_storage['TIANE_telegram_name_to_id_table'][user]
                        self.telegram.sendAudio(audiofile, self.local_storage['TIANE_telegram_name_to_id_table'][user],
                                                original_command)
                    except KeyError:
                        Log.write('WARNING',
                                  'Eine Audiodatei konnte nicht abgespielt werden, da kein Nutzer als Ziel angegeben wurde',
                                  conv_id=original_command, show=True)
                    return
                else:
                    Log.write('ERROR',
                              'Eine Audiodatei sollte via Telegram gesendet werden, obwohl Telegram nicht eingerichtet ist!'.format(
                                  audiofile), conv_id=original_command, show=True)
                    return
            if raum == None:
                # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, wo die Audio abgespielt werden soll. Einfach beenden.
                if user == None or user == 'Unknown':
                    Log.write('WARNING',
                              'Eine Audiodatei konnte nicht abgespielt werden, da kein Nutzer als Ziel angegeben wurde',
                              conv_id=original_command, show=True)
                    return
                # Die Audio soll bei einem bestimmten user abgespielt werden
                current_waiting_room = ('', None)
                while True:
                    for name, room in self.rooms.items():
                        if user in room.users:
                            if current_waiting_room[0] == '':
                                current_waiting_room = (name, room)
                                room.request_play(original_command, audiofile, raum, user, priority, send=True)
                            if not name == current_waiting_room[0]:
                                # Der Benutzer hat gerade den Raum gewechselt, die Audio muss folgen!
                                current_waiting_room[1].request_play(original_command, audiofile, raum, user, priority,
                                                                     cancel=True,
                                                                     send=True)
                                while True:
                                    cancel_response = current_waiting_room[1].request_play(original_command, audiofile,
                                                                                           raum,
                                                                                           user, priority, cancel=True)
                                    if not cancel_response == 'ongoing':
                                        break
                                    time.sleep(0.03)
                                if cancel_response == False:
                                    # Konnte nicht abgebrochen werden, wurde bereits abgespielt
                                    # Und Ja, das heißt wirklich "wurde bereits abgespielt" und nicht "wird gerade abgespielt",
                                    # weil in dem Fall im Raum die Requests gar nicht erst bearbeitet werden können...
                                    return
                                # Alles okay, wir fragen bei einem anderen Raum nach
                                current_waiting_room[1].request_end_Conversation(original_command)
                                current_waiting_room = (name, room)
                                room.request_play(original_command, audiofile, raum, user, priority, send=True)
                            if room.request_play(original_command, audiofile, raum, user, priority) == True:
                                return
                    time.sleep(0.03)
            else:
                # Die Audio soll in einem bestimmten Raum abgespielt werden
                for name, room in self.rooms.items():
                    if name.lower() == raum.lower():
                        # Dem Raum den Auftrag erteilen, es abzuspielen
                        room.Clientconnection.send({'TIANE_audio_play': audiofile})
                        room.request_play(original_command, audiofile, raum, user, send=True)
                        # Warten, bis der Raum bestätigt, es abgespielt zu haben
                        while room.request_play(original_command, audiofile, raum, user) == False:
                            time.sleep(0.03)
                        return
                    
        def route_listen(self, original_command, user, telegram=False):
            # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, wem TIANE zuhören soll. Einfach beenden.
            if user == None or user == 'Unknown':
                Log.write('WARNING', 'Für einen Aufruf von tiane.listen() konnte kein user als Ziel ermittelt werden.', conv_id=original_command, show=True)
                return 'TIMEOUT_OR_INVALID'
            # Tiane soll einem bestimmten user zuhören
            # Ist der user in einem WebSocket raum?
            ws_answer = TWebsocket.listen(user, self.local_storage)
            if ws_answer is not None:
                return ws_answer
            current_waiting_room = ('',None)
            if self.telegram is not None:
                if telegram == True or user not in self.Users.userlist:
                    # Dem Telegram-Thread Bescheid sagen, dass man auf eine Antwort wartet,
                    # aber erst, wenn kein anderer mehr wartet
                    while True:
                        if not user in self.telegram_queued_users:
                            self.telegram_queued_users.append(user)
                            break
                        time.sleep(0.03)
            else:
                telegram = False
            while True:
                if telegram:
                    # Schauen, ob die Telegram-Antwort eingegangen ist
                    response = self.telegram_queue_output.pop(user, None)
                    if response is not None:
                        self.telegram_queued_users.remove(user)
                        Log.write('ACTION', '--{}-- (Telegram): {}'.format(user.upper(), response['text']), conv_id=original_command, show=True)
                        return response
                else:
                    for name, room in self.rooms.items():
                        if user in room.users:
                            if current_waiting_room[0] == '':
                                current_waiting_room = (name,room)
                                room.request_listen(original_command,user,send=True)
                            if not name == current_waiting_room[0]:
                                # Der Benutzer hat gerade den Raum gewechselt, das Gespräch muss folgen!
                                current_waiting_room[1].request_listen(original_command,user,cancel=True,send=True)
                                while True:
                                    cancel_response = current_waiting_room[1].request_listen(original_command, user, cancel=True)
                                    if not cancel_response == 'ongoing':
                                        break
                                    time.sleep(0.03)
                                if not cancel_response == True:
                                    # Konnte nicht abgebrochen werden, wurde bereits gesagt
                                    return cancel_response # , die in diesem Fall nämlich praktischerweise die Antwort des Nutzers enthält...
                                # Alles okay, wir fragen bei einem anderen Raum nach
                                current_waiting_room[1].request_end_Conversation(original_command)
                                current_waiting_room = (name,room)
                                room.request_listen(original_command,user,send=True)
                            response = room.request_listen(original_command, user)
                            if not response == False:
                                return response
                time.sleep(0.03)

        def route_query_modules(self, user, name=None, text=None, room=None, direct=False, origin_room=None, data=None, must_be_secure=False): #direct: True = Sprachaufruf , must_be_secure: True = Nur server module die SECURE markiert sind.
            room, name = self.get_context(user, name, text, room, direct, origin_room)
            if not room == None:
                if room == self.server_name:
                    return self.Modules.query_threaded(user, name, text, direct=direct, origin_room=origin_room, data=data, must_be_secure=must_be_secure)
                else:
                    if not must_be_secure:
                        for room_name, raum in self.rooms.items():
                            if room_name.lower() == room.lower():
                                response = raum.request_query_modules(user, name=name, text=text, direct=direct, origin_room=origin_room, data=data)
                                # Bin mir mit dem folgenden Abschnitt noch nicht ganz sicher. Eigentlich ist ein möglicher Zielraum doch (bei Sprachaufruf) das letzte,
                                # was durchsucht werden muss... oder meint get_context was anderes..? Sagen wir mal, das hier kann man entfernen, wenn das Programm mal gut über mehrere Räume getestet ist :)
                                '''if response == False:
                                    # Die Anfrage könnte auch "aus Versehen" an den Raum gegangen sein, man sollte
                                    # zumindest noch die eigenen user- und common-modules befragen.
                                    return self.Modules.query_threaded(user, name, text, direct=direct, origin_room=origin_room)
                                else:'''
                                return response
            else:
                return self.Modules.query_threaded(user, name, text, direct=direct, origin_room=origin_room, data=data, must_be_secure=must_be_secure)

        def speechVariation(self, input):
            """
            This function is the counterpiece to the batchGen-function. It compiles the same
            sentence-format as given there but it only picks one random variant and directly
            pushes it into tiane. It returns the generated sentence.
            """
            if not isinstance(input, str):
                parse = random.choice(input)
            else:
                parse = input
            while "[" in parse and "]" in parse:
                t_a = time.time()
                sp0 = parse.split("[",1)
                front = sp0[0]
                sp1 = sp0[1].split("]",1)
                middle = sp1[0].split("|",1)
                end = sp1[1]
                t_b = time.time()
                parse = front + random.choice(middle) + end
            return parse

        def add_to_context(self, user, module, room, origin_room):
            # Wir speichern einfach mal so auf Verdacht auf ganz verschiedene Arten Nutzer, Raum und Modul der Anfrage ab...
            # Context-Dictionary initialisieren, falls noch nicht vorhanden
            try:
                test = self.local_storage['TIANE_context']
            except KeyError:
                self.local_storage['TIANE_context'] = {}

            self.local_storage['TIANE_context'][user] = (room,module)
            self.local_storage['TIANE_context'][origin_room] = (room,module)
            self.local_storage['TIANE_context'][module] = (user,room)


        def get_context(self, user, name, text, room, direct, origin_room):
            # Lädt das zuletzt aufgerufene Modul, wenn der Nutzer seine Anfrage mit "und" beginnt.
            # Grundvoraussetzung, die gegeben sein muss: Das Modul muss per Sprachbefehl aufgerufen worden sein!

            if name == None and not text == None and direct == True and not (user == None or user == 'Unknwon'):
                if text.lower().startswith('und ') or (text.lower().startswith('noch') and ('ein' in text.lower() or 'mal' in text.lower())):
                    # Es wird unterschieden zwischen drei Fällen:
                    # 1.: selber Nutzer, selbes Thema, ggf. anderer Raum (Wetter in ...; und in ...)
                    # 2.: selber Raum, selbes Thema, ggf. anderer Nutzer (Wer bin ich; und ich)
                    # 3.: selber Nutzer, selbes Thema, anderer Raum gemeint (Mach das Licht im ... an; und im ...)

                    # Fall 3
                    try:
                        target_room = self.Analyzer.analyze(text)['room']
                    except:
                        traceback.print_exc()
                        Log.write('ERROR', 'Satzanalyse fehlgeschlagen!', conv_id=text, show=True)
                        target_room = 'None'
                    if not target_room == 'None':
                        new_room = None
                        new_name = None
                        try:
                            new_name = self.local_storage['TIANE_context'][user][0]
                            new_room = target_room
                        except:
                            pass
                        if new_room is not None and new_name is not None:
                            return new_room, new_name

                    # Fall 1
                    if not (user == None or user == 'Unknown'):
                        new_room = None
                        new_name = None
                        try:
                            new_room,new_name = self.local_storage['TIANE_context'][user]
                        except:
                            pass
                        if new_room is not None and new_name is not None:
                            return new_room, new_name

                    # Fall 2 # gehört als letztes. WEIL: die Wahrscheinlichkeit, dass irgendein Nutzer im Raum schon mal "und" gesagt hat, ist höher als bei einem Nutzer ;)...
                    if not origin_room == None:
                        new_room = None
                        new_name = None
                        try:
                            new_room,new_name = self.local_storage['TIANE_context'][origin_room]
                        except:
                            pass
                        if new_room is not None and new_name is not None:
                            return new_room, new_name
                    else:
                        Log.write('ERROR', '[Einfach dem Ferdi schicken, der weiß (ungefähr), wo das Problem ist]\n'
                                           'Tipp: Es hat was damit zu tun, dass add_to_context eben nur "ZIEMLICH SICHER" einen origin_room erhält...',
                                           conv_id=text, show=True)
            return room, name

        def end_Conversation(self,original_command):
            for room in self.rooms.values():
                room.request_end_Conversation(original_command)

        def sendWebSocketEvent(self, event: str, data: dict):
            TWebsocket.sendEvent(event, data)

        def translate(self, text, targetLang='de'):
            try:
                request = Request(
                'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=' + urllib.parse.quote(targetLang) + '&dt=t&q=' + urllib.parse.quote(
                     text))
                response = urlopen(request)
                answer = json.loads(response.read())
                return answer[0][0][0]
            except:
                return text

    class Logging:
        def __init__(self):
            self.log = []

        def write(self, typ, content, info=None, conv_id=None, show=False):
            if info is not None:
                logentry = info
            else:
                logentry = {}
            logentry['time'] = time.strftime('%y_%m_%d %H:%M:%S', time.localtime(time.time()))
            logentry['type'] = typ
            logentry['content'] = content
            logentry['show'] = show
            logentry['conv_id'] = conv_id
            try:
                last_logentry = self.log[-1]
            except IndexError:
                last_logentry = logentry
            self.log.append(logentry)
            if show:
                print(self.format(logentry, last_logentry))

        def format(self, logentry, last_logentry):
            if logentry['type'] == 'ERROR' or logentry['type'] == 'WARNING' or logentry['type'] == 'DEBUG' or logentry['type'] == 'INFO' or logentry['type'] == 'TRACE':
                spaces = ''
                if last_logentry['type'] == 'ACTION':
                    spaces = '\n\n'
                    if last_logentry['conv_id'] == logentry['conv_id']:
                        spaces = ''
                textline = spaces + '[{}] '.format(logentry['type']) + logentry['content']

            elif logentry['type'] == 'ACTION':
                spaces = ''
                if not last_logentry['type'] == 'ACTION':
                    spaces = '\n\n'
                    if last_logentry['conv_id'] == logentry['conv_id']:
                        spaces = ''
                else:
                    if not last_logentry['conv_id'] == logentry['conv_id']: # conversation_id wird am Anfang original_command sein, aber in weiser Voraussicht hab ich das schon mal umbenannt...
                        spaces = '\n'
                    if last_logentry['conv_id'] == 'HW_DETECTED':
                        spaces = ''
                textline = spaces + logentry['content']

            else:
                textline = logentry['content']
            return textline


    class Room_Dock:
        def __init__(self, clientconnection, addr):
            self.addr = addr
            self.Clientconnection = clientconnection

            self.name = ''

            self.users = []

            self.room_guessed_user = ''
            self.server_guessed_user = ''

            self.distribute_dict = {} # Cache für send_update_information

            rt = Thread(target=self.start_connection)
            rt.daemon = True
            rt.start()

        def request_say(self, original_command, text, raum, user, cancel=False, send=False):
            # Verschickt Anfragen zum Sagen an den Raum und returnt True, wenn diese gesagt wurden
            # user hat den Raum gewechselt; Anfrage abbrechen, sofern noch möglich!
            if cancel == True:
                if send == True:
                    self.Clientconnection.send_buffer({'TIANE_room_cancel_say':[original_command]})
                    return
                response = self.Clientconnection.readanddelete('TIANE_room_confirms_cancel_say_{}'.format(original_command))
                if response is not None:
                    return response
                else:
                    return 'ongoing'
            # alles normal, einfach auf Bestätigung warten
            else:
                if send == True:
                    self.Clientconnection.send_buffer({'TIANE_room_say':[{'original_command':original_command,'text':text,'room':raum,'user':user}]})
                    return
                response = self.Clientconnection.readanddelete('TIANE_room_confirms_say_{}'.format(original_command))
                if response is not None:
                    return True
                else:
                    return False
                
        def request_play(self, original_command, audiofile, raum, user, priority, cancel=False, send=False):
            # Verschickt Audiodateien zum Abspielen an den Raum und returnt True, wenn diese abgespielt wurden
            # user hat den Raum gewechselt; Anfrage abbrechen, sofern noch möglich!
            try:
                if cancel == True:
                    if send == True:
                        self.Clientconnection.send_buffer({'TIANE_room_cancel_play': [original_command]})
                        return
                    response = self.Clientconnection.readanddelete(
                        'TIANE_room_confirms_cancel_play_{}'.format(original_command))
                    if response is not None:
                        return response
                    else:
                        return 'ongoing'
                # alles normal, einfach auf Bestätigung warten
                else:
                    if send == True:
                        self.Clientconnection.send_buffer({'TIANE_room_play': [
                            {'original_command': original_command, 'audiofile': audiofile, 'room': raum,
                             'user': user, 'priority': priority}]})
                        return
                    response = self.Clientconnection.readanddelete(
                        'TIANE_room_confirms_play_{}'.format(original_command))
                    if response is not None:
                        return True
                    else:
                        return False
            except:
                traceback.print_exc()
                
        def request_listen(self, original_command, user, cancel=False, send=False):
            # Verschickt Anfragen zum Zuhören an den Raum und returnt den gesprochenen Text, sofern fertig
            # user hat den Raum gewechselt; Anfrage abbrechen, sofern noch möglich!
            if cancel == True:
                if send == True:
                    self.Clientconnection.send_buffer({'TIANE_room_cancel_listen':[original_command]})
                    return
                response = self.Clientconnection.readanddelete('TIANE_room_confirms_cancel_listen_{}'.format(original_command))
                if response is not None:
                    if response == True:
                        # True: erfolgreich abgebrochen
                        return True
                    else:
                        response = self.Clientconnection.readanddelete('TIANE_room_confirms_listen_{}'.format(original_command))
                        if response is not None:
                            # response: Antwort des Nutzers; es war wohl schon zu spät zum abbrechen
                            return response
                # ongoing: Man wartet noch
                return 'ongoing'
            # alles normal, einfach auf Antwort warten
            else:
                if send == True:
                    self.Clientconnection.send_buffer({'TIANE_room_listen':[{'original_command':original_command,'user':user}]})
                    return
                response = self.Clientconnection.readanddelete('TIANE_room_confirms_listen_{}'.format(original_command))
                if response is not None:
                    return response
                else:
                    return False

        def request_query_modules(self, user, name=None, text=None, direct=False, origin_room=None, data=None):
            if not text == None:
                original_command = text
            else:
                original_command = name
            self.Clientconnection.send_buffer({'TIANE_room_query_modules':[{'original_command':original_command, 'user':user, 'text':text, 'name':name, 'direct':direct, 'origin_room':origin_room, 'data':data}]})
            while True:
                response = self.Clientconnection.readanddelete('TIANE_room_confirms_query_modules_{}'.format(original_command))
                if response is not None:
                    return response
                time.sleep(0.03)

        def request_end_Conversation(self, original_command):
            self.Clientconnection.send_buffer({'TIANE_room_end_Conversation':[original_command]})

        def handle_online_requests(self):
            say_requests = []
            listen_requests = []
            play_requests = []
            query_requests = []

            while True:
                # SAY
                # Neue Aufträge einholen
                new_say_requests = self.Clientconnection.readanddelete('TIANE_server_say')
                if new_say_requests is not None:
                    for request in new_say_requests:
                        for existing_request in say_requests:
                            if request['original_command'] == existing_request['original_command']:
                                break
                        else:
                            say_requests.append(request)
                # Aufträge bearbeiten
                for request in say_requests:
                    rst = Thread(target = self.thread_say, args=(request,))
                    rst.daemon = True
                    rst.start()
                    say_requests.remove(request)
                
                # PLAY
                # Neue Aufträge einholen
                new_play_requests = self.Clientconnection.readanddelete('TIANE_server_play')
                if new_play_requests is not None:
                    for request in new_play_requests:
                        for existing_request in play_requests:
                            if request['original_command'] == existing_request['original_command']:
                                break
                        else:
                            play_requests.append(request)
                # Aufträge bearbeiten
                for request in play_requests:
                    rst = Thread(target=self.thread_play, args=(request,))
                    rst.daemon = True
                    rst.start()
                    play_requests.remove(request)
                    
                # LISTEN
                # Neue Aufträge einholen
                new_listen_requests = self.Clientconnection.readanddelete('TIANE_server_listen')
                if new_listen_requests is not None:
                    for request in new_listen_requests:
                        for existing_request in listen_requests:
                            if request['original_command'] == existing_request['original_command']:
                                break
                        else:
                            listen_requests.append(request)
                # Aufträge bearbeiten
                for request in listen_requests:
                    rlt = Thread(target = self.thread_listen, args=(request,))
                    rlt.daemon = True
                    rlt.start()
                    listen_requests.remove(request)

                # QUERY_MODULES
                # Neue Aufträge einholen
                new_query_requests = self.Clientconnection.readanddelete('TIANE_server_query_modules')
                if new_query_requests is not None:
                    for request in new_query_requests:
                        for existing_request in query_requests:
                            if request['original_command'] == existing_request['original_command']:
                                break
                        else:
                            query_requests.append(request)
                # Aufträge bearbeiten
                for request in query_requests:
                    response = Tiane.route_query_modules(request['user'], name=request['name'], text=request['original_command'], room=request['room'], direct=request['direct'], origin_room=self.name)
                    self.Clientconnection.send({'TIANE_server_confirms_query_modules_{}'.format(request['original_command']):response})
                    query_requests.remove(request)

                # END_CONVERSATION
                end_conversation_requests = self.Clientconnection.readanddelete('TIANE_server_end_Conversation')
                if end_conversation_requests is not None:
                    for request in end_conversation_requests:
                        Tiane.end_Conversation(request)

                # ADD_CONTEXT
                add_context_requests = self.Clientconnection.readanddelete('TIANE_context')
                if add_context_requests is not None:
                    for request in add_context_requests:
                        Tiane.add_to_context(request['user'], request['module'], request['room'], self.name)

                # VOICE_RECOGNITION
                voice_recognition_request = self.Clientconnection.readanddelete('TIANE_user_voice_recognized')
                if voice_recognition_request is not None:
                    self.room_guessed_user = voice_recognition_request
                if not self.server_guessed_user == '':
                    self.Clientconnection.send({'TIANE_user_server_guess':self.server_guessed_user})
                    Log.write('ACTION', '--listening to {} (room: {})--'.format(self.server_guessed_user, self.name), conv_id='HW_DETECTED', show=True)
                    self.server_guessed_user = ''

                # LOGGING
                new_logging_requests = self.Clientconnection.readanddelete('TIANE_LOG')
                if new_logging_requests is not None:
                    for request in new_logging_requests:
                        Log.write(request['type'], request['content'], info=request['info'], conv_id=request['conv_id'], show=request['show'])

                # SEND_UPDATE_INFORMATION
                self.send_update_information()

                # VERBINDUNG PRÜFEN
                if self.Clientconnection.connected == False:
                    break

                time.sleep(0.03)

        def send_update_information(self):
            # Verteilt die in keys_to_distribute festgelegten Daten aus dem Local_storage an die Räume
            information_dict = {}
            for key in Tiane.local_storage['keys_to_distribute']:
                if not key in Tiane.local_storage.keys():
                    Log.write('WARNING', 'Der Schlüssel {} ist in local_storage nicht vorhanden und kann daher nicht an die Räume verteilt werden!'.format(key), show=True)
                    Tiane.local_storage['keys_to_distribute'].remove(key)
                    continue
                information_dict[key] = Tiane.local_storage[key]
            self.Clientconnection.send({'TIANE_server_info':information_dict})

        def thread_say(self, request):
            Tiane.route_say(request['original_command'],request['text'],request['room'],request['user'], request['output'])
            self.Clientconnection.send({'TIANE_server_confirms_say_{}'.format(request['original_command']):True})
        
        def thread_play(self, request):
            Tiane.route_play(request['original_command'], request['audiofile'], request['room'], request['user'],
                            request['output'])
            self.Clientconnection.send({'TIANE_server_confirms_say_{}'.format(request['original_command']): True})
        
        def thread_listen(self, request):
            response = Tiane.route_listen(request['original_command'],request['user'], telegram=request['telegram'])
            self.Clientconnection.send({'TIANE_server_confirms_listen_{}'.format(request['original_command']):response})

        def recvall(self, sock, count):
            buf = b''
            while count:
                newbuf = sock.recv(count)
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
            return buf

        def start_connection(self):
            # Informationen über den Raum empfangen...
            time.sleep(0.5)
            while True:
                information_dict = self.Clientconnection.readanddelete('TIANE_room_info')
                if information_dict is not None:
                    self.name = information_dict['name']
                    Rooms[self.name] = Devices_connecting[self.addr]
                    del Devices_connecting[self.addr]
                    Room_list.append(self.name)
                    Tiane.local_storage['rooms'][self.name] = {'name':self.name, 'users':[]}
                    Tiane.Analyzer.room_list = Room_list
                    break
                time.sleep(0.01)

            # ...und Informationen an den Raum senden.
            self.send_update_information()
            Log.write('INFO', 'Verbindung mit Raum {} hergestellt'.format(self.name), show=True)

            # Alles geklärt, jetzt zur eigentlichen Aufgabe dieser Klasse...
            self.handle_online_requests()

            # Raum ist offline? Aufräumen!
            Room_list.remove(self.name)
            del Rooms[self.name]
            del Tiane.local_storage['rooms'][self.name]
            for user in Local_storage['users'].values():
                try:
                    if user['room'] == self.name:
                        del user['room']
                except KeyError:
                    continue
            Log.write('WARNING', 'Verbindung mit Raum {} unterbrochen'.format(self.name), show=True)


    class Network_Device:
        def __init__(self, conn, addr):
            self.conn = conn
            self.addr = addr
            self.Clientconnection = TNetwork_Connection_Server()
            self.Clientconnection.key = TNetwork_Key

            self.type = ''
            self.name = ''

            self.storage = {} # Speicher für beliebige, das Gerät betreffende Daten

            ndt = Thread(target=self.start_connection)
            ndt.daemon = True
            ndt.start()

        def start_connection(self):
            try:
                self.Clientconnection.connect(self.conn, self.addr)
            except:
                del Devices_connecting[self.addr]
                return

            # Herausfinden, um was für ein Gerät es sich handelt
            while True:
                device_type = self.Clientconnection.read('DEVICE_TYPE')
                if device_type is not None:
                    if device_type == 'TIANE_ROOM':
                        # Oh, ein Raum? Übergeben an Room_Dock!
                        Devices_connecting[self.addr] = Room_Dock(self.Clientconnection, self.addr)
                        return
                    else:
                        device_name = self.Clientconnection.read('DEVICE_NAME')
                        if device_name is not None:
                            Other_devices[device_name] = Devices_connecting[self.addr]
                            del Devices_connecting[self.addr]
                            self.type = device_type
                            self.name = device_name
                            Log.write('INFO', 'Verbindung mit Gerät {} ({}) hergestellt'.format(self.name, self.type), show=True)
                            break
                time.sleep(0.03)

            # Es handelt sich um ein proprietäres Gerät. Einfach die Verbindung halten.
            while True:
                if self.Clientconnection.connected == False:
                    del Other_devices[self.name]
                    Log.write('INFO', 'Verbindung mit Gerät {} ({}) unterbrochen'.format(self.name, self.type))
                    break
                time.sleep(0.5)


    def updateFeedback():
        if feedbackMap is not None:
            feedbackMap.seek(0)
            newPick = pickle.dumps(Local_storage)
            feedbackMap.write(newPick)
            time.sleep(0.25)
            # TODO: check command-mmap and execute corresponding commands

    #################################################-MAIN-################################################
    java_start = False
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'jni':
            java_start = True
            print('TIANE wurde von java aus gestartet.')

    relPath = str(Path(__file__).parent) + "/"
    absPath = os.path.dirname(os.path.abspath(__file__))

    Log = Logging()

    if java_start:
        jiane.createJavalogger(Log)

    # aus TIANE_config.json laden
    with open(relPath+'TIANE_config.json', 'r') as config_file:
        config_data = json.load(config_file)

    System_name = config_data['System_name']
    Server_name = config_data['Server_name']
    Home_location = config_data["Home_location"]
    Local_storage = config_data['Local_storage']
    websocket_mode = config_data['websocket']
    TNetwork_Key = base64.b64decode(config_data['TNetwork_Key'].encode('utf-8')) # sehr umständliche Decoder-Zeile. Leider nötig :(

    Local_storage['TIANE_PATH'] = absPath

    # !!!!!!!!!!!!!!!!! ACHTUNG !!!!!!!!!!!!!!!!! #
    # Open_mode ist nur für Vorführungen und stellt ein enormes Sicherheitsrisiko dar,
    # da so auch unautorisierte Nutzer Zugriff via Telegram haben!
    Open_mode = config_data['Open_mode']


    Devices_connecting = {}
    Rooms = {}
    Other_devices = {}

    Room_list = []

    Users = Users()
    Modules = Modules()
    Analyzer = Sentence_Analyzer(room_list=Room_list)
    Tiane = TIANE()
    Tiane.local_storage['TIANE_starttime'] = time.time()


    time.sleep(2)

    # ggf. das Telegram-Interface starten:
    if config_data['telegram']:
        Log.write('', '', show=True)
        Log.write('INFO', 'Starte Telegram...', show=True)
        if config_data['telegram_key'] == '':
            Log.write('ERROR', 'Kein Telegram-Bot-Token angegeben!', show=True)
        else:
            from resources.telegram import TelegramInterface
            Tiane.telegram = TelegramInterface(config_data['telegram_key'], Tiane)
            Tiane.telegram.start()
            tgt = Thread(target=Tiane.telegram_thread)
            tgt.daemon = True
            tgt.start()
        Log.write('', '', show=True)


    Tiane.Modules.start_continuous()

    if websocket_mode.lower() == 'disabled':
        pass
    elif websocket_mode.lower() == 'enabled':
        Log.write('INFO', 'Starte WebSocket...', show=True)
        TWebsocket.startWsServer(Tiane, config_data['websocket_port'], True, config_data['websocket_timeout'])
    elif websocket_mode.lower() == 'secure':
        Log.write('INFO', 'Starte WebSocket... (secure)', show=True)
        TWebsocket.startWsServer(Tiane, config_data['websocket_port'], False, config_data['websocket_timeout'])
    else:
        Log.write('ERROR', 'Fehlerhaft Konfiguration: WebSocket-Modus nicht bekannt.', show=True)

    # Setzt einen socket auf einem freien Port >= 50000 auf.
    port = 50000
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('',port))
            break
        except:
            sock.close()
            port += 1
            continue
    Log.write('DEBUG', 'Server Port: {}'.format(port), show=False)

    sock.listen(True)
    time.sleep(1.5)

    if (java_start):
        jiane.setSignalHandlers()
        sock.settimeout(0.1)
        # Da Signal-Handling nicht wie gewohnt funktioniert, wenn Python von
        # java gestartet wird, muss regelmäßig geprüft werden, ob TIANE beendet
        # werden soll. Deswegen der Timeout.

    Log.write('', '--------- FERTIG ---------\n\n', show=True)

    # "Hauptschleife"
    while True:
        # Socket steht, auf Verbindung warten
        try:
            if java_start and jiane.shouldStop():
                raise KeyboardInterrupt
            conn, addr = sock.accept()
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            Log.write('', '\n', show=True)
            break
        # Ein entsprechendes Geräte-Objekt erstellen und ihm die Verbindung überlassen
        Devices_connecting[addr] = Network_Device(conn, addr)

    sock.close()
    Modules.stop_continuous()
    Log.write('', '------ Räume werden beendet...', show=True)
    if Rooms == {}:
        Log.write('INFO', '-- (Keine zu beenden)', show=True)
    for room in Rooms.values():
        room.Clientconnection.stop()
        Log.write('INFO', 'Raum {} beendet'.format(room.name), show=True)

    for device in Other_devices.values():
        device.Clientconnection.stop()
    Log.write('', '\n[{}] Auf wiedersehen!\n'.format(System_name.upper()), show=True)

if __name__ == "__main__":
    runMain()
