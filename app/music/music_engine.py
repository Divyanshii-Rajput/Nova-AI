from app.browser.youtube import YouTubePlayer


class MusicEngine:

    def __init__(self):

        self.youtube = YouTubePlayer()

    def play(self, text: str):

        text = text.lower()

        words = [
            "play",
            "song",
            "music",
            "youtube",
            "on youtube",
            "please",
        ]

        for word in words:

            text = text.replace(word, "")

        song = text.strip()

        if not song:

            print("No song detected.")

            return False

        return self.youtube.play(song)