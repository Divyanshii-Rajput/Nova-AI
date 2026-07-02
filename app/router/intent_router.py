from app.models.intent import Intent


class IntentRouter:
    """
    Determines the user's intent based on the recognized text.
    """

    def __init__(self):

        self.app_keywords = [
            "open",
            "launch",
            "start"
        ]

        self.music_keywords = [
            "play",
            "song",
            "music"
        ]

        self.web_keywords = [
            "search",
            "google"
        ]

    def detect_intent(self, text: str) -> Intent:

        text = text.lower()

        # ---------- Open Application ----------

        if any(word in text for word in self.app_keywords):
            return Intent.OPEN_APP

        # ---------- Play Music ----------

        if any(word in text for word in self.music_keywords):
            return Intent.PLAY_MUSIC

        # ---------- Search Web ----------

        if any(word in text for word in self.web_keywords):
            return Intent.SEARCH_WEB

        # ---------- AI ----------

        return Intent.AI_CHAT