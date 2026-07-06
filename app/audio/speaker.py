import pyttsx3


class Speaker:
    """
    Converts text to speech using the system TTS engine.
    """

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 180)

        self.engine.setProperty("volume", 1.0)

    def speak(self, text: str):

        if not text:
            return

        self.engine.say(text)

        self.engine.runAndWait()