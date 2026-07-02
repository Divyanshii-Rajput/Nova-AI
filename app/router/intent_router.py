from app.models.intent import Intent


class IntentRouter:
    """
    Determines the user's intent.
    """

    def detect_intent(self, text: str) -> Intent:

        text = text.lower()

        music_keywords = [
            "play",
            "song",
            "music",
            "gaana",
            "gana"
        ]

        if any(word in text for word in music_keywords):
            return Intent.PLAY_MUSIC

        websites = [
            "youtube",
            "gmail",
            "github",
            "linkedin",
            "leetcode",
            "chatgpt",
            "geeksforgeeks"
        ]

        if any(site in text for site in websites):
            return Intent.OPEN_WEBSITE

        # Spotify should be treated as music
        if "spotify" in text:
            return Intent.PLAY_MUSIC

        app_keywords = [
            "open",
            "launch",
            "start"
        ]

        if any(word in text for word in app_keywords):
            return Intent.OPEN_APP

        return Intent.AI_CHAT