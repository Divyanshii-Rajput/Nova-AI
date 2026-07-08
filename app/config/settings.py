import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Global configuration for Nova AI.
    """

    CONFIG_PATH = Path("config/settings.json")

    # -----------------------------------
    # Defaults
    # -----------------------------------

    APP_NAME = "Nova AI"
    VERSION = "1.0 Beta"

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

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_MODEL = "llama3-8b-8192"

    OLLAMA_MODEL = "llama3"

    OLLAMA_HOST = "http://localhost:11434"

    LLM_PROVIDERS = ["gemini", "groq", "ollama"]

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

    # -----------------------------------
    # User Persisted Settings
    # -----------------------------------

    THEME = "System"
    STARTUP = False
    VOICE = "Default"
    VOLUME = 75
    MODEL = "Gemini"
    TEMPERATURE = 50

    @classmethod
    def load(cls) -> None:
        """
        Load settings from settings.json.
        """
        if not cls.CONFIG_PATH.exists():
            return

        try:
            with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            cls.THEME = data.get("theme", cls.THEME)
            cls.STARTUP = data.get("startup", cls.STARTUP)
            cls.VOICE = data.get("voice", cls.VOICE)
            cls.VOLUME = data.get("volume", cls.VOLUME)
            cls.MODEL = data.get("model", cls.MODEL)
            cls.TEMPERATURE = data.get("temperature", cls.TEMPERATURE)
        except Exception:
            pass

    @classmethod
    def save(cls) -> None:
        """
        Save settings to settings.json.
        """
        cls.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(cls.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "theme": cls.THEME,
                    "startup": cls.STARTUP,
                    "voice": cls.VOICE,
                    "volume": cls.VOLUME,
                    "model": cls.MODEL,
                    "temperature": cls.TEMPERATURE,
                }, f, indent=4)
        except Exception:
            pass


# Load settings on module import
Settings.load()