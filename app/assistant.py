import string

from app.config.settings import settings
from app.router.intent_router import IntentRouter
from app.services.voice_engine import VoiceEngine
from app.services.action_engine import ActionEngine


class NovaAssistant:

    def __init__(self):

        self.name = settings.APP_NAME

        self.voice = VoiceEngine()

        self.router = IntentRouter()

        self.actions = ActionEngine()

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

            print(f"You said : {text}")

            # ----------------------------
            # Clean text
            # ----------------------------

            text_lower = text.lower().strip()

            text_lower = text_lower.translate(
                str.maketrans("", "", string.punctuation)
            )

            # ----------------------------
            # Exit Commands
            # ----------------------------

            if text_lower in [
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

            # ----------------------------
            # Detect Intent
            # ----------------------------

            intent = self.router.detect_intent(text)

            print(f"Detected Intent : {intent.value}")

            # ----------------------------
            # Execute Action
            # ----------------------------

            self.actions.execute(intent, text)