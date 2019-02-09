from TNetwork import TNetwork_Connection_Client
from TIANE_Audio import Audio_Output
from TIANE_Audio import Audio_Input
from analyze import Sentence_Analyzer
from threading import Thread
import snowboydecoder
import traceback
import random
import pkgutil
import time
import sys
import os

class Modules:
    def __init__(self):
        self.load_modules()

        self.Modulewrapper = Modulewrapper
        self.Modulewrapper_continuous = Modulewrapper_continuous

        self.continuous_stopped = False
        self.continuous_threads_running = 0

    def load_modules(self):
        print('------ ROOM_MODULES ------')
        self.modules = self.get_modules('modules')
        if self.modules == []:
            print('[INFO] -- (Keine vorhanden)')
        print('------ CONTINUOUS')
        self.continuous_modules = self.get_modules('modules/continuous',continuous=True)
        if self.continuous_modules == []:
            print('[INFO] -- (Keine vorhanden)')

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
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules


    def query_threaded(self, user, name, text, direct=False): # direct: Es handelt sich um einen direkten Sprachaufruf des Moduls. Etwas unintuitiv, da ich manchmal auch
                                                              # von einem Direktaufruf spreche, wenn das Modul "gezielt", also direkt, über start_module aufgerufen wird...
        if text == None:
            text = random.randint(0,1000000000)
            analysis = {}
        else:
            try:
                analysis = Tiane.Analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Satzanalyse fehlgeschlagen!')
                analysis = {}
        if not name == None:
            # Modul wurde per start_module aufgerufen
            for module in self.modules:
                if module.__name__ == name:
                    Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user)
                    mt = Thread(target=self.run_threaded_module, args=(text,module,))
                    mt.daemon = True
                    mt.start()
                    if direct:
                        Tiane.Serverconnection.send_buffer({'TIANE_context':[{'user':user, 'module':module.__name__, 'room':Tiane.room_name}]})
                    return True
            print('[ERROR] Das Modul {} konnte nicht gestartet werden!'.format(name))
        elif not text == None:
            # Ganz normal die Module abklingeln
            for module in self.modules:
                try:
                    if module.isValid(text):
                        Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user)
                        mt = Thread(target=self.run_threaded_module, args=(text,module,))
                        mt.daemon = True
                        mt.start()
                        if direct:
                            Tiane.Serverconnection.send_buffer({'TIANE_context':[{'user':user, 'module':module.__name__, 'room':Tiane.room_name}]})
                        return True
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} konnte nicht abgefragt werden!'.format(module.__name__))
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
            Tiane.Conversation.end(str(text))
            return

    def start_continuous(self):
        # Startet den Thread, in dem die continuous_modules ausgeführt werden (siehe unten).
        print('---- STARTE MODULE... ----')
        self.continuous_threads_running = 0
        if not self.continuous_modules == []:
            ct = Thread(target=self.run_continuous)
            ct.daemon = True
            ct.start()
            self.continuous_threads_running += 1
        else:
            print('[INFO] -- (Keine vorhanden)')
        return

    def run_continuous(self):
        # Führt die continuous_modules aus. Continuous_modules laufen immer im Hintergrund,
        # um auf andere Ereignisse als Sprachbefehle zu warten (z.B. Sensorwerte, Daten etc.).
        for module in self.continuous_modules:
            intervalltime = module.INTERVALL if hasattr(module, 'INTERVALL') else 0
            Tiane.continuous_modules[module.__name__] = self.Modulewrapper_continuous(intervalltime)
            try:
                module.start(Tiane.continuous_modules[module.__name__], Tiane.local_storage)
                print('[INFO] Modul {} gestartet'.format(module.__name__))
            except:
                pass
        Local_storage['module_counter'] = 0
        while True:
            for module in self.continuous_modules:
                # Continuous_modules können ein Zeitintervall definieren, in dem sie gerne
                # aufgerufen werden wollen, um Ressourcen zu sparen.
                if time.time() - Tiane.continuous_modules[module.__name__].last_call >= Tiane.continuous_modules[module.__name__].intervall_time:
                    Tiane.continuous_modules[module.__name__].last_call = time.time()
                    try:
                        module.run(Tiane.continuous_modules[module.__name__], Tiane.local_storage)
                        Tiane.continuous_modules[module.__name__].counter += 1
                    except:
                        traceback.print_exc()
                        print('[ERROR] Runtime-Error in Continuous-Module {}. Das Modul wird nicht mehr ausgeführt.\n'.format(module.__name__))
                        del Tiane.continuous_modules[module.__name__]
                        self.continuous_modules.remove(module)
            if self.continuous_stopped:
                break
            Local_storage['module_counter'] += 1
            time.sleep(0.01)
        self.continuous_threads_running -= 1

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
            for module in self.continuous_modules:
                try:
                    module.stop(Tiane.continuous_modules[module.__name__], Tiane.local_storage)
                    print('[INFO] Modul {} beendet'.format(module.__name__))
                    no_stopped_modules = False
                except:
                    pass
            # aufräumen
            Tiane.continuous_modules = {}
            if no_stopped_modules == True:
                print('[INFO] -- (Keine zu beenden)')
        return

class TIANE:
    def __init__(self):
        self.Serverconnection = Serverconnection
        self.Conversation = Conversation
        self.Modules = Modules
        self.Analyzer = Analyzer
        self.Audio_Input = Audioinput
        self.Audio_Output = Audiooutput

        self.active_modules = {}
        self.continuous_modules = {}

        self.local_storage = Local_storage
        self.room_name = room_name
        self.room_list = []
        self.server_name = ''
        self.users = []
        self.userlist = []

    def start(self):
        srt = Thread(target=self.handle_online_requests)
        srt.daemon = True
        srt.start()

    def handle_voice_call(self, text, user):
        self.Conversation.transform_blockage(text, user)
        # Immer erst mal den Server fragen, der fragt dann auch direkt den passenden Raum, falls nötig...
        try:
            response = Tiane.request_query_modules(user, text=text, direct=True)
        except ConnectionAbortedError:
            return
        if response == True:
            return
        # Ansonsten: Die eigenen Module durchgehen...
        response = self.Modules.query_threaded(user, None, text, direct=True)
        if response == False:
            Tiane.say(text, 'Das habe ich leider nicht verstanden.', Tiane.room_name, user)
            Tiane.Conversation.end(text)

    def handle_online_requests(self):
        say_requests = []
        listen_requests = []
        query_requests = []
        while True:
            # SAY
            # Neue Aufträge einholen
            new_say_requests = self.Serverconnection.readanddelete('TIANE_room_say')
            if new_say_requests is not None:
                for request in new_say_requests:
                    for existing_request in say_requests:
                        if request['original_command'] == existing_request['original_command']:
                            break
                    else:
                        say_requests.append(request)
            # Zu cancelnde Aufträge bearbeiten
            cancel_requests = self.Serverconnection.readanddelete('TIANE_room_cancel_say')
            if cancel_requests is not None:
                for request in cancel_requests:
                    for say_request in say_requests:
                        if request == say_request['original_command']:
                            say_requests.remove(say_request)
                            self.Serverconnection.send({'TIANE_room_confirms_cancel_say_{}'.format(request):True})
                            cancel_requests.remove(request)
                            break
                    else:
                        self.Serverconnection.send({'TIANE_room_confirms_cancel_say_{}'.format(request):False})
                        cancel_requests.remove(request)
            # Aufträge bearbeiten
            for request in say_requests:
                if self.Conversation.query(request['original_command']) == True:
                    self.Conversation.begin(request['original_command'], request['user'])
                    self.say(request['original_command'],request['text'],request['room'],request['user'])
                    self.Serverconnection.send({'TIANE_room_confirms_say_{}'.format(request['original_command']):True})
                    say_requests.remove(request)
                    break

            # LISTEN
            # Neue Aufträre einholen
            new_listen_requests = self.Serverconnection.readanddelete('TIANE_room_listen')
            if new_listen_requests is not None:
                for request in new_listen_requests:
                    for existing_request in listen_requests:
                        if request['original_command'] == existing_request['original_command']:
                            break
                    else:
                        listen_requests.append(request)
            # Zu cancelnde Aufträge bearbeiten
            cancel_requests = self.Serverconnection.readanddelete('TIANE_room_cancel_listen')
            if cancel_requests is not None:
                for request in cancel_requests:
                    for listen_request in listen_requests:
                        if request == listen_request['original_command']:
                            listen_requests.remove(listen_request)
                            self.Serverconnection.send({'TIANE_room_confirms_cancel_listen_{}'.format(request):True})
                            cancel_requests.remove(request)
                            break
                    else:
                        self.Serverconnection.send({'TIANE_room_confirms_cancel_listen_{}'.format(request):False})
                        cancel_requests.remove(request)
            # Aufträge bearbeiten
            for request in listen_requests:
                if self.Conversation.query(request['original_command']) == True:
                    self.Conversation.begin(request['original_command'], request['user'])
                    response = self.listen(request['original_command'], request['user'])
                    self.Serverconnection.send({'TIANE_room_confirms_listen_{}'.format(request['original_command']):response})
                    listen_requests.remove(request)
                    break

            # QUERY_MODULES
            # Neue Aufträge einholen
            new_query_requests = self.Serverconnection.readanddelete('TIANE_room_query_modules')
            if new_query_requests is not None:
                for request in new_query_requests:
                    for existing_request in query_requests:
                        if request['original_command'] == existing_request['original_command']:
                            break
                    else:
                        query_requests.append(request)
            # Aufträge bearbeiten
            for request in query_requests:
                response = self.Modules.query_threaded(request['user'], request['name'], request['text'], direct=request['direct'])
                self.Serverconnection.send({'TIANE_room_confirms_query_modules_{}'.format(request['original_command']):response})
                query_requests.remove(request)

            # END_CONVERSATION
            end_conversation_requests = self.Serverconnection.readanddelete('TIANE_room_end_Conversation')
            if end_conversation_requests is not None:
                for request in end_conversation_requests:
                    self.Conversation.end(request)

            # GET_UPDATE_INFORMATION
            information_dict = self.Serverconnection.readanddelete('TIANE_server_info')
            if information_dict is not None:
                self.get_update_information(information_dict)

            # RELOAD_MODULES
            request = self.Serverconnection.readanddelete('TIANE_reload_modules')
            if request is not None:
                if request == True:
                    print('\n\n--------- RELOAD ---------')
                    self.Modules.stop_continuous()
                    self.Modules.load_modules()
                    self.Modules.start_continuous()
                    self.Serverconnection.send({'TIANE_confirm_reload_modules':True})
                    time.sleep(1)
                    print('--------- FERTIG ---------\n\n')

            # Noch verbunden?
            if not self.Serverconnection.connected:
                break

            time.sleep(0.03)

    def request_say(self, original_command, text, raum, user):
        self.Serverconnection.send_buffer({'TIANE_server_say':[{'original_command':original_command,'text':text,'room':raum,'user':user}]})
        while not self.Serverconnection.readanddelete('TIANE_server_confirms_say_{}'.format(original_command)) == True:
            if not self.Serverconnection.connected:
                raise ConnectionAbortedError
            time.sleep(0.03)

    def request_listen(self, original_command, user):
        self.Serverconnection.send_buffer({'TIANE_server_listen':[{'original_command':original_command,'user':user}]})
        while True:
            response = self.Serverconnection.readanddelete('TIANE_server_confirms_listen_{}'.format(original_command))
            if response is not None:
                return response
            if not self.Serverconnection.connected:
                raise ConnectionAbortedError
            time.sleep(0.03)

    def request_query_modules(self, user, name=None, text=None, room=None, direct=False):
        if not text == None:
            original_command = text
        else:
            original_command = name
        self.Serverconnection.send_buffer({'TIANE_server_query_modules':[{'original_command':original_command, 'user':user, 'name':name, 'room':room, 'direct':direct}]})
        while True:
            response = self.Serverconnection.readanddelete('TIANE_server_confirms_query_modules_{}'.format(text))
            if response is not None:
                return response
            if not self.Serverconnection.connected:
                raise ConnectionAbortedError
            time.sleep(0.03)

    def request_end_Conversation(self, original_command):
        self.Serverconnection.send_buffer({'TIANE_server_end_Conversation':[original_command]})

    def get_update_information(self, information_dict):
        # Erst generell alle keys updaten...
        for key,value in information_dict.items():
            self.local_storage[key] = value

        # ...und dann noch um Spezialfälle kümmern
        room_list = []
        for room in self.local_storage['rooms'].keys():
            room_list.append(room)
        self.room_list = room_list
        self.Analyzer.room_list = self.room_list

        self.server_name = self.local_storage['server_name']

        userlist = []
        for user in self.local_storage['users'].keys():
            userlist.append(user)
        self.userlist = userlist
        self.Audio_Input.userlist = userlist

        self.users = self.local_storage['rooms'][self.room_name]['users']


    def start_module(self, user, name, text, room):
        if room == None or room == self.room_name:
            return self.Modules.query_threaded(user, name, text)
        else:
            return self.request_query_modules(user, name=name, text=text, room=room)

    def listen(self, original_command, user):
        self.Conversation.begin(original_command, user)
        return self.Audio_Input.listen()

    def say(self, original_command, text, room, user):
        self.Conversation.begin(original_command, user)
        print('\n--TIANE:-- {}'.format(text))
        self.Audio_Output.say(text)

class Modulewrapper:
    # Diese Klasse ist wichtig: Module bekommen sie anstelle einer "echten" Tiane-Instanz
    # vorgesetzt. Denn es gibt nur eine Tiane-Instanz, um von dort aus alles regeln zu
    # können, aber Module brauchen verschiedene Instanzen, die Informationen über sie ent-
    # halten müssen, z.B. welcher Nutzer das Modul aufgerufen hat. Diese Informationen
    # ergänzt diese Klasse und schleift ansonsten einfach alle von Modulen aus aufrufbaren
    # Funktionen an die Hauptinstanz von Tiane durch.
    def __init__(self, text, analysis, user):
        self.text = text # original_command
        self.analysis = analysis
        self.user = user

        self.core = Tiane
        self.Analyzer = Tiane.Analyzer
        self.serverconnection = Tiane.Serverconnection
        self.audio_Input = Tiane.Audio_Input
        self.audio_Output = Tiane.Audio_Input
        self.room_name = Tiane.room_name
        self.room_list = Tiane.room_list
        self.users = Tiane.users
        self.userlist = Tiane.userlist
        self.local_storage = Tiane.local_storage
        self.server_name = Tiane.server_name

    def say(self, text, room=None, user=None):
        if user == None:
            user = self.user
        if user == None: # Immer noch? Kann durchaus sein...
            room = self.room_name
        Tiane.request_say(self.text, text, room, user)

    def listen(self, user=None):
        if user == None:
            user = self.user
        text = Tiane.request_listen(self.text, user)
        return text

    def end_Conversation(self):
        Tiane.request_end_Conversation(self.text)

    def start_module(self, user=None, name=None, text=None, room=None):
        if user == None:
            user = self.user
        response = Tiane.start_module(user, name, text, room)

    def start_module_and_confirm(self, user=None, name=None, text=None, room=None):
        if user == None:
            user = self.user
        return Tiane.start_module(user, name, text, room)

class Modulewrapper_continuous:
    # Dieselbe Klasse für continuous_modules. Die Besonderheit: Die say- und listen-Funktionen
    # fehlen (also genau das, wofür der Modulewrapper eigentlich da war xD), weil continuous_-
    # modules ja nicht selbst nach außen telefonieren sollen. Dafür gibt es hier einen
    # Parameter für die Zeit zwischen zwei Aufrufen des Moduls.
    def __init__(self, intervalltime):
        self.intervall_time = intervalltime
        self.last_call = 0
        self.counter = 0

        self.core = Tiane
        self.Analyzer = Tiane.Analyzer
        self.serverconnection = Tiane.Serverconnection
        self.audio_Input = Tiane.Audio_Input
        self.audio_Output = Tiane.Audio_Input
        self.room_name = Tiane.room_name
        self.room_list = Tiane.room_list
        self.users = Tiane.users
        self.userlist = Tiane.userlist
        self.local_storage = Tiane.local_storage
        self.server_name = Tiane.server_name

    def start_module(self, user=None, name=None, text=None):
        response = Tiane.start_module(user, name, text)

    def start_module_and_confirm(self, user=None, name=None, text=None):
        return Tiane.start_module(user, name, text)

class Conversation:
    # Anders als man denken könnte, wird das hier nicht wie ein Objekt mehrmals initialisiert
    # - einfach aus dem Grund, dass es sich nicht lohnt: Es gibt in einem Raum nur eine Con-
    # versation, die kann man dann auch am besten in einer Instanz verwalten.
    def __init__(self):
        self.active = False
        self.blocked = False
        self.user = ''
        self.original_command = ''

    def query(self, original_command):
        if (self.active == False or self.original_command == original_command) and not self.blocked:
            return True
        else:
            return False

    def begin(self, original_command, user):
        # Das hier ist die Funktion, die Module tatsächlich
        # auf eine Conversation warten lässt...
        while not self.query(original_command) == True:
            time.sleep(2)
        self.active = True
        self.original_command = original_command
        self.user = user

    def transform_blockage(self, original_command, user):
        # Verwandelt eine Blockade in eine normale Konversation...
        # Darf deshalb unbedingt nur bei direktem Sprachkommando
        # intern verwendet werden, ansonsten gibt's Chaos!
        self.active = True
        self.original_command = original_command
        self.user = user
        self.blocked = False

    def end(self, original_command):
        if original_command == self.original_command:
            self.active = False
            self.user = ''
            self.original_command = ''

#################################################-MAIN-#################################################
#-----------Initialisieren-----------#
#------------------------------------------------------------------------------------------------------#
room_name = 'NAME_OF_ROOM_HERE'
SERVER_IP = 'IP.OF.TIANE.SERVER.HERE'
#------------------------------------------------------------------------------------------------------#
num_cameras = 0
speech = True

Local_storage = {}
Modules = Modules()
Local_storage['TIANE_modules_required_vocabulary'] = []
Analyzer = Sentence_Analyzer()
Serverconnection = TNetwork_Connection_Client()
Conversation = Conversation()
Audioinput = Audio_Input(Serverconnection, Local_storage)
Audiooutput = Audio_Output(Serverconnection, Local_storage, Audioinput)
Tiane = TIANE()

#-----------Daten mit dem Server austauschen-----------#
print('[INFO] Versuche mit Server auf {} zu verbinden...'.format(SERVER_IP))
Serverconnection.connect(SERVER_IP)

# Informationen über den Raum an den Server senden...
Serverconnection.send({'DEVICE_TYPE':'TIANE_ROOM'})
Serverconnection.send({'TIANE_room_info':{'name':room_name, 'num_cameras':num_cameras, 'speech':speech}})
# ...und auf Antwort warten, denn diese Informationen sind für den Betrieb wichtig.
# Sobald einmal vorhanden, werden sie per get_update_information aktuell gehalten.
while True:
    information_dict = Serverconnection.readanddelete('TIANE_server_info')
    if information_dict is not None:
        Tiane.get_update_information(information_dict)
        break
print('[INFO] Verbindung mit Server "{}" ({}) hergestellt'.format(Tiane.server_name, Serverconnection.ip))

#-----------Starten-----------#
Modules.start_continuous()
Audiooutput.start()
Tiane.start()
Audioinput.start_hotword_detection()
time.sleep(0.75)

time.sleep(1)
print('--------- FERTIG ---------')
for i in range (1,40):
    print('\n')


# Hauptschleife. Wartet auf Kommando, ermittelt den Nutzer, der es erteilt hat, und sucht das entsprechende Modul zum ausführen.
try:
    while True:
        if not Serverconnection.connected:
            raise ConnectionAbortedError
        if not Tiane.Conversation.active == True:
            if not Local_storage['TIANE_Hotword_detected'] == {}:
                Tiane.Conversation.blocked = True
                print('\n\nUser --{}-- detected'.format(Local_storage['TIANE_Hotword_detected']['user'].upper()))
                # Server knows best. Einfach den schon mal fragen, dann wissen wir gleich (wenn der Text vorliegt), wer da überhaupt spricht...
                Tiane.Serverconnection.send({'TIANE_user_voice_recognized':Local_storage['TIANE_Hotword_detected']['user']})
                while True:
                    # Warten auf Text (keine Sorge, es kommt auf jeden Fall welcher)
                    # und auf Antwort vom Server.
                    user = Tiane.Serverconnection.read('TIANE_user_server_guess')
                    text = Local_storage['TIANE_recognized_text']
                    if user is not None and not text == '':
                        user = Tiane.Serverconnection.readanddelete('TIANE_user_server_guess')
                        break
                    if not Serverconnection.connected:
                        raise ConnectionAbortedError
                    time.sleep(0.02)
                Local_storage['TIANE_recognized_text'] = ''
                print('\n--{}:-- {}\n'.format(user.upper(), text))
                Tiane.handle_voice_call(text, user)
                Local_storage['TIANE_Hotword_detected'] = {}
        time.sleep(0.03)
except ConnectionAbortedError:
    print('\n\n[ERROR] Verbindung zum Server unterbrochen!\n')
finally:
    Modules.stop_continuous()
    Audioinput.stop()
    Audiooutput.stop()
    Serverconnection.stop()
    print('\n[TIANE] Auf wiedersehen!\n')
