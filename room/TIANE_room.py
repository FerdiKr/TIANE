from TNetwork import TNetwork_Connection_Client
from TIANE_Audio import Audio_Output
from TIANE_Audio import Audio_Input
from analyze import Sentence_Analyzer
from threading import Thread
import resources.snowboy.snowboydecoder
import traceback
import pkgutil
import random
import base64
import json
import time
import sys
import os
from urllib.request import urlopen, Request
import urllib.parse


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
        print('------ ROOM_MODULES ------')
        self.modules = self.get_modules('modules')
        if self.modules == []:
            print('[INFO] -- (Keine vorhanden)')
        print('------ CONTINUOUS')
        self.continuous_modules = self.get_modules('modules/continuous',continuous=True)
        if self.continuous_modules == []:
            print('[INFO] -- (Keine vorhanden)')
        Local_storage['TIANE_room_Modules_defined_Vocabulary'] = self.modules_defined_vocabulary
        try:
            for word in Local_storage['TIANE_room_Modules_defined_Vocabulary']:
                if not word in Local_storage['TIANE_Modules_defined_Vocabulary']:
                    Local_storage['TIANE_Modules_defined_Vocabulary'].append(word)
        except KeyError:
            Local_storage['TIANE_Modules_defined_Vocabulary'] = Local_storage['TIANE_room_Modules_defined_Vocabulary'].copy()

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
                continue
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


    def query_threaded(self, user, name, text, direct=False, origin_room=None, data=None): # direct: Es handelt sich um einen direkten Sprachaufruf des Moduls. Etwas unintuitiv, da ich manchmal auch
                                                                                           # von einem Direktaufruf spreche, wenn das Modul "gezielt", also direkt, über start_module aufgerufen wird...
                                                                                           # origin_room ist hauptsächlich dafür da, dass es "Telegram" sein kann, damit Module wissen, wie sie zu antworten haben
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
                    Tiane.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--Modul {} ({}) direkt aufgerufen (Parameter: {})--'.format(module.__name__, Tiane.room_name, text), 'info':None, 'conv_id':str(text), 'show':True}]})
                    Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
                    mt = Thread(target=self.run_threaded_module, args=(text,module,))
                    mt.daemon = True
                    mt.start()
                    if direct:
                        Tiane.Serverconnection.send_buffer({'TIANE_context':[{'user':user, 'module':module.__name__, 'room':Tiane.room_name}]})
                    return True
            print('[ERROR] Das Modul {} konnte nicht gefunden werden!'.format(name))
        elif not text == None:
            # Ganz normal die Module abklingeln
            # Bei Telegram-Aufrufen zuerst die entsprechenden telegram_isValids abklappern:
            if origin_room == 'Telegram':
                for module in self.modules:
                    try:
                        if module.telegram_isValid(data):
                            Tiane.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--Modul {} ({}) via telegram_isValid gestartet--'.format(module.__name__, Tiane.room_name), 'info':None, 'conv_id':str(text), 'show':True}]})
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
            for module in self.modules:
                try:
                    if module.isValid(text):
                        Tiane.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--Modul {} ({}) gestartet--'.format(module.__name__, Tiane.room_name), 'info':None, 'conv_id':str(text), 'show':True}]})
                        Tiane.active_modules[str(text)] = self.Modulewrapper(text, analysis, user, origin_room, data)
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
            Tiane.request_end_Conversation(str(text))
            Tiane.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--Modul {} ({}) beendet--'.format(module.__name__, Tiane.room_name), 'info':None, 'conv_id':str(text), 'show':True}]})
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
                    continue
            # aufräumen
            Tiane.continuous_modules = {}
            if no_stopped_modules == True:
                print('[INFO] -- (Keine zu beenden)')
        return

class Users:
    def __init__(self):
        self.userlist = []
        self.userdict = {}


class TIANE:
    def __init__(self):
        self.Serverconnection = Serverconnection
        self.Conversation = Conversation
        self.Modules = Modules
        self.Users = Users
        self.Analyzer = Analyzer
        self.Audio_Input = Audioinput
        self.Audio_Output = Audiooutput

        self.active_modules = {}
        self.continuous_modules = {}

        self.local_storage = Local_storage
        self.room_name = room_name
        self.room_list = []
        self.server_name = ''
        self.system_name = ''
        self.users = []
        self.userlist = []
        self.path = Local_storage['TIANE_PATH']

    def start(self):
        srt = Thread(target=self.handle_online_requests)
        srt.daemon = True
        srt.start()
        
    def hotword_detected(self):
        # Der Name wurde bewusst mit Hinsicht auf weitere Reaktionen (wie z.B. Leuchten, etc.) gewählt

        # playing Bling-Sound
        TOP_DIR = os.path.dirname(os.path.abspath(__file__))
        DETECT_DING = os.path.join(TOP_DIR, "resources/snowboy/resources/ding.wav")
        DETECT_DONG = os.path.join(TOP_DIR, "resources/snowboy/resources/dong.wav")

        audiofile = wave.open(DETECT_DONG, 'rb')
        chunk = 1024
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
        self.Audio_Output.notification_audio_format = format
        self.Audio_Output.priority_play(audio_buffer)
        
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
        play_requests = []
        query_requests = []
        while True:
            # SAY
            # Neue Aufträge einholen
            new_say_requests = self.Serverconnection.readanddelete('TIANE_room_say')
            if new_say_requests is not None:
                for request in new_say_requests:
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
                    
            # PLAY
            # Neue Aufträge einholen
            new_play_requests = self.Serverconnection.readanddelete('Tiane_room_play')
            if new_play_requests is not None:
                for request in new_play_requests:
                    play_requests.append(request)
            # Zu cancelnde Aufträge bearbeiten
            cancel_requests = self.Serverconnection.readanddelete('Tiane_room_cancel_play')
            if cancel_requests is not None:
                for request in cancel_requests:
                    for play_request in play_requests:
                        if request == play_request['original_command']:
                            play_requests.remove(play_request)
                            self.Serverconnection.send({'Tiane_room_confirms_cancel_play_{}'.format(request): True})
                            cancel_requests.remove(request)
                    else:
                        self.Serverconnection.send({'Tiane_room_confirms_cancel_play_{}'.format(request): False})
                        cancel_requests.remove(request)
            # Aufträge bearbeiten
            for request in play_requests:
                if self.Conversation.query(request['original_command']) == True:
                    self.play(request['original_command'], request['audiofile'], request['room'], request['user'])
                    self.Serverconnection.send({'Tiane_room_confirms_play_{}'.format(request['original_command']): True})
                    play_requests.remove(request)

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
                response = self.Modules.query_threaded(request['user'], request['name'], request['text'], direct=request['direct'], origin_room=request['origin_room'], data=request['data'])
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

    def request_say(self, original_command, text, raum, user, output):
        self.Serverconnection.send_buffer({'TIANE_server_say':[{'original_command':original_command,'text':text,'room':raum,'user':user,'output':output}]})
        while not self.Serverconnection.readanddelete('TIANE_server_confirms_say_{}'.format(original_command)) == True:
            if not self.Serverconnection.connected:
                raise ConnectionAbortedError
            time.sleep(0.03)
            
    def request_play(self, original_command, audiofile, raum, user, output):
        self.Serverconnection.send_buffer({'Tiane_server_play': [
            {'original_command': original_command, 'audiofile': audiofile, 'room': raum, 'user': user,
             'output': output}]})
        while not self.Serverconnection.readanddelete('Tiane_server_confirms_play_{}'.format(original_command)) == True:
            if not self.Serverconnection.connected:
                raise ConnectionAbortedError
            time.sleep(0.03)
            
    def request_listen(self, original_command, user, telegram=False):
        self.Serverconnection.send_buffer({'TIANE_server_listen':[{'original_command':original_command,'user':user,'telegram':telegram}]})
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
        if 'rooms' in information_dict.keys():
            room_list = []
            for room in self.local_storage['rooms'].keys():
                room_list.append(room)
            self.room_list = room_list
            self.Analyzer.room_list = self.room_list

            self.users = self.local_storage['rooms'][self.room_name]['users']

        if 'server_name' in information_dict.keys():
            self.server_name = self.local_storage['server_name']

        if 'system_name' in information_dict.keys():
            self.system_name = self.local_storage['system_name']

        if 'users' in information_dict.keys():
            userlist = []
            for user in self.local_storage['users'].keys():
                userlist.append(user)
            self.userlist = userlist
            self.Users.userlist = userlist
            self.Users.userdict = self.local_storage['users']
            self.Audio_Input.userlist = userlist

        if 'TIANE_Modules_defined_Vocabulary' in information_dict.keys():
            for word in self.local_storage['TIANE_room_Modules_defined_Vocabulary']:
                if not word in self.local_storage['TIANE_Modules_defined_Vocabulary']:
                    self.local_storage['TIANE_Modules_defined_Vocabulary'].append(word)


    def start_module(self, user, name, text, room):
        if room == None or room == self.room_name:
            return self.Modules.query_threaded(user, name, text)
        else:
            return self.request_query_modules(user, name=name, text=text, room=room)

    def listen(self, original_command, user):
        self.Conversation.begin(original_command, user)
        self.Audio_Input.detector.stopped = False
        self.Audio_Input.bling_callback()
        self.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--listening to {} (room: {})--'.format(user,self.room_name), 'info':None, 'conv_id':original_command, 'show':True}]})
        response = self.Audio_Input.listen()
        self.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--{}-- ({}): {}'.format(user.upper(),self.room_name,response), 'info':None, 'conv_id':original_command, 'show':True}]})
        return response

    def say(self, original_command, text, room, user):
        self.Conversation.begin(original_command, user)
        print('\n--{}:-- {}'.format(self.system_name.upper(),text))
        self.Serverconnection.send_buffer({'TIANE_LOG':[{'type':'ACTION','content':'--{}--@{} ({}): {}'.format(self.system_name.upper(),user,self.room_name,text), 'info':None, 'conv_id':original_command, 'show':True}]})
        self.Audio_Output.say(text)

    def play(self, original_command, audiofile, room, user):
        self.Serverconnection.send_buffer({'Tiane_LOG': [{'type': 'ACTION', 'content': '--{}--@{} ({}): {}'.format(
            self.system_name.upper(), user, self.room_name, text), 'info': None, 'conv_id': original_command,
                                                         'show': True}]})
        self.Audio_Output.playback_audio_format = audiofile["format"]
        self.Audio_Output.play(audiofile["buffer"])

        
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
        self.room = origin_room # !!!

        self.telegram_data = data
        self.telegram_call = True if data is not None else False

        self.core = Tiane
        self.Analyzer = Tiane.Analyzer
        self.serverconnection = Tiane.Serverconnection
        self.audio_Input = Tiane.Audio_Input
        self.audio_Output = Tiane.Audio_Output
        self.room_name = Tiane.room_name
        self.room_list = Tiane.room_list
        self.users = Tiane.users
        self.Users = Tiane.Users
        self.userlist = Tiane.Users.userlist
        self.local_storage = Tiane.local_storage
        self.server_name = Tiane.server_name
        self.system_name = Tiane.system_name
        self.path = Tiane.path

    def say(self, text, room=None, user=None, output='auto'):
        if user == None or user == 'Unknown':
            user = self.user
        if user == None or user == 'Unknown': # Immer noch? Kann durchaus sein...
            room = self.room_name
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
        Tiane.request_say(self.text, text, room, user, output)
    
    def play(self, audiofile, room=None, user=None):
        #ToDo: Audio soll an Server geschickt werden und dann von diesem abgearbeitet werden
        self.Audio_Output.play(audiofile)
    
    def listen(self, user=None, input='auto'):
        if user == None or user == 'Unknown':
            user = self.user
        if input == 'telegram' or (input == 'auto' and self.room == 'Telegram'):
            response = Tiane.request_listen(self.text, user, telegram=True)
            text = response['text']
        else:
            text = Tiane.request_listen(self.text, user)
        return text

    def asynchronous_say(self, text, room=None, user=None, output='auto'):
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
        st = Thread(target=Tiane.request_say, args=(self.text, text, room, user, output))
        st.daemon = True
        st.start()

    def telegram_listen(self, user=None):
        if user == None or user == 'Unknown':
            user = self.user
        response = Tiane.request_listen(self.text, user, telegram=True)
        return response

    def end_Conversation(self):
        Tiane.request_end_Conversation(self.text)

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
    def __init__(self, intervalltime):
        self.intervall_time = intervalltime
        self.last_call = 0
        self.counter = 0

        self.core = Tiane
        self.Analyzer = Tiane.Analyzer
        self.serverconnection = Tiane.Serverconnection
        self.audio_Input = Tiane.Audio_Input
        self.audio_Output = Tiane.Audio_Output
        self.room_name = Tiane.room_name
        self.room_list = Tiane.room_list
        self.users = Tiane.users
        self.Users = Tiane.Users
        self.userlist = Tiane.Users.userlist
        self.local_storage = Tiane.local_storage
        self.server_name = Tiane.server_name
        self.system_name = Tiane.system_name
        self.path = Tiane.path

    def start_module(self, user=None, name=None, text=None):
        response = Tiane.start_module(user, name, text)

    def start_module_and_confirm(self, user=None, name=None, text=None):
        return Tiane.start_module(user, name, text)

    def translate(self, ttext, targetLang='de'):
        return Tiane.translate(ttext, targetLang)

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
        Tiane.Audio_Input.detector.stopped = True
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
            Tiane.Audio_Input.detector.stopped = False


#################################################-MAIN-#################################################

# aus TIANE_config.json laden
with open('TIANE_config.json', 'r') as config_file:
    config_data = json.load(config_file)

room_name = config_data['Room_name']
server_ip = config_data['Server_IP']
Local_storage = config_data['Local_storage']
Hotword_sensitivity = config_data['Hotword_sensitivity']
Hotword_Audio_gain = config_data['Hotword_Audio_gain']
TNetwork_Key = base64.b64decode(config_data['TNetwork_Key'].encode('utf-8')) # sehr umständliche Decoder-Zeile. Leider nötig :(
dirname = os.path.dirname(os.path.abspath(__file__))
Local_storage['TIANE_PATH'] = dirname

Users = Users()
Modules = Modules()
Analyzer = Sentence_Analyzer()
Serverconnection = TNetwork_Connection_Client()
Serverconnection.key = TNetwork_Key
Conversation = Conversation()

Local_storage['TIANE_Modules_defined_Vocabulary'] = Local_storage['TIANE_room_Modules_defined_Vocabulary'].copy()
Audioinput = Audio_Input(Serverconnection, Local_storage)
Audiooutput = Audio_Output(Serverconnection, Local_storage, Audioinput)
Tiane = TIANE()

#-----------Daten mit dem Server austauschen-----------#
print('[INFO] Versuche mit Server auf {} zu verbinden...'.format(server_ip))
Serverconnection.connect(server_ip)

# Informationen über den Raum an den Server senden...
Serverconnection.send({'DEVICE_TYPE':'TIANE_ROOM'})
Serverconnection.send({'TIANE_room_info':{'name':room_name}})
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
Audioinput.start_hotword_detection(sensitivity=Hotword_sensitivity, audio_gain=Hotword_Audio_gain)
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
                # Wir haben noch keine wirkliche Konversation, aber wir blockieren sie schon mal
                Tiane.Conversation.blocked = True
                Tiane.hotword_detected()
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
    print('\n[{}] Auf wiedersehen!\n'.format(Tiane.system_name.upper()))
