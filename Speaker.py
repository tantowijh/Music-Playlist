import os
import tempfile
import langid
from gtts import gTTS
import soundfile as sf
import sounddevice as sd

class Speak:
    def __init__(self, text):
        self.play_audio = self.play_audio_sounddevice
        # Set up gTTS object with language
        bahasa = self.langid_voice(text)

        # Generate the speech and save as an MP3 file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3_file:
            tts = gTTS(text, lang=bahasa)
            tts.save(mp3_file.name)
            mp3_filename = mp3_file.name

        # Convert the MP3 audio to WAV format
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
            self.convert_to_wav(mp3_filename, wav_file.name)
            wav_filename = wav_file.name

        # Play the audio file using sounddevice
        self.play_audio(wav_filename)

        # Clean up the temporary files
        os.remove(mp3_filename)
        os.remove(wav_filename)

    def langid_voice(self, text):
        lang, confidence = langid.classify(text)
        return lang

    def convert_to_wav(self, input_file, output_file):
        data, sample_rate = sf.read(input_file)
        sf.write(output_file, data, sample_rate)

    def play_audio_sounddevice(self, audio_file):
        data, sample_rate = sf.read(audio_file)
        sd.play(data, sample_rate)
        sd.wait()
