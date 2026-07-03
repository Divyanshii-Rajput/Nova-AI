from app.models.intent import Intent


class IntentRouter:

    WEBSITE_KEYWORDS = [
        "youtube",
        "github",
        "gmail",
        "linkedin",
        "chatgpt",
        "leetcode",
        "geeksforgeeks"
    ]

    MUSIC_KEYWORDS = [
        "play",
        "music",
        "song"
    ]

    APP_KEYWORDS = [
        "open",
        "launch",
        "start"
    ]

    def detect_intent(self, text: str):

        text = text.lower()

        if any(word in text for word in self.MUSIC_KEYWORDS):
            return Intent.PLAY_MUSIC

        if any(word in text for word in self.WEBSITE_KEYWORDS):
            return Intent.OPEN_WEBSITE

        if any(word in text for word in self.APP_KEYWORDS):
            return Intent.OPEN_APP

        return Intent.AI_CHAT