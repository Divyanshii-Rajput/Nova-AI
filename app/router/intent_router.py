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

    FILE_KEYWORDS = [
        "resume",
        ".pdf",
        ".doc",
        ".ppt",
        ".pptx",
        "notes",
        "report",
        "assignment",
        "project"
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

        if any(word in text for word in self.FILE_KEYWORDS):
            return Intent.OPEN_FILE

        if any(word in text for word in self.APP_KEYWORDS):
            return Intent.OPEN_APP

        return Intent.AI_CHAT