from app.models.intent import Intent


class IntentDetector:
    """
    Detects the user's intent.
    """

    FILE_HINTS = {
        "resume",
        "report",
        "notes",
        "assignment",
        "project",
        "ppt",
        "pdf",
        "doc",
        "chapter",
        "unit",
        "semester",
        "lab",
        "syllabus",
    }

    WEBSITE_NAMES = {
        "youtube",
        "github",
        "linkedin",
        "gmail",
        "chatgpt",
        "leetcode",
        "geeksforgeeks",
    }

    APP_KEYWORDS = {
        "open",
        "launch",
        "start",
    }

    MUSIC_KEYWORDS = {
        "play",
        "song",
        "music",
    }

    SEARCH_KEYWORDS = {
        "search",
        "google",
    }

    EXIT_KEYWORDS = {
        "exit",
        "quit",
        "bye",
        "goodbye",
        "close",
    }

    SCREENSHOT_KEYWORDS = {
        "screenshot",
        "capture",
    }

    SYSTEM_KEYWORDS = {
        "volume",
        "brightness",
        "shutdown",
        "restart",
        "lock",
        "sleep",
    }

    def detect(self, text: str) -> Intent:

        words = set(text.split())

        if words & self.EXIT_KEYWORDS:
            return Intent.EXIT

        if words & self.SCREENSHOT_KEYWORDS:
            return Intent.TAKE_SCREENSHOT

        if words & self.SYSTEM_KEYWORDS:
            return Intent.SYSTEM_CONTROL

        if words & self.SEARCH_KEYWORDS:
            return Intent.SEARCH_WEB

        if words & self.MUSIC_KEYWORDS:
            return Intent.PLAY_MUSIC

        if words & self.WEBSITE_NAMES:
            return Intent.OPEN_WEBSITE

        if words & self.FILE_HINTS:
            return Intent.OPEN_FILE

        if words & self.APP_KEYWORDS:
            return Intent.OPEN_APP

        return Intent.AI_CHAT