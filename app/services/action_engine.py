from app.actions.open_app import AppLauncher
from app.actions.open_website import WebsiteLauncher
from app.music.music_engine import MusicEngine
from app.models.intent import Intent


class ActionEngine:

    def __init__(self):

        self.app_launcher = AppLauncher()
        self.website_launcher = WebsiteLauncher()
        self.music_engine = MusicEngine()

    def execute(self, intent, text):

        if intent == Intent.OPEN_APP:
            return self.app_launcher.open_application(text)

        elif intent == Intent.OPEN_WEBSITE:
            return self.website_launcher.open_website(text)

        elif intent == Intent.PLAY_MUSIC:
            return self.music_engine.play(text)

        print("No action executed.")

        return False