from app.config.settings import settings
from app.router.intent_router import IntentRouter
from app.services.voice_engine import VoiceEngine
from app.core.action_engine import ActionEngine

from app.nlp.text_cleaner import TextCleaner
from app.nlp.alias_matcher import AliasMatcher


class NovaAssistant:

    def __init__(self):

        self.name = settings.APP_NAME

        self.voice = VoiceEngine()

        self.router = IntentRouter()

        self.actions = ActionEngine()

        self.cleaner = TextCleaner()

        self.aliases = AliasMatcher()

        self.running = True

    def run(self):

        print("=" * 50)
        print(f"🚀 {self.name} Started")
        print("=" * 50)

        while self.running:

            print("\n🎤 Listening...\n")

            text = self.voice.listen()

            if not text:
                continue

            print(f"Original : {text}")

            text = self.cleaner.clean(text)

            text = self.aliases.normalize(text)

            print(f"Normalized : {text}")

            if text in [
                "exit",
                "quit",
                "stop",
                "bye",
                "goodbye",
                "close nova"
            ]:

                print("\n👋 Goodbye!")

                self.running = False

                break

            intent = self.router.detect_intent(text)

            print(f"Detected Intent : {intent.value}")

            self.actions.execute(intent, text)