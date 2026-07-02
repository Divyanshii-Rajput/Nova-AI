from app.music.youtube_player import YouTubePlayer


class MusicEngine:

    def __init__(self):

        self.youtube = None

    def play(self, text):

        if self.youtube is None:

            self.youtube = YouTubePlayer()

        text = text.lower()

        remove_words = [
            "play",
            "song",
            "music",
            "youtube",
            "on youtube",
            "please",
        ]

        for word in remove_words:

            text = text.replace(word, "")

        song = text.strip()

        if not song:

            print("No song detected.")

            return False

        return self.youtube.play(song)