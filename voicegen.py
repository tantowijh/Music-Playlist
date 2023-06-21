import os
from simpleplayer import voicegen

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

if not os.path.exists('voices'):
    os.makedirs('voices')
    
if __name__ == "__main__":
    for voice in text_to_say_gen:
        voicegen(voice, f"voices/{voice}", 'id')
