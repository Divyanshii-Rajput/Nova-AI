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

            text_lower = text.lower()

            if text_lower in ["exit", "quit", "stop", "bye"]:

                from app.browser.browser_manager import BrowserManager

                BrowserManager().close()

                print("\n👋 Goodbye!")

                self.running = False

                break

            intent = self.router.detect_intent(text)

            print(f"Detected Intent : {intent.value}")

            self.actions.execute(intent, text)