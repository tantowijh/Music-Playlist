# Music Playlist Double Linked List

This project implements a music playlist using a doubly linked list data structure in Python. The playlist allows you to manage and play music from a local folder called 'songs'.

## Features

1. **Load Music from Local Folder**: The program loads music files from the 'songs' folder in the local directory and creates a playlist with the songs.

2. **Add Song to Playlist**: Menu option 1 allows you to add a song from the 'songs' folder to the playlist. Simply select the song you want to add, and it will be appended to the playlist.

3. **Play Current Song**: Menu option 2 plays the currently selected song in the playlist. The program will play the audio of the song using the default media player.

4. **Play Next Song**: Menu option 3 plays the next song in the playlist. If the current song is the last in the playlist, it will loop back to the first song.

5. **Play Previous Song**: Menu option 4 plays the previous song in the playlist. If the current song is the first in the playlist, it will loop back to the last song.

6. **Stop the Song**: Menu option 5 stops the currently playing song.

7. **Delete Songs in Playlist**: Menu option 6 allows you to delete songs from the playlist. You can select a song to remove, and it will be removed from the playlist.

8. **Search in Playlist**: Menu option 7 enables you to search for a specific song in the playlist. Enter the title of the song, and the program will display the corresponding song if found.

9. **Toggle Add/Remove Song Feature**: Menu option 8 lets you enable or disable the feature to add and remove songs from the playlist. You can turn it on or off as per your preference.

10. **Exit Program**: Menu option 9 allows you to exit the program gracefully.

## Prerequisites

- Python 3.x
- Local folder 'songs' containing the music files

## How to Run

1. Clone or download this repository to your local machine.

2. Ensure that your music files are placed in the 'songs' folder within the project directory.

3. Open a terminal or command prompt and navigate to the project directory.

4. Run the following command to start the program:

```python
import os
print("Hello, World!")
```

5. Follow the on-screen menu instructions to interact with the music playlist.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to modify and enhance it according to your needs.

**Note**: Please ensure that you have the necessary permissions to use and distribute the music files in the 'songs' folder.
