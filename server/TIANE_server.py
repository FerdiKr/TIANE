from TNetwork import TNetwork_Connection_Server
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

class Modules:
    def __init__(self):
        self.load_modules()

        self.Modulewrapper = Modulewrapper
        self.Modulewrapper_continuous = Modulewrapper_continuous

        self.continuous_stopped = False
        self.continuous_threads_running = 0

        self.modules_defined_vocabulary = []

    def load_modules(self):
        self.modules_defined_vocabulary = []
        print('----- COMMON_MODULES -----')
        self.common_modules = self.get_modules('modules')
        if self.common_modules == []:
            print('[INFO] -- (Keine vorhanden)')
        print('------ CONTINUOUS')
        self.common_continuous_modules = self.get_modules('modules/continuous',continuous=True)
        if self.common_continuous_modules == []:
            print('[INFO] -- (Keine vorhanden)')

        print('------ USER_MODULES ------')
        self.no_user_modules = True
        self.user_modules = self.get_user_modules()
        if self.no_user_modules == True:
            print('[INFO] -- (Keine vorhanden)')
        print('------ CONTINUOUS')
        self.no_user_continuous_modules = True
        self.user_continuous_modules = self.get_user_modules(continuous=True)
        if self.no_user_continuous_modules == True:
            print('[INFO] -- (Keine vorhanden)')
        Local_storage['TIANE_Modules_defined_Vocabulary'] = self.modules_defined_vocabulary

    def get_modules(self, directory, continuous=False):
        dirname = os.path.dirname(os.path.abspath(__file__))
        locations = [os.path.join(dirname, directory)]
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                traceback.print_exc()
                print('[WARNING] Modul {} ist fehlerhaft und wurde übersprungen!'.format(name))
            else:
                if continuous == True:
                    print('[INFO] Fortlaufendes Modul {} geladen'.format(name))
                    modules.append(mod)
                else:
                    print('[INFO] Modul {} geladen'.format(name))
                    modules.append(mod)
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
                    print('[WARNING] Modul {} (Nutzer: {}) ist fehlerhaft und wurde übersprungen!'.format(name, username))
                else:
                    if continuous == True:
                        print('[INFO] Fortlaufendes Modul {} (Nutzer: {}) geladen'.format(name, username))
                        modules.append(mod)
                        self.no_user_continuous_modules = False
                    else:
                        print('[INFO] Modul {} (Nutzer: {}) geladen'.format(name, username))
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

    def query_threaded(self, user, name, text, direct=False, origin_room=None):
        if text == None or text == '':
            text = random.randint(0,1000000000)
            analysis = {}
        else:
            print(text)
            try:
                analysis = Tiane.Analyzer.analyze(str(text))
                print(analysis)
            except:
                traceback.print_exc()
                print('[ERROR] Satzanalyse fehlgeschlagen!\n')
                analysis = {}

        if name is not None:
            # Modul wurde direkt aufgerufen
            for module in self.common_modules:
                if module.__name__ == name:
                    Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room)
                    mt = Thread(target=self.run_threaded_module, args=(text,module,))
                    mt.daemon = True
                    mt.start()
                    if direct:
                        Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                    return True
            for module in self.user_modules[user]:
                if module.__name__ == name:
                    Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room)
                    mt = Thread(target=self.run_threaded_module, args=(text,module,))
                    mt.daemon = True
                    mt.start()
                    if direct:
                        Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                    return True

        # Kein Direktaufruf? Ganz normal die Module durchgehen...
        for module in self.common_modules:
            try:
                if module.isValid(text):
                    Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room)
                    mt = Thread(target=self.run_threaded_module, args=(text,module,))
                    mt.daemon = True
                    mt.start()
                    if direct:
                        Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                    return True
            except:
                traceback.print_exc()
                print('[ERROR] Modul {} konnte nicht abgefragt werden!'.format(module.__name__))
        if user is not None:
            # ... Und wenn wir nen Nutzer haben, können wir auch noch in seinen Modulen suchen
            if not user == 'Unknown':
                for module in self.user_modules[user]:
                    try:
                        if module.isValid(text):
                            Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room)
                            mt = Thread(target=self.run_threaded_module, args=(text,module,))
                            mt.daemon = True
                            mt.start()
                            if direct:
                                Tiane.add_to_context(user, module.__name__, Tiane.server_name, origin_room)
                            return True
                    except:
                        traceback.print_exc()
                        print('[ERROR] Modul {} (Nutzer: {}) konnte nicht abgefragt werden!'.format(module.__name__, user))

        # Hier ist die Lösung, die dafür sorgt, dass die Anfrage ggf. an einen bestimmten
        # Raum weitergeleitet wird... Das macht Sinn: So bleiben Direktaufrufe
        # über den Modulnamen auf jeden Fall unbehelligt und nur so können Sonderfälle wie "Erinner mich... wenn ich in der Küche bin"
        # korrekt interpretiert werden!
        if not analysis == {}:
            if not analysis['room'] == 'None':
                return Tiane.route_query_modules(user, name, text, analysis['room'], direct=direct, origin_room=origin_room)

        return False

    def run_threaded_module(self, text, module):
        try:
            module.handle(text, Tiane.active_modules[str(text)], Tiane.local_storage)
        except:
            traceback.print_exc()
            print('[ERROR] Runtime-Error in Modul {}. Das Modul wurde beendet.\n'.format(module.__name__))
            Tiane.active_modules[str(text)].say('Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
        finally:
            del Tiane.active_modules[str(text)]
            Tiane.end_Conversation(text)
            return

    def start_continuous(self):
        # Startet den Thread, in dem die continuous_modules ausgeführt werden (siehe unten).
        print('---- STARTE MODULE... ----')
        self.continuous_threads_running = 0
        Local_storage['module_counter'] = {}
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
            print('[INFO] -- (Keine vorhanden)')
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
                print('[INFO] Modul {} (Nutzer: {}) gestartet'.format(module.__name__, user))
            except:
                #traceback.print_exc()
                pass
        Local_storage['module_counter'][user] = 0
        while True:
            for module in modules:
                # Continuous_modules können ein Zeitintervall definieren, in dem sie gerne
                # aufgerufen werden wollen, um Ressourcen zu sparen.
                if time.time() - Tiane.continuous_modules[user][module.__name__].last_call >= Tiane.continuous_modules[user][module.__name__].intervall_time:
                    Tiane.continuous_modules[user][module.__name__].last_call = time.time()
                    try:
                        module.run(Tiane.continuous_modules[user][module.__name__], Tiane.local_storage)
                        Tiane.continuous_modules[user][module.__name__].counter += 1
                    except:
                        traceback.print_exc()
                        print('[ERROR] Runtime-Error in Continuous-Module {} (Nutzer "{}"). Das Modul wird nicht mehr ausgeführt.\n'.format(module.__name__, user))
                        del Tiane.continuous_modules[user][module.__name__]
                        modules.remove(module)
            if self.continuous_stopped:
                break
            Local_storage['module_counter'][user] += 1
            time.sleep(0.01)
        self.continuous_threads_running -= 1
        return

    def stop_continuous(self):
        # Stoppt den Thread, in dem die continuous_modules ausgeführt werden, am Ende des Durchlaufs.
        # Gibt den Modulen aber danach noch eine Gelegenheit, aufzuräumen...
        if self.continuous_threads_running > 0:
            print('------ Module werden beendet...')
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
                    print('[INFO] Modul {} (Nutzer: {}) beendet'.format(module.__name__, 'common'))
                    no_stopped_modules = False
                except:
                    pass
            for user, modules in self.user_continuous_modules.items():
                for module in modules:
                    try:
                        module.stop(Tiane.continuous_modules[user][module.__name__], Tiane.local_storage)
                        print('[INFO] Modul {} (Nutzer: {}) beendet'.format(module.__name__, user))
                        no_stopped_modules = False
                    except:
                        pass
            # aufräumen
            Tiane.continuous_modules = {}
            if no_stopped_modules == True:
                print('[INFO] -- (Keine zu beenden)')
        return



class Modulewrapper:
    # Diese Klasse ist wichtig: Module bekommen sie anstelle einer "echten" Tiane-Instanz
    # vorgesetzt. Denn es gibt nur eine Tiane-Instanz, um von dort aus alles regeln zu
    # können, aber Module brauchen verschiedene Instanzen, die Informationen über sie ent-
    # halten müssen, z.B. welcher Nutzer das Modul aufgerufen hat. Diese Informationen
    # ergänzt diese Klasse und schleift ansonsten einfach alle von Modulen aus aufrufbaren
    # Funktionen an die Hauptinstanz von Tiane durch.
    def __init__(self, text, analysis, user, origin_room):
        self.text = text # original_command
        self.analysis = analysis
        self.user = user
        self.room = origin_room

        self.core = Tiane
        self.Analyzer = Tiane.Analyzer
        self.rooms = Tiane.rooms
        self.other_devices = Tiane.other_devices
        self.local_storage = Tiane.local_storage
        self.userlist = Tiane.userlist
        self.room_list = Tiane.room_list
        self.server_name = Tiane.server_name
        self.system_name = Tiane.system_name
        self.path = Tiane.path

    def say(self, text, room=None, user=None):
        if user == None or user == 'Unknown':
            user = self.user
        if user == None or user == 'Unknown': # Immer noch? Kann durchaus sein...
            room = self.room
        Tiane.route_say(self.text, text, room, user)

    def listen(self, user=None):
        if user == None or user == 'Unknown':
            user = self.user
        text = Tiane.route_listen(self.text, user)
        return text

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

        self.core = Tiane
        self.Analyzer = Tiane.Analyzer
        self.rooms = Tiane.rooms
        self.other_devices = Tiane.other_devices
        self.local_storage = Tiane.local_storage
        self.userlist = Tiane.userlist
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


class TIANE:
    def __init__(self):
        self.Modules = Modules
        self.Analyzer = Analyzer

        self.active_modules = {}
        self.continuous_modules = {}
        self.rooms = Rooms
        self.other_devices = Other_devices
        self.devices_connecting = Devices_connecting

        self.local_storage = Local_storage
        self.userlist = Userlist
        self.room_list = Room_list
        self.server_name = Server_name
        self.system_name = System_name
        self.path = Local_storage['TIANE_PATH']

    def start_module(self, user, name, text, room):
        if user == None or user == 'Unknown':
            user = random.choice(self.userlist)
        return self.route_query_modules(user, name=name, text=text, room=room)

    def route_say(self, original_command, text, raum, user):
        if raum == None:
            # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, wo der Text gesagt werden soll. Einfach beenden.
            if user == None or user == 'Unknown':
                print('[WARNING] Der Text "{}" konnte nicht gesagt werden, weil weder ein Raum noch ein Nutzer als Ziel angegeben wurden'.format(text))
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
            for name, room in self.rooms.items():
                if name.lower() == raum.lower():
                    # Dem Raum den Auftrag erteilen, es zu sagen
                    room.request_say(original_command, text, raum, user, send=True)
                    # Warten, bis der Raum bestätigt, es gesagt zu haben
                    while room.request_say(original_command, text, raum, user) == False:
                        time.sleep(0.03)
                    return

    def route_listen(self, original_command, user):
        # Spezialfall berücksichtigen: Es kann beim besten Willen nicht ermittelt werden, wem TIANE zuhören soll. Einfach beenden.
        if user == None or user == 'Unknown':
            print('[WARNING] Für einen Aufruf von tiane.listen() konnte kein user als Ziel ermittelt werden.')
            return 'TIMEOUT_OR_INVALID'
        # Tiane soll einem bestimmten user zuhören
        current_waiting_room = ('',None)
        while True:
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

    def route_query_modules(self, user, name=None, text=None, room=None, direct=False, origin_room=None):
        room, name = self.get_context(user, name, text, room, direct, origin_room)
        if not room == None:
            if room == self.server_name:
                return self.Modules.query_threaded(user, name, text, direct=direct, origin_room=origin_room)
            else:
                for room_name, raum in self.rooms.items():
                    if room_name.lower() == room.lower():
                        response = raum.request_query_modules(user, name=name, text=text, direct=direct)
                        # Bin mir mit dem folgenden Abschnitt noch nicht ganz sicher. Eigentlich ist ein möglicher Zielraum doch (bei Sprachaufruf) das letzte,
                        # was durchsucht werden muss... oder meint get_context was anderes..? Sagen wir mal, das hier kann man entfernen, wenn das Programm mal gut über mehrere Räume getestet ist :)
                        '''if response == False:
                            # Die Anfrage könnte auch "aus Versehen" an den Raum gegangen sein, man sollte
                            # zumindest noch die eigenen user- und common-modules befragen.
                            return self.Modules.query_threaded(user, name, text, direct=direct, origin_room=origin_room)
                        else:'''
                        return response
        else:
            return self.Modules.query_threaded(user, name, text, direct=direct, origin_room=origin_room)

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
            if text.lower().startswith('und '):
                # Es wird unterschieden zwischen drei Fällen:
                # 1.: selber Nutzer, selbes Thema, ggf. anderer Raum (Wetter in ...; und in ...)
                # 2.: selber Raum, selbes Thema, ggf. anderer Nutzer (Wer bin ich; und ich)
                # 3.: selber Nutzer, selbes Thema, anderer Raum gemeint (Mach das Licht im ... an; und im ...)

                # Fall 3
                try:
                    target_room = self.Analyzer.analyze(text)['room']
                except:
                    traceback.print_exc()
                    print['[ERROR] Satzanalyse fehlgeschlagen!']
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
                    print('[ERROR] [Einfach dem Ferdi schicken, der weiß (ungefähr), wo das Problem ist]')
                    print('Tipp: Es hat was damit zu tun, dass add_to_context eben nur "ZIEMLICH SICHER" einen origin_room erhält...')
        return room, name

    def end_Conversation(self,original_command):
        for room in self.rooms.values():
            room.request_end_Conversation(original_command)


class Room_Dock:
    def __init__(self, clientconnection, addr):
        self.addr = addr
        self.Clientconnection = clientconnection

        self.name = ''

        self.users = []

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

    def request_query_modules(self, user, name=None, text=None, direct=False):
        if not text == None:
            original_command = text
        else:
            original_command = name
        self.Clientconnection.send_buffer({'TIANE_room_query_modules':[{'original_command':original_command, 'user':user, 'text':text, 'name':name, 'direct':direct}]})
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
        query_requests = []

        distribute_dict = {}

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

            # SEND_UPDATE_INFORMATION
            self.send_update_information()

            # VERBINDUNG PRÜFEN
            if self.Clientconnection.connected == False:
                break

            time.sleep(0.03)

    def send_update_information(self):
        # Verteilt die in keys_to_distribute festgelegten Daten aus dem Local_storage an die Räume,
        # aber nur, wenn sich diese gegenüber dem letzten Aufruf tatsächlich verändert haben, um
        # Ressourcen zu schonen.
        information_dict = {}
        for key in Tiane.local_storage['keys_to_distribute']:
            if not key in Tiane.local_storage.keys():
                print('[WARNING] Der Schlüssel {} ist in local_storage nicht vorhanden und kann daher nicht an die Räume verteilt werden!'.format(key))
                Tiane.local_storage['keys_to_distribute'].remove(key)
                continue
            if key in self.distribute_dict.keys():
                if self.distribute_dict[key] == Tiane.local_storage[key]:
                    continue
            information_dict[key] = Tiane.local_storage[key]
            self.distribute_dict[key] = Tiane.local_storage[key]
        if not information_dict == {}:
            self.Clientconnection.send({'TIANE_server_info':information_dict})

    def thread_say(self, request):
        Tiane.route_say(request['original_command'],request['text'],request['room'],request['user'])
        self.Clientconnection.send({'TIANE_server_confirms_say_{}'.format(request['original_command']):True})

    def thread_listen(self, request):
        response = Tiane.route_listen(request['original_command'],request['user'])
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
        print('[INFO] Verbindung mit Raum {} hergestellt'.format(self.name))

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
                pass
        print('[WARNING] Verbindung mit Raum {} unterbrochen'.format(self.name))


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
                        print('[INFO] Verbindung mit Gerät {} ({}) hergestellt'.format(self.name, self.type))
                        break
            time.sleep(0.03)

        # Es handelt sich um ein proprietäres Gerät. Einfach die Verbindung halten.
        while True:
            if self.Clientconnection.connected == False:
                del Other_devices[self.name]
                print('[WARNING] Verbindung mit Gerät {} ({}) unterbrochen'.format(self.name, self.type))
                break
            time.sleep(0.5)




#################################################-MAIN-#################################################

# aus TIANE_config.json laden
with open('TIANE_config.json', 'r') as config_file:
    config_data = json.load(config_file)

System_name = config_data['System_name']
Server_name = config_data['Server_name']
Local_storage = config_data['Local_storage']
TNetwork_Key = base64.b64decode(config_data['TNetwork_Key'].encode('utf-8')) # sehr umständliche Decoder-Zeile. Leider nötig :(

# Nutzer seperat aus dem users-Ordner laden
Local_storage['users'] = {}
dirname = os.path.dirname(os.path.abspath(__file__))
Local_storage['TIANE_PATH'] = dirname
location = os.path.join(dirname, 'users')
subdirs = os.listdir(location)
for subdir in subdirs:
    userpath = os.path.join(location, subdir)
    with open(userpath + '/User_Info.json', 'r') as user_file:
        user_data = json.load(user_file)
    user_data['User_Info']['path'] = userpath
    Local_storage['users'][subdir] = user_data['User_Info']
Userlist = []
for name in Local_storage['users'].keys():
    Userlist.append(name)


Devices_connecting = {}
Rooms = {}
Other_devices = {}

Room_list = []

Modules = Modules()
Analyzer = Sentence_Analyzer(room_list=Room_list)
Tiane = TIANE()
Tiane.local_storage['TIANE_starttime'] = time.time()

time.sleep(1)
Tiane.Modules.start_continuous()

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

sock.listen(True)
time.sleep(1.5)
print('--------- FERTIG ---------\n\n')

# "Hauptschleife"
while True:
    # Socket steht, auf Verbindung warten
    try:
        conn, addr = sock.accept()
    except KeyboardInterrupt:
        print('\n')
        break
    # Ein entsprechendes Raum-Objekt erstellen und ihm die Verbindung überlassen
    Devices_connecting[addr] = Network_Device(conn, addr)

sock.close()
Modules.stop_continuous()
print('------ Räume werden beendet...')
if Rooms == {}:
    print('[INFO] -- (Keine zu beenden)')
for room in Rooms.values():
    room.Clientconnection.stop()
    print('[INFO] Raum {} beendet'.format(room.name))

for device in Other_devices.values():
    device.Clientconnection.stop()
print('\n[{}] Auf wiedersehen!\n'.format(System_name.upper()))
