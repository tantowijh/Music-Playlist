import os
import platform
import subprocess

# Inisialisasi class untuk memainkan audio
class AudioPlayer:
    def __init__(self, song):
        self.song = song
        self.process = None
        
        # Memainkan audio sesuai dengan OS yang digunakan pengguna
        # audio diputar menggunakan subprocess Popen dengan parameter yang sesuai dengan OS
        if platform.system() == "Windows":
            self.process = subprocess.Popen(['start', '', song], shell=True)
        elif platform.system() == "Darwin":
            self.process = subprocess.Popen(['afplay', song])
        else:
            if self.audio_setup():
                self.process = subprocess.Popen(['mpg123', song])
    
    def audio_setup(self):
        # Cek apakah pengguna sudah menginstall mpg123 khusus untuk OS Linux, FreeBSD, OpenBSD, NetBSD, dan Solaris
        if platform.system() in ["Linux", "FreeBSD", "OpenBSD", "NetBSD", "Solaris"]:
            if os.system("which mpg123 >/dev/null 2>&1") != 0:
                # mpg123 belum terinstall, maka akan diinstall terlebih dahulu
                if platform.system() in ["Linux", "FreeBSD", "OpenBSD", "NetBSD"]:
                    os.system("sudo apt-get install -y mpg123 >/dev/null 2>&1")
                elif platform.system() == "Solaris":
                    os.system("sudo pkg install -y mpg123 >/dev/null 2>&1")
                return True
        return False
    
    def stop(self):
        # Mematikan audio sesuai dengan OS yang digunakan pengguna
        if self.process is not None:
            if platform.system() == "Windows":
                if self.process.poll() is None:
                    os.system("taskkill /f /im mpg123.exe")
            else:
                self.process.terminate()
        
       
