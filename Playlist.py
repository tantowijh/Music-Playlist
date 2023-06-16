import os
import time
import subprocess
from Speaker import Speak as voice

lokasi = []
judul = []
path = "songs"
accepted_formats = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"]
center = 50

class Song:
    def __init__(self, title, path):
        # Inisialisasi atribut
        self.title = title
        self.path = path
        self.prev_song = None
        self.next_song = None

    def info(self):
        # Mengembalikan informasi lagu
        return f"{self.title}", f"{self.path}"

class Playlist:
    def __init__(self, enableSpeak=True):
        # Inisialisasi atribut
        self.path = path
        self.loadLocalSong()
        self.head = None
        self.tail = None
        self.current_song = None
        self.player = None
        if enableSpeak:
            self.speak = voice
        else:
            self.speak = lambda text: None

    def loadLocalSong(self):
        judul.clear()
        lokasi.clear()
        if not os.path.exists(self.path):
            # Jika folder tidak ada, buat folder
            os.makedirs(self.path)
        # Membaca lagu dari folder
        for song in os.listdir(self.path):
            _, file_extension = os.path.splitext(song)
            if file_extension.lower() in accepted_formats:
                lokasi.append(f"{self.path}/{song}")
                judul.append(os.path.splitext(song)[0])
    
    def updatePath(self, new_path=""):
        if new_path:
            if not os.path.exists(new_path):
                print("Direktori tidak ditemukan! Buat direktori baru atau masukkan direktori yang benar.")
                time.sleep(2)
                return
            self.path = new_path
        self.loadLocalSong()

    def add_song(self, title, path):
        # Menambahkan lagu ke daftar putar
        new_song = Song(title, path)
        # Cek apakah lagu sudah ada dalam daftar putar
        if self.search_song(title) is not None:
            print("Lagu sudah ada dalam daftar putar")
            time.sleep(2)
            return
        # Menambahkan lagu ke daftar putar
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            self.current_song = new_song
        # Jika daftar putar tidak kosong
        else:
            new_song.prev_song = self.tail
            self.tail.next_song = new_song
            self.tail = new_song
        self.speak(f"{title}")
        self.speak(f"berhasil ditambahkan ke daftar putar")

    def remove_song(self, song):
        # Menghapus lagu dari daftar putar
        if song is self.head:
            # Jika lagu yang dihapus adalah lagu pertama
            self.head = song.next_song
        if song is self.tail:
            # Jika lagu yang dihapus adalah lagu terakhir
            self.tail = song.prev_song
        if song.prev_song is not None:
            # Jika lagu yang dihapus bukan lagu pertama
            song.prev_song.next_song = song.next_song
        if song.next_song is not None:
            # Jika lagu yang dihapus bukan lagu terakhir
            song.next_song.prev_song = song.prev_song
        if song is self.current_song:
            # Jika lagu yang dihapus adalah lagu yang sedang diputar
            self.stopping()
            if song.next_song is not None:
                song.next_song.prev_song = song.prev_song
            self.current_song = song.next_song

        self.speak(f"{song.title}")
        self.speak(f"berhasil dihapus dari daftar putar")

    def search_song(self, title):
        # Mencari lagu dalam daftar putar
        current = self.head
        while current is not None:
            # Jika lagu ditemukan
            if current.title == title:
                return current
            current = current.next_song
        return None
    
    def stopping(self):
        # Mematikan lagu yang sedang diputar
        if self.player is not None and self.player.poll() is None:
            print("\nMematikan lagu...")
            self.player.terminate()
        else:
            print("\nTidak ada lagu yang sedang diputar!")
    
    def play_song(self, song):
        # Memainkan lagu
        if self.player is not None and self.player.poll() is None:
            self.player.terminate()
        command = ["python", "Player.py", song]
        self.player = subprocess.Popen(command)


    def play(self):
        # Memainkan lagu saat ini
        if self.current_song is not None:
            info, path = self.current_song.info()
            print("Playing:", info)
            self.play_song(path)
        else:
            print("Daftar putar kosong!")

    def monitor_player_status(self):
        # Memantau status pemutaran lagu
        if self.current_song is not None:
            info, path = self.current_song.info()
        if self.player is not None and self.player.poll() is None:
            print("\nPlaying: \033[1;35m" + info + "\033[0m")  # Magenta

    def next(self):
        # Memainkan lagu berikutnya
        if self.current_song is not None and self.current_song.next_song is not None:
            self.current_song = self.current_song.next_song
            info, path = self.current_song.info()
            print("Memutar lagu selanjutnya:", info)
            self.play_song(path)
        else:
            print("Akhir daftar putar")

    def prev(self):
        # Memainkan lagu sebelumnya
        if self.current_song is not None and self.current_song.prev_song is not None:
            self.current_song = self.current_song.prev_song
            info, path = self.current_song.info()
            print("Memutar lagu sebelumnya:", info)
            self.play_song(path)
        else:
            print("Awal daftar putar")

    def display(self):
        # Menampilkan daftar putar
        current = self.head
        no = 1
        if current is None:
            print("Daftar putar kosong!")
            return
        while current is not None:
            info, path = current.info()
            if current == self.current_song:
                print(f"{no}) \033[1;32m{info}\033[0m [Lagu saat ini]")  # Green
            elif current == self.current_song.next_song:
                print(f"{no}) \033[1;34m{info}\033[0m [Lagu berikutnya]")
            elif current == self.current_song.prev_song:
                print(f"{no}) \033[1;31m{info}\033[0m [Lagu sebelumnya]")
            else:
                print(f"{no}) {info}")
            current = current.next_song
            no += 1
    
    def isEmpty(self):
        # Cek apakah daftar putar kosong
        if Playlist.head is None:
            print("\nDaftar putar kosong!")
            time.sleep(2)
            return True

class Application:
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def namaProgram(self):
        # Nama program
        program_name = "MUSIC PLAYER"
        subtitle = "Double Linked List Program"
        underline = "-" * center

        # Cetak nama program
        print("╔" + "═" * center + "╗")
        print("║" + program_name.center(center) + "║")
        print("║" + underline.center(center) + "║")
        print("║" + subtitle.center(center) + "║")
        print("╚" + "═" * center + "╝")

        print("\nDaftar Putar:")
        Playlist.display()
    
    def subtitle(self, subtitle):
        # Nama program
        program_name = subtitle
        # Cetak nama program
        print("╔" + "═" * center + "╗")
        print("║" + program_name.center(center) + "║")
        print("╚" + "═" * center + "╝")

    def load_playlist(self):
        # Menampilkan daftar lagu
        self.subtitle("Daftar Lagu Tersedia")
        if judul:
            for index, lagu in enumerate(judul, start=1):
                print(f"[{index:2}] {lagu}")
        else:
            print("Tidak ada lagu yang tersedia!")
            time.sleep(2)
            return
        print("----------------------------------------------------------")
        try:
            tambah = int(input("Pilih lagu yang ingin ditambahkan ke daftar putar: "))
        except ValueError:
            print("Input harus berupa angka!")
            time.sleep(2)
            return
        if tambah not in range(1, len(judul)+1):
            print("Lagu tidak ditemukan dalam daftar lagu")
            time.sleep(2)
            return
        Playlist.add_song(judul[int(tambah)-1], lokasi[int(tambah)-1])

# Buat objek daftar putar
Playlist = Playlist()
App = Application()

# Menu
while True:
    App.clearScreen()
    App.namaProgram()
    Playlist.monitor_player_status()
    print("\nMenu:")
    print("[ 1] Tambah daftar putar")
    print("[ 2] Putar lagu saat ini")
    print("[ 3] Putar lagu berikutnya")
    print("[ 4] Putar lagu sebelumnya")
    print("[ 5] Berhenti memutar lagu")
    print("[ 6] Hapus dari daftar putar")
    print("[ 7] Cari dalam daftar putar")
    if Playlist.speak == voice:
        print("[ 8] Matikan fungsi suara")
    else:
        print("[ 8] Nyalakan fungsi suara")
    print("[ 9] Ganti direktori lagu")
    print("[10] Keluar")
    print("----------------------------")
    pilihan = input("Masukkan pilihan Anda: ")

    if pilihan == "1":
        print("\nDaftar Putar:")
        App.load_playlist()
    elif pilihan == "2":
        print("\nMemutar lagu saat ini:")
        Playlist.play()
        time.sleep(1.5)
    elif pilihan == "3":
        print("\nMemutar lagu berikutnya:")
        Playlist.next()
        time.sleep(1.5)
    elif pilihan == "4":
        print("\nMemutar lagu sebelumnya:")
        Playlist.prev()
        time.sleep(1.5)
    elif pilihan == "5":
        Playlist.stopping()
        time.sleep(1.5)
    elif pilihan == "6":
        if Playlist.isEmpty():
            continue
        print()
        judul_lagu = input("Masukkan judul lagu yang akan dihapus: ")
        lagu = Playlist.search_song(judul_lagu)
        if lagu:
            Playlist.remove_song(lagu)
            print("Lagu berhasil dihapus dari daftar putar")
        else:
            print("Lagu tidak ditemukan dalam daftar putar")
        time.sleep(2)
    elif pilihan == "7":
        if Playlist.isEmpty():
            continue
        print()
        judul_lagu = input("Masukkan judul lagu yang akan dicari: ")
        lagu = Playlist.search_song(judul_lagu)
        if lagu:
            print("Lagu ditemukan dalam daftar putar")
        else:
            print("Lagu tidak ditemukan dalam daftar putar")
        time.sleep(2)
    elif pilihan == "8":
        if Playlist.speak == voice:
            Playlist.speak = lambda text: None
            print("\nSuara dimatikan")
            time.sleep(1)
        else:
            Playlist.speak = voice
            print()
            Playlist.speak("Menyalakan suara")
    elif pilihan == "10":
        Playlist.stopping()
        break
    elif pilihan == "9":
        path = input("Masukkan path direktori lagu: ")
        Playlist.updatePath(path)
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
        time.sleep(2)

print("\nKeluar dari program\n")