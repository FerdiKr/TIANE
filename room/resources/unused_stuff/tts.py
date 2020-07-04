from resources.picotts import PicoTTS
import audioop
import pyaudio
import wave
import io

DOWNSAMPLE_TO = 16000
class Text_to_Speech:
    def __init__(self, rate, voice):
        self.chunk = 1024
        self.rate = rate
        self.voice = voice
        self.tts = PicoTTS(voice=self.voice)

    def synth_wav(self, text):
        wavs = self.tts.synth_wav(text)
        temp_file_19 = io.BytesIO()
        # Audio in eine neue Datei schreiben, die einfach als self.rate definiert wurde:
        with wave.open(io.BytesIO(wavs), 'rb') as readfile:
            with wave.open(temp_file_19, 'wb') as writefile:
                writefile.setnchannels(1)
                writefile.setsampwidth(2)
                writefile.setframerate(self.rate)
                wav_data = readfile.readframes(1024)
                while wav_data != b'':
                    writefile.writeframesraw(wav_data)
                    wav_data = readfile.readframes(1024)
        temp_file_19.seek(0)
        down_file_16 = 'temp16.wav'
        # Die temporäre Datei wird dann wieder auf 16kHz gedownsampled
        with wave.open(temp_file_19, 'rb') as readfile:
            with wave.open(down_file_16, 'wb') as writefile:
                wav_data = readfile.readframes(readfile.getnframes())
                writefile.setnchannels(1)
                writefile.setsampwidth(2)
                writefile.setframerate(DOWNSAMPLE_TO)
                writefile.writeframesraw(audioop.ratecv(wav_data, 2, 1, self.rate, 16000, None)[0])
        #down_file_16.seek(0)
        return wave.open(down_file_16, 'rb')

    def say(self, text):
        # Diese Funktion kann durch eine beliebige Sprachsynthesefunktion ersetzt werden, die Text annimmt und einen
        # audio-buffer ausgibt (und "notification_audio_format" entsprechend anpasst)(siehe Beispiel).
        # Denkbar wäre z.B. espeak oder google cloud text-to-speech.
        if not text == '':
            wav = self.synth_wav(text)
            format = {'format': 8,
                      'channels':1,
                      'rate':16000,
                      'chunk':self.chunk}
            wav_data = wav.readframes(self.chunk)
            audio_buffer = []
            while wav_data:
                audio_buffer.append(wav_data)
                wav_data = wav.readframes(self.chunk)
            audio_buffer.append('Endederdurchsage')
            return format, audio_buffer
