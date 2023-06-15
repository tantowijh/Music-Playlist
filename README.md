# Music Playlist Double Linked List

Proyek ini mengimplementasikan sebuah playlist musik menggunakan struktur data doubly linked list dalam bahasa Python. Playlist ini memungkinkan Anda mengelola dan memutar musik dari folder lokal yang bernama 'songs'.

## Fitur

1. **Muat Musik dari Folder Lokal**: Program ini memuat file musik dari folder 'songs' pada direktori lokal dan membuat sebuah playlist dengan lagu-lagu tersebut.

2. **Tambahkan Lagu ke Playlist**: Opsi menu 1 memungkinkan Anda menambahkan lagu dari folder 'songs' ke dalam playlist. Cukup pilih lagu yang ingin ditambahkan, dan lagu tersebut akan ditambahkan ke playlist.

3. **Putar Lagu Saat Ini**: Opsi menu 2 memutar lagu yang saat ini dipilih dalam playlist. Program akan memutar audio dari lagu tersebut menggunakan pemutar media default.

4. **Putar Lagu Berikutnya**: Opsi menu 3 memutar lagu berikutnya dalam playlist. Jika lagu saat ini adalah lagu terakhir dalam playlist, program akan kembali memutar lagu pertama.

5. **Putar Lagu Sebelumnya**: Opsi menu 4 memutar lagu sebelumnya dalam playlist. Jika lagu saat ini adalah lagu pertama dalam playlist, program akan kembali memutar lagu terakhir.

6. **Hentikan Lagu**: Opsi menu 5 menghentikan lagu yang sedang diputar.

7. **Hapus Lagu dalam Playlist**: Opsi menu 6 memungkinkan Anda menghapus lagu-lagu dari playlist. Anda dapat memilih lagu yang ingin dihapus, dan lagu tersebut akan dihapus dari playlist.

8. **Cari dalam Playlist**: Opsi menu 7 memungkinkan Anda mencari lagu tertentu dalam playlist. Masukkan judul lagu, dan program akan menampilkan lagu yang sesuai jika ditemukan.

9. **Toggle Speaker Aktif/Non-Aktif**: Opsi menu 8 memungkinkan Anda mengaktifkan atau menonaktifkan fitur suara. Anda dapat menghidupkan atau mematikan fitur ini sesuai keinginan.

10. **Ganti Folder Memuat Musik**: Opsi menu 9 memungkinkan Anda mengganti folder yang digunakan untuk memuat musik.

10. **Keluar dari Program**: Opsi menu 10 memungkinkan Anda keluar dari program dengan aman.

## Prasyarat

- Python 3.x
- Folder lokal 'songs' yang berisi file musik

## Cara Menjalankan

1. Clone atau unduh repository ini ke directory lokal Anda.

2. Install library yang dibutuhkan dengan menjalankan perintah berikut:

```
pip install -r requirements.txt
```

3. Pastikan file musik Anda ditempatkan dalam folder 'songs' di dalam direktori proyek.

4. Buka terminal atau command prompt, lalu navigasikan ke direktori proyek.

5. Jalankan perintah berikut untuk memulai program:

```
pytho3 main.py
```

6. Ikuti petunjuk menu yang ditampilkan di layar untuk berinteraksi dengan playlist musik.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to modify and enhance it according to your needs.

**Note**: Pastikan Anda memiliki izin yang diperlukan untuk menggunakan dan mendistribusikan file musik dalam folder 'songs'. Jika Anda mengaktifkan mode suara, pastikan Anda terhubung ke internet.
