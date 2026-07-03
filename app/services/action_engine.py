from app.actions.open_app import AppLauncher
from app.actions.open_website import WebsiteLauncher
from app.music.music_engine import MusicEngine
from app.files.file_search import FileSearcher
from app.files.file_opener import FileOpener
from app.models.intent import Intent


class ActionEngine:

    def __init__(self):

        self.app_launcher = AppLauncher()

        self.website_launcher = WebsiteLauncher()

        self.music_engine = MusicEngine()

        self.file_searcher = FileSearcher()

        self.file_opener = FileOpener()

    def execute(self, intent, text):

        if intent == Intent.OPEN_APP:

            return self.app_launcher.open_application(text)

        elif intent == Intent.OPEN_WEBSITE:

            return self.website_launcher.open_website(text)

        elif intent == Intent.OPEN_FILE:

            path = self.file_searcher.search(text)

            return self.file_opener.open(path)

        elif intent == Intent.PLAY_MUSIC:

            print("🎵 Music module under development.")

            return True

        print("No action executed.")

        return False