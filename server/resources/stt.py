import wave
import pyaudio
import speech_recognition as sr
import os

class Speech_to_Text:
    def __init__(self, vocabulary_list):
        self.vocabulary_list = vocabulary_list # Enthält eine Liste aller Wörter, die in den WORDS-Listen von Modulen vorkommen, die also unter Umständen verstanden werden müssen
        self.recognizer = sr.Recognizer()

    def recognize(self, audio_file_path):
        # Diese Funktion kann durch eine beliebige Spracherkennungsfunktion ersetzt werden, die eine Audiodatei annimmt und den erkannten
        # Text ausgibt. Die library speech_recognition bietet dafür übrigens noch einige andere gute Beispiele :)
        with sr.AudioFile(audio_file_path) as source:
            audio = self.recognizer.record(source)  # read the entire audio file
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `self.recognizer.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `self.recognizer.recognize_google(audio)`
            text = self.recognizer.recognize_google(audio,language='de-DE')
        except sr.UnknownValueError:
            text = "TIMEOUT_OR_INVALID"
        except sr.RequestError as e:
            text = "TIMEOUT_OR_INVALID"
        except:
            text = "TIMEOUT_OR_INVALID"
        return text
