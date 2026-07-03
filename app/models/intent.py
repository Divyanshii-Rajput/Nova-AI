from enum import Enum


class Intent(Enum):

    OPEN_APP = "open_app"

    OPEN_WEBSITE = "open_website"

    OPEN_FILE = "open_file"

    PLAY_MUSIC = "play_music"

    SEARCH_WEB = "search_web"

    AI_CHAT = "ai_chat"

    UNKNOWN = "unknown"