import logging
import threading
import sys
import subprocess
import base64
from PySide6.QtCore import QObject

logger = logging.getLogger(__name__)


class Speaker(QObject):
    """
    Converts text to speech using an isolated subprocess calling SAPI5 SpVoice.
    This guarantees zero COM apartment conflicts and zero event loop deadlocks.
    """

    def __init__(self):
        super().__init__()
        self._process = None
        self._lock = threading.Lock()

    def stop(self) -> None:
        """
        Cancel any ongoing text-to-speech rendering immediately.
        """
        with self._lock:
            if self._process and self._process.poll() is None:
                try:
                    self._process.terminate()
                except Exception:
                    pass

    def speak(self, text: str):
        """
        Speak the given text synchronously, blocking the caller thread pool context.
        """
        if not text:
            return

        self.stop()

        from app.config.settings import Settings
        Settings.load()

        volume = int(Settings.VOLUME)
        rate = int((Settings.SPEECH_RATE - 180) / 10)
        selected_voice = Settings.VOICE

        # Base64 encode the speech text to ensure safe parsing of quotes and newlines
        b64_text = base64.b64encode(text.encode("utf-8")).decode("utf-8")

        # Build clean self-contained python code to dispatch SAPI5 in an isolated process
        code = f"""
import win32com.client
import pythoncom
import base64
import sys

try:
    pythoncom.CoInitialize()
    voice = win32com.client.Dispatch("SAPI.SpVoice")
    voice.Volume = {volume}
    voice.Rate = {rate}
    
    selected_voice = {repr(selected_voice)}
    if selected_voice != "Default":
        voices = voice.GetVoices()
        target_gender = selected_voice.lower()
        for i in range(voices.Count):
            v = voices.Item(i)
            desc = v.GetDescription().lower()
            if target_gender in desc:
                voice.Voice = v
                break
                
    text = base64.b64decode("{b64_text}").decode("utf-8")
    voice.Speak(text)
except Exception as e:
    sys.exit(1)
"""

        with self._lock:
            self._process = subprocess.Popen(
                [sys.executable, "-c", code],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        # Block synchronously until the speaking process exits
        self._process.wait()