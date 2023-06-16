import soundfile as sf
import sounddevice as sd
import sys

class AudioPlayer:
    def __init__(self, filename):
        self.filename = filename

    def play(self):
        # Read the audio data and sample rate using soundfile
        data, sample_rate = sf.read(self.filename)

        # Play the audio using sounddevice
        sd.play(data, sample_rate)
        sd.wait()  # Wait until the playback is finished

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python Player.py <song_file>")
        sys.exit(1)

    song = sys.argv[1]
    player = AudioPlayer(song)
    player.play()