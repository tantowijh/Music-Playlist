import os
import langid
from gtts import gTTS
import platform

# Inisialisasi class untuk memainkan audio
class speak:
    # Inisialisasi pemanggil suara
    def __init__(self, text):
        self.audio_setup()
        # Mengatur object gTTS dengan bahasa dan tld
        bahasa = self.langid_voice(text)
        tts = gTTS(text, lang=bahasa)
        # Menyimpan file audio
        tts.save("output.mp3")
        # Memainkan file audio menggunakan perintah yang sesuai untuk sistem operasi saat ini
        if platform.system() == "Windows":
            os.system("start output.mp3")
        elif platform.system() == "Darwin":
            os.system("afplay output.mp3")
        else:
            if self.audio_setup():
                os.system("mpg123 output.mp3")

    # Inisiaisasi setup audio player untuk sistem operasi yang digunakan
    def audio_setup(self):
        # mengecek mpg123 sudah terinstall atau belum, jika belum maka akan menginstallnya
        if platform.system() in ["Linux", "FreeBSD", "OpenBSD", "NetBSD", "Solaris"]:
            if os.system("which mpg123 >/dev/null 2>&1") != 0:
                """mpg123 tidak terinstall maka menginstall sekarang..."""
                if platform.system() in ["Linux", "FreeBSD", "OpenBSD", "NetBSD"]:
                    os.system("sudo apt-get install -y mpg123 >/dev/null 2>&1")
                elif platform.system() == "Solaris":
                    os.system("sudo pkg install -y mpg123 >/dev/null 2>&1")
                return True
        return False
    
    # Mendeteksi bahasa dari text
    def langid_voice(self, text):
        # Mengatur bahasa dan tld sesuai dengan bahasa yang dideteksi
        lang, confidence = langid.classify(text)
        return lang