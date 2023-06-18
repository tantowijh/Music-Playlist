import subprocess   

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