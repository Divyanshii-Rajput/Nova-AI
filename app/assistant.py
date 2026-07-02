from app.config.settings import settings
from app.router.intent_router import IntentRouter
from app.services.voice_engine import VoiceEngine


class NovaAssistant:

    def __init__(self):

        self.name = settings.APP_NAME

        self.voice = VoiceEngine()

        self.router = IntentRouter()

    def start(self):

        print("=" * 50)
        print(self.name)
        print("=" * 50)

        text = self.voice.listen()

        print()

        print(f"You said : {text}")

        intent = self.router.detect_intent(text)

        print()

        print(f"Detected Intent : {intent.value}")