import os
import socket
from gtts import gTTS


class VoiceGenerator:
    # Kelas ini akan mengubah teks menjadi suara
    def __init__(self, text, filename, lang='id'):
        if not self.check_internet_connection():
            print('Tidak ada koneksi internet')
            return
        if not os.path.exists('voices'):
            os.makedirs('voices')
        filename = "voices/"+filename+'.mp3'

        # Render teks ke dalam file MP3
        tts = gTTS(text, lang=lang)
        tts.save(filename)
    
    def check_internet_connection(self):
        try:
            # Mencoba membuat koneksi ke DNS Google pada port 53, timeout 3 detik
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except socket.error:
            return False


text_to_say_gen = [
    "Suara diaktifkan",
    "Suara dinonaktifkan",
    "Direktori tidak ditemukan",
    "Berhasil menghapus lagu",
    "Lagu tidak ditemukan",
    "Daftar putar terakhir",
    "Berhasil menambahkan lagu",
    "Direktori berhasil diubah",
    "Memutar lagu berikutnya",
    "Daftar putar pertama",
    "Berhenti memutar lagu",
    "Daftar putar kosong",
    "Memutar lagu sebelumnya",
    "Lagu sudah ada",
    "Input tidak valid",
    "Lagu ditemukan",
    "Memutar lagu saat ini",
    "Tidak ada lagu yang diputar",
]

save = "voices"

if __name__ == "__main__":
    for voice in text_to_say_gen:
        VoiceGenerator(voice, voice, 'id')
