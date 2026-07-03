from enum import Enum


class Intent(Enum):
    """
    Represents every supported user command.
    """

    OPEN_APP = "open_app"
    OPEN_FILE = "open_file"
    OPEN_FOLDER = "open_folder"

    OPEN_WEBSITE = "open_website"
    SEARCH_WEB = "search_web"

    PLAY_MUSIC = "play_music"

    TAKE_SCREENSHOT = "take_screenshot"

    SYSTEM_CONTROL = "system_control"

    AI_CHAT = "ai_chat"

    EXIT = "exit"

    UNKNOWN = "unknown"