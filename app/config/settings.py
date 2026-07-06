import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Global configuration for Nova AI.
    """

    # -----------------------------------
    # Application
    # -----------------------------------

    APP_NAME = "Nova AI"
    VERSION = "1.0 Beta"

    # -----------------------------------
    # Speech
    # -----------------------------------

    WHISPER_MODEL = "base"

    RECORD_DURATION = 5

    VOICE_OUTPUT = True

    SPEECH_RATE = 180

    SPEECH_VOLUME = 1.0

    # -----------------------------------
    # AI
    # -----------------------------------

    AI_ENABLED = True

    AI_PROVIDER = "gemini"

    GEMINI_MODEL = "gemini-2.5-flash"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # -----------------------------------
    # Search
    # -----------------------------------

    MAX_FILE_RESULTS = 5

    FUZZY_MATCH_SCORE = 70

    # -----------------------------------
    # UI
    # -----------------------------------

    SHOW_STARTUP_BANNER = True

    SHOW_RECOGNIZED_TEXT = True

    SHOW_NORMALIZED_TEXT = True

    SHOW_ENTITY = True

    SHOW_INTENT = True

    # -----------------------------------
    # Logging
    # -----------------------------------

    DEBUG = False