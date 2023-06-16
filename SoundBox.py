import os
import tempfile
import langid
import subprocess
from gtts import gTTS
from Player import AudioPlayer


class SoundBox:
    # Kelas ini akan mengubah teks menjadi suara
    def __init__(self, text):
        self.play_audio = AudioPlayer
        # Mengatur bahasa objek gTTS
        bahasa = self.langid_voice(text)

        # Render tekst ke dalam file MP3
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3_file:
            tts = gTTS(text, lang=bahasa)
            tts.save(mp3_file.name)
            mp3_filename = mp3_file.name

        # Memutar audio WAV
        self.play_audio(mp3_filename).play()

        # Menghapus temporary file
        os.remove(mp3_filename)

    def langid_voice(self, text):
        # Mengidentifikasi bahasa
        lang, confidence = langid.classify(text)
        return lang
    

class PlaySong:
    # Kelas ini akan memutar lagu
    def __init__(self):
        self.player = None

    def play(self, song):
        if self.player is not None:
            self.stop()
        command = ["python", "Player.py", song]
        self.player = subprocess.Popen(command)
    
    def stop(self):
        if self.player is not None and self.player.poll() is None:
            self.player.terminate()
            self.player.wait()