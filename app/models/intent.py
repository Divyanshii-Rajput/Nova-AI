from enum import Enum


class Intent(Enum):
    """
    Represents all supported intents in Nova AI.
    """

    OPEN_APP = "open_app"
    OPEN_FILE = "open_file"
    PLAY_MUSIC = "play_music"
    SEARCH_WEB = "search_web"
    SYSTEM = "system"

    AI_CHAT = "ai_chat"

    UNKNOWN = "unknown"