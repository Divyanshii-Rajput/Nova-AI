from app.config.settings import settings
from app.voice.recorder import AudioRecorder
from app.voice.transcriber import SpeechTranscriber


class NovaAssistant:

    def __init__(self):

        self.name = settings.APP_NAME

        self.recorder = AudioRecorder()

        self.transcriber = SpeechTranscriber()

    def start(self):

        print("=" * 50)
        print(self.name)
        print("=" * 50)

        audio = self.recorder.record()

        text = self.transcriber.transcribe(audio)

        print()

        print("You said:")

        print(text)