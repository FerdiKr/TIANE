from resources.snowboy import snowboydecoder
from stt import Speech_to_Text
from tts import Text_to_Speech
from threading import Thread
import speech_recognition as sr

import pyaudio
import wave
import time
import sys
import os
import io

class HWobject:
    def __init__(self, file, user, local_storage):
        self.file = file
        self.user = user
        self.local_storage = local_storage

    def handle(self):
        self.local_storage['TIANE_Hotword_detected'] = {'file':self.file, 'user':self.user}
        self.bling_callback()

    def bling_callback(self):
        snowboydecoder.play_audio_file()
        sys.stdout.write("\nlistening...")
        sys.stdout.flush()

class Audio_Input:
    def __init__(self, serverconnection, local_storage):
        self.Serverconnection = serverconnection
        self.local_storage = local_storage
        self.userlist = []
        self.detector = None
        self.stt = Speech_to_Text(self.local_storage['TIANE_Modules_defined_Vocabulary'])
        self.hotword_models_and_names = []
        self.stopped = False
        self.hwobjects = []

    def start_hotword_detection(self, sensitivity=0.5, audio_gain=1):
        self.stopped = False
        self.local_storage['TIANE_Hotword_detected'] = {}
        self.local_storage['TIANE_recognized_text'] = ''
        # Alle gegebenen Hotword-Detection-Modelle finden und - falls zutreffend -
        # zusammen mit dem dazugehörigen Nutzernamen speichern.
        dirname = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(dirname, 'hotword_models')
        for file in os.listdir(directory):
            if file.endswith('.pmdl'):
                for user in self.userlist:
                    if user.lower() in file.lower():
                        self.hotword_models_and_names.append((os.path.join(directory, file), user))
                        break
                else:
                    self.hotword_models_and_names.append((os.path.join(directory, file), 'Unknown'))
            elif file.endswith('.umdl'):
                self.hotword_models_and_names.append((os.path.join(directory, file), 'Unknown'))

        models = []
        callbacks = []
        for file, user in self.hotword_models_and_names:
            models.append(file)
            self.hwobjects.append(HWobject(file, user, self.local_storage))
            for hobject in self.hwobjects:
                if hobject.file == file:
                    callbacks.append(hobject.handle)

########### Die folgenden zwei Werte beeinflussen die Hotworderkennung erheblich; wenn sie unzuverlässig funktioniert, lohnt es sich, mit diesen Werten zu experimentieren! ###
        sensitivity = sensitivity*len(models)
        audio_gain = audio_gain
###############################################################################################################################################################################

        snsrt = Thread(target=self.run_hotword_detection, args=(models, callbacks, sensitivity, audio_gain,))
        snsrt.daemon = True
        snsrt.start()

    def run_hotword_detection(self, models, callbacks, sensitivity, audio_gain):
        self.detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity, audio_gain=audio_gain)

        # main loop
        self.detector.start(detected_callback=callbacks,
                           audio_recorder_callback=self.audioRecorderCallback,
                           interrupt_check=self.interrupt_callback,
                           sleep_time=0.01)

        self.detector.terminate()

    def audioRecorderCallback(self, fname):
        print(" converting audio to text...")
        text = self.stt.recognize(fname)
        self.local_storage['TIANE_recognized_text'] = text
        os.remove(fname)

    def listen(self):
        # Diese Funktion sieht sehr einfach aus, ist in ihrer Funktionsweise aber doch recht tricky:
        # Da snowboy den PyAudio-input-stream fest in der Hand hat und nicht mit vertretbarem Aufwand
        # hergibt, benutze ich einfach direkt snowboy, um Antworten einzufangen. Dafür ist meine leicht
        # modifizierte Version von snowboydecoder.py erforderlich, die nämlich eine Variable "activated"
        # hinzufügt. Ist dieser Wert auf True gesetzt, geht snowboy in den Zuhören-Modus, als wäre ein
        # Hotword gesagt worden, nimmt so lange Ton auf, wie es Sprache feststellen kann, und ruft direkt
        # audioRecorderCallback mit dieser Tondatei auf, ich muss also hier nur warten und den fertig
        # übersetzten Text abholen :)
        self.bling_callback()
        self.detector.activated = True
        while self.local_storage['TIANE_recognized_text'] == '':
            time.sleep(0.01)
        text = self.local_storage['TIANE_recognized_text']
        self.local_storage['TIANE_recognized_text'] = ''
        print('\n- {}\n'.format(text))
        return text

    def bling_callback(self):
        snowboydecoder.play_audio_file()
        sys.stdout.write("\nlistening...")
        sys.stdout.flush()

    def interrupt_callback(self):
        return self.stopped

    def stop(self):
        self.stopped = True

class Audio_Output:
    # Verwaltet sämtliche Audio-Output-Streams des Clients, also z.B. Musik und
    # Benachrichtigungen, mit zwei verschiedenen Prioritätsstufen. Ein Stream
    # aus dem Puffer mit niedriger Priorität ('playback_audio_buffer') wird sofort
    # unterbrochen, sobald ein der Puffer für hohe Priorität ('notification_audio_buffer')
    # gefüllt wird, und erst nach Ende dieses wichtigen Streams fortgesetzt.
    def __init__(self, serverconnection, local_storage, Audio_Input):
        self.Serverconnection = serverconnection
        self.local_storage = local_storage
        self.audioinput = Audio_Input
        self.playback_audio_buffer = []
        self.notification_audio_buffer = []
        self.playback_audio_format = {}
        self.notification_audio_format = {}
        self.audio = pyaudio.PyAudio()
        self.tts = Text_to_Speech(19000, 'de-DE')
        self.stopped = False

    def start(self):
        ot = Thread(target=self.putout)
        ot.daemon = True
        ot.start()
        return self

    def putout(self):
        while True:
            # Wenn Musik gestreamt wird, diese Musik wiedergeben...
            if not self.playback_audio_buffer == []:
                stream = self.audio.open(format=self.playback_audio_format['format'],
                                         channels=self.playback_audio_format['channels'],
                                         rate=self.playback_audio_format['rate'],
                                         output=True,
                                         frames_per_buffer=self.playback_audio_format['chunk'])
                for data in self.playback_audio_buffer:
                    if not data == 'Endederdurchsage':
                        stream.write(data)
                    else:
                        # ...es sei denn, sie ist zuende, dann wird aufgeräumt...
                        stream.stop_stream()
                        stream.close()
                        self.playback_audio_buffer = []
                        break

                    # ...oder eine Benachrichtigung oder sonstiger "wichtigerer" Ton dazwischen kommt,
                    # dann wird die Wiedergabe unterbrochen und auf diese neuen Daten umgestellt
                    if not self.notification_audio_buffer == []:
                        stream.stop_stream()
                        stream.close()
                        stream = self.audio.open(format=self.notification_audio_format['format'],
                                                 channels=self.notification_audio_format['channels'],
                                                 rate=self.notification_audio_format['rate'],
                                                 output=True,
                                                 frames_per_buffer=self.notification_audio_format['chunk'])
                        for data in self.notification_audio_buffer:
                            if not data == 'Endederdurchsage':
                                stream.write(data)
                            else:
                                stream.stop_stream()
                                stream.close()
                                self.notification_audio_buffer = []
                                break
                        # Nach Ende dieser unterbrechenden Durchsage wird natürlich wieder auf die
                        # normale Audiowiedergabe umgestellt.
                        stream = self.audio.open(format=self.playback_audio_format['format'],
                                                 channels=self.playback_audio_format['channels'],
                                                 rate=self.playback_audio_format['rate'],
                                                 output=True,
                                                 frames_per_buffer=self.playback_audio_format['chunk'])
                        self.notification_audio_buffer = []
            # Es kann natürlich auch sein, dass eine Benachrichtigung kommt, ohne dass zuvor Musik
            # gespielt wird, in dem Fall wird einfach nur diese Benachrichtigung wiedergegeben.
            elif not self.notification_audio_buffer == []:
                stream = self.audio.open(format=self.notification_audio_format['format'],
                                         channels=self.notification_audio_format['channels'],
                                         rate=self.notification_audio_format['rate'],
                                         output=True,
                                         frames_per_buffer=self.notification_audio_format['chunk'])
                for data in self.notification_audio_buffer:
                    if not data == 'Endederdurchsage':
                        stream.write(data)
                    else:
                        stream.stop_stream()
                        stream.close()
                        self.notification_audio_buffer = []
                        break
            # Im Realbetrieb wird natürlich die allermeiste Zeit gar nichts anliegen,
            # deshalb macht das Folgende Sinn:
            else:
                time.sleep(0.2)
            if self.stopped:
                stream.stop_stream()
                stream.close()
                break

    def say(self, text):
        # Gibt den gegebenen Text an die Text-to-Speech-Funktion weiter und wartet,
        # bis die Durchsage beendet ist.
        self.audioinput.detector.stopped = True # Kleiner Hack: Diese supercoole Zeile sorgt dafür, dass die Hotworderkennung nicht mithört xD
        if text == '' or text == None:
            text = 'Das sollte nicht passieren. Eines meiner internen Module antwortet nicht mehr.'
        format, buffer = self.tts.say(str(text))
        self.notification_audio_format = format
        self.notification_audio_buffer = buffer
        time.sleep(0.1)
        while not self.notification_audio_buffer == []:
            time.sleep(0.1)
        self.audioinput.detector.stopped = False

    def play(self, data):
        # Spielt gegebene wave-Audio-Stream-Daten ab
        for x in data:
            self.playback_audio_buffer.append(x)

    def priority_play(self, data):
        # Im Grunde genommen das selbe wie play(), mit dem Unterschied, dass es den "Prioritäts"-Stream
        # benutzt: Hiermit abgespielter Ton unterbricht notfalls laufende low-priority-streams. Kann
        # aber Probleme im Zusammenhang mit der Sprachausgabe (die auch diesen high-priority-stream nutzt)
        # verursachen, daher nur verwenden, wenn du weißt, was du tust ;)
        for x in data:
            self.notification_audio_buffer.append(x)

    def set_format(self, format_dict):
        self.playback_audio_format = format_dict

    def stop(self):
        self.stopped = True
