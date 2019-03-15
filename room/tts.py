from resources.picotts import PicoTTS
import pyaudio
import wave
import io

class Text_to_Speech:
    def __init__(self, rate, voice):
        self.chunk = 1024
        self.rate = rate
        self.voice = voice

    def synth_wav(self, text):
        tts = PicoTTS(voice=self.voice)
        wavs = tts.synth_wav(text)
        wav = wave.open(io.BytesIO(wavs))
        return wav

    def say(self, text):
        # Diese Funktion kann durch eine beliebige Sprachsynthesefunktion ersetzt werden, die Text annimmt und einen
        # audio-buffer ausgibt (und "notification_audio_format" entsprechend anpasst)(siehe Beispiel).
        # Denkbar wäre z.B. espeak oder google cloud text-to-speech.
        if not text == '':
            wav = self.synth_wav(text)
            format = {'format': 8,
                      'channels':1,
                      'rate':self.rate,
                      'chunk':self.chunk}
            wav_data = wav.readframes(self.chunk)
            audio_buffer = []
            while wav_data:
                audio_buffer.append(wav_data)
                wav_data = wav.readframes(self.chunk)
            audio_buffer.append('Endederdurchsage')
            return format, audio_buffer
