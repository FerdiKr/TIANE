from resources.picotts import PicoTTS
import pyaudio
import wave
import io
import requests

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

    def synth_mary(self, text):
        params = (
            ('INPUT_TYPE', 'TEXT'),
            ('OUTPUT_TYPE', 'AUDIO'),
            ('INPUT_TEXT', text),
            ('VOICE_SELECTIONS', 'bits1-hsmm de female hmm'),
            ('AUDIO_OUT', 'WAVE_FILE'),
            ('LOCALE', 'de'),
            ('VOICE', 'bits1-hsmm'),
            ('AUDIO', 'WAVE_FILE'),
        )
        response = requests.get('https://iot.foobar.rocks/mary/process', params=params, stream=True)
        wav = wave.open(io.BytesIO(response.raw.read()))
        return wav

    def say(self, text):
        # Diese Funktion kann durch eine beliebige Sprachsynthesefunktion ersetzt werden, die Text annimmt und einen
        # audio-buffer ausgibt (und "notification_audio_format" entsprechend anpasst)(siehe Beispiel).
        # Denkbar wäre z.B. espeak oder google cloud text-to-speech.
        if not text == '':
            wav = self.synth_wav(text)
            # wav = self.synth_mary(text)
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
