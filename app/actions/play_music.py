import webbrowser
from urllib.parse import quote_plus


class MusicPlayer:
    """
    Plays music using YouTube search.
    """

    def play(self, text: str):

        text = text.lower()

        # Remove common words
        keywords = [
            "play",
            "song",
            "music",
            "on youtube",
            "youtube",
            "please",
        ]

        for word in keywords:
            text = text.replace(word, "")

        song = text.strip()

        if not song:
            print("❌ No song name detected.")
            return False

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(song)
        )

        webbrowser.open(url)

        print(f"🎵 Searching YouTube for: {song}")

        return True