import os
import time
from threading import Thread
from simpleplayer import PlaySong as voice
from simpleplayer import PlaySong

lokasi = []
judul = []
path = "songs"
accepted_formats = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"]
center = 58

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
        self.speaking_thread = None

        if enableSpeak:
            self.speaker = voice
        else:
            self.speaker = lambda text: None
        
    def speaking(self, voice_out):
        # Memutar suara
        self.speaker(voice_out).play()
    
    def speak(self, voice_in):
        # Memulaikan thread untuk memutar suara
        if self.speaker != voice:
            print(f"{os.path.basename(os.path.splitext(voice_in)[0])}")
            time.sleep(1)
            return
        self.stop_speaking()
        self.speaking_thread = Thread(target=self.speaking, args=(voice_in,))
        self.speaking_thread.start()

    def stop_speaking(self):
        # Menghentikan thread untuk memutar suara
        if self.speaking_thread is not None and self.speaking_thread.is_alive():
            self.speaker.keep_speaking = False
        # Menunggu thread selesai
        if self.speaking_thread is not None:
            self.speaking_thread.join()

    def loadLocalSong(self):
        judul.clear()
        lokasi.clear()
        if not os.path.exists(self.path):
            # Jika folder tidak ada, buat folder
            os.makedirs(self.path)
        # Membaca lagu dari folder
        for song in sorted(os.listdir(self.path)):
            # Memisahkan judul lagu dan ekstensi file
            _, file_extension = os.path.splitext(song)
            if file_extension.lower() in accepted_formats:
                lokasi.append(f"{self.path}/{song}")
                judul.append(_)
    
    def updatePath(self, new_path=""):
        if new_path:
            if not os.path.exists(new_path):
                self.speak("voices/Direktori tidak ditemukan.mp3")
                return
            self.path = new_path
        self.loadLocalSong()
        self.speak("voices/Direktori berhasil diubah.mp3")

    def song_exist(self, title, arg=None):
        if self.search_song(title) is not None:
            if arg is None:
                self.speak("voices/Lagu sudah ada.mp3")
            return True

    def add_song(self, title, path):
        # Menambahkan lagu ke daftar putar
        new_song = Song(title, path)
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            self.current_song = new_song
        else:
            self.tail.next_song = new_song
            new_song.prev_song = self.tail
            self.tail = new_song
        self.speak("voices/Berhasil menambahkan lagu.mp3")

    def add_song_in_start(self, title, path):
        # Menambahkan lagu ke daftar putar
        new_song = Song(title, path)
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            self.current_song = new_song
        else:
            new_song.next_song = self.head
            self.head.prev_song = new_song
            self.head = new_song
        self.speak("voices/Berhasil menambahkan lagu.mp3")

    def add_song_in_end(self, title, path):
        new_song = Song(title, path)
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            self.current_song = new_song
        else:
            self.tail.next_song = new_song
            new_song.prev_song = self.tail
            self.tail = new_song
        self.speak("voices/Berhasil menambahkan lagu.mp3")

    def add_song_after(self, title, path, after):
        new_song = Song(title, path)
        if not self.song_exist(after, any):
            return
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current is not None:
                if current.title == after:
                    new_song.next_song = current.next_song
                    new_song.prev_song = current
                    current.next_song = new_song
                    if new_song.next_song is not None:
                        new_song.next_song.prev_song = new_song
                    else:
                        self.tail = new_song
                    break
                current = current.next_song
        self.speak("voices/Berhasil menambahkan lagu.mp3")

    def add_song_before(self, title, path, before):
        new_song = Song(title, path)
        if not self.song_exist(before, any):
            return
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current is not None:
                if current.title == before:
                    new_song.prev_song = current.prev_song
                    new_song.next_song = current
                    current.prev_song = new_song
                    if new_song.prev_song is not None:
                        new_song.prev_song.next_song = new_song
                    else:
                        self.head = new_song
                    break
                current = current.next_song
        self.speak("voices/Berhasil menambahkan lagu.mp3")
    
    def delete_at_start(self):
        current = self.head
        # Menghentikan lagu jika sedang diputar
        if self.current_song == current:
            if self.monitor_player_status("apasaja"):
                self.stopping("delete")
        self.head = current.next_song
        self.current_song = self.head
        self.speak("voices/Berhasil menghapus lagu.mp3")
    
    def delete_at_end(self):
        current = self.head
        ekor = self.tail
        if current.next_song is None:
            self.head = None
            return
        while current is not None:
            if current.next_song is None:
                self.tail = current.prev_song
                self.tail.next_song = None
                if self.current_song == current:
                    if self.monitor_player_status("apasaja"):
                        self.stopping("delete")
                    self.current_song = current.prev_song
                break
            current = current.next_song
        self.speak("voices/Berhasil menghapus lagu.mp3")

    def remove_song(self, song):
        # Menghentikan lagu jika sedang diputar
        if self.monitor_player_status("apasaja"):
            self.stopping("delete")
        # Menghapus lagu dari daftar putar
        if song is self.head:
            # Jika lagu yang dihapus adalah lagu pertama
            self.head = song.next_song
            if self.current_song == song:
                self.current_song = None
        if song is self.tail:
            # Jika lagu yang dihapus adalah lagu terakhir
            self.tail = song.prev_song
        if song.prev_song is not None:
            self.current_song = song.prev_song
            song.prev_song.next_song = song.next_song
        if song.next_song is not None:
            self.current_song = song.next_song
            song.next_song.prev_song = song.prev_song
        self.speak("voices/Berhasil menghapus lagu.mp3")

    def search_song(self, title, arg=None):
        # Mencari lagu dalam daftar putar
        current = self.head
        if arg is None:
            while current is not None:
                # Jika lagu ditemukan
                if current.title == title:
                    return current
                current = current.next_song
            return None
        else:
            founded_items = []
            no = 1
            while current is not None:
                founded_items.append(f"[{no:2}] {current.title}")
                current = current.next_song
                no += 1
            matching_items = [item for item in founded_items if title.lower() in item.lower()]
            return matching_items
    
    def stopping(self, arg=None):
        # Mematikan lagu yang sedang diputar
        if self.player is not None:
            self.player.stop()
            if arg != "delete":
                self.speak("voices/Berhenti memutar lagu.mp3")
            self.player = None
        else:
            if arg is None:
                self.speak("voices/Tidak ada lagu yang diputar.mp3")
    
    def play_song(self, song):
        # Memainkan lagu
        if self.player is not None:
            self.player.stop()
        self.player = PlaySong(song)
        self.player.play()


    def play(self):
        # Memainkan lagu saat ini
        if self.current_song is not None:
            info, path = self.current_song.info()
            self.play_song(path)
            self.speak("voices/Memutar lagu saat ini.mp3")
        else:
            self.speak("voices/Daftar putar kosong.mp3")

    def monitor_player_status(self, arg=None):
        # Memantau status pemutaran lagu
        if self.current_song is not None:
            info, path = self.current_song.info()
        if self.player is not None:
            if arg is None:
                print("\nPlaying: \033[1;35m" + info + "\033[0m")  # Magenta
            else: return True

    def next(self):
        # Memainkan lagu berikutnya
        if self.current_song is not None and self.current_song.next_song is not None:
            self.current_song = self.current_song.next_song
            info, path = self.current_song.info()
            self.play_song(path)
            self.speak("voices/Memutar lagu berikutnya.mp3")
        else:
            self.speak("voices/Daftar putar terakhir.mp3")

    def prev(self):
        # Memainkan lagu sebelumnya
        if self.current_song is not None and self.current_song.prev_song is not None:
            self.current_song = self.current_song.prev_song
            info, path = self.current_song.info()
            self.play_song(path)
            self.speak("voices/Memutar lagu sebelumnya.mp3")
        else:
            self.speak("voices/Daftar putar pertama.mp3")

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
            elif self.current_song is not None and current == self.current_song.next_song:
                print(f"{no}) \033[1;34m{info}\033[0m [Lagu berikutnya]") # Blue
            elif self.current_song is not None and current == self.current_song.prev_song:
                print(f"{no}) \033[1;31m{info}\033[0m [Lagu sebelumnya]") # Red
            else:
                print(f"{no}) {info}")
            current = current.next_song
            no += 1
    
    def isEmpty(self, arg=None):
        # Cek apakah daftar putar kosong
        if Playlist.head is None:
            if arg is None:
                self.speak("voices/Daftar putar kosong.mp3")
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
        self.clearScreen()
        # Menampilkan daftar lagu
        self.subtitle("Daftar Lagu Tersedia")
        print("------------------------------------------------------------")
        if judul:
            for index, lagu in enumerate(judul, start=1):
                print(f"[{index:2}] {lagu}")
        else:
            Playlist.speak("voices/Lagu tidak ditemukan.mp3")
            return
        print("------------------------------------------------------------")
        try:
            tambah = int(input("Pilih lagu yang ingin ditambahkan ke daftar putar: "))
        except ValueError:
            Playlist.speak("voices/Input tidak valid.mp3")
            return
        if tambah not in range(1, len(judul)+1):
            Playlist.speak("voices/Lagu tidak ditemukan.mp3")
            return
        if Playlist.isEmpty(any):
            Playlist.add_song(judul[tambah-1], lokasi[tambah-1])
            return
        
        # Cek apakah lagu sudah ada dalam daftar putar
        if Playlist.song_exist(judul[tambah-1]):
            return
        print("------------------------------------------------------------")
        print("Daftar Putar saat ini: ")
        Playlist.display()
        print("------------------------------------------------------------")
        print("Pilih posisi lagu yang ingin ditambahkan ke daftar putar:")
        print("[1] Tambah di awal daftar putar")
        print("[2] Tambah di akhir daftar putar")
        print("[3] Tambah setelah (judul lagu)")
        print("[4] Tambah sebelum (judul lagu)")
        print("------------------------------------------------------------")

        try:
            posisi = int(input("Masukkan pilihan Anda: "))
        except ValueError:
            Playlist.speak("voices/Input tidak valid.mp3")
            return
        if posisi not in range(1, 5):
            Playlist.speak("voices/Input tidak valid.mp3")
            return
        print("------------------------------------------------------------")

        if posisi == 1:
            Playlist.add_song_in_start(judul[tambah-1], lokasi[tambah-1])
        elif posisi == 2:
            Playlist.add_song_in_end(judul[tambah-1], lokasi[tambah-1])
        elif posisi == 3:
            Playlist.add_song_after(judul[tambah-1], lokasi[tambah-1], input("Tambah setelah lagu: "))
        elif posisi == 4:
            Playlist.add_song_before(judul[tambah-1], lokasi[tambah-1], input("Tambah sebelum lagu: "))
        else:
            Playlist.speak("voices/Input tidak valid.mp3")
            return
        
    def delete_playlist(self):
        if Playlist.isEmpty():
            return
        self.clearScreen()
        self.subtitle("Hapus Lagu Dari Daftar Putar")
        print("------------------------------------------------------------")
        print("Daftar Putar saat ini: ")
        Playlist.display()
        print("------------------------------------------------------------")
        print("Hapus lagu berdasarkan:")
        print("[1] Hapus lagu di awal daftar putar")
        print("[2] Hapus lagu di akhir daftar putar")
        print("[3] Hapus lagu (dengan judul)")
        print("------------------------------------------------------------")
        try:
            hapus = int(input("Pilih lagu yang ingin dihapus dari daftar putar: "))
        except ValueError:
            Playlist.speak("voices/Input tidak valid.mp3")
            return
        if hapus not in range(1, len(judul)+1):
            Playlist.speak("voices/Lagu tidak ditemukan.mp3")
            return
        print("------------------------------------------------------------")
        if hapus == 1:
            Playlist.delete_at_start()
        elif hapus == 2:
            Playlist.delete_at_end()
        elif hapus == 3:
            judul_lagu = input("Masukkan judul lagu yang akan dihapus: ")
            lagu = Playlist.search_song(judul_lagu)
            if lagu:
                Playlist.remove_song(lagu)
            else:
                Playlist.speak("voices/Lagu tidak ditemukan.mp3")
        else:
            Playlist.speak("voices/Input tidak valid.mp3")
        
    def pencarian_lagu(self):
        if Playlist.isEmpty():
            return
        judul_lagu = input("Masukkan judul lagu yang akan dicari: ")
        lagu = Playlist.search_song(judul_lagu, any)
        if lagu:
            self.clearScreen()
            self.subtitle("Hasil Pencarian")
            Playlist.speak("voices/Lagu ditemukan.mp3")
            for lagu in lagu:
                print(lagu)
            input("\nTekan enter untuk melanjutkan...")
        else:
            Playlist.speak("voices/Lagu tidak ditemukan.mp3")

# Buat objek / instance daftar putar
Playlist = Playlist()
App = Application()

# Menu
while True:
    App.clearScreen()
    App.namaProgram()
    Playlist.monitor_player_status()
    print("\nMenu:")
    print(f"[{1:2}] {'♫':2} Tambah daftar putar")
    print(f"[{2:2}] {'⏯':2} Putar lagu saat ini")
    print(f"[{3:2}] {'⏭':2} Putar lagu berikutnya")
    print(f"[{4:2}] {'⏮':2} Putar lagu sebelumnya")
    print(f"[{5:2}] {'⏹':2} Berhenti memutar lagu")
    print(f"[{6:2}] {'🚫'} Hapus dari daftar putar")
    print(f"[{7:2}] {'🔎'} Cari dalam daftar putar")
    if Playlist.speaker == voice:
        print(f"[{8:2}] {'🔇'} Matikan fungsi suara")
    else:
        print(f"[{8:2}] {'🔊'} Nyalakan fungsi suara")
    print(f"[{9:2}] {'⏏️':3} Ganti direktori lagu")
    print(f"[{10:2}] {'⛔'} Keluar")
    print("------------------------------------------------------------")
    pilihan = input("Masukkan pilihan Anda: ")

    if pilihan == "1":
        print("\nDaftar Putar:")
        App.load_playlist()
    elif pilihan == "2":
        Playlist.play()
    elif pilihan == "3":
        Playlist.next()
    elif pilihan == "4":
        Playlist.prev()
    elif pilihan == "5":
        Playlist.stopping()
    elif pilihan == "6":
        App.delete_playlist()
    elif pilihan == "7":
        App.pencarian_lagu()
    elif pilihan == "8":
        if Playlist.speaker == voice:
            Playlist.speak("voices/Suara dinonaktifkan.mp3")
            Playlist.speaker = lambda text: None
        else:
            Playlist.speaker = voice
            Playlist.speak("voices/Suara diaktifkan.mp3")
    elif pilihan == "9":
        path = input("Masukkan path direktori lagu: ")
        Playlist.updatePath(path)
    elif pilihan == "10":
        Playlist.stopping(exit)
        break
    else:
        Playlist.speak("voices/Input tidak valid.mp3")

print("\nKeluar dari program\n")