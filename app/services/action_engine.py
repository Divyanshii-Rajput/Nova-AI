from app.actions.open_app import AppLauncher
from app.actions.open_website import WebsiteLauncher
from app.models.intent import Intent


class ActionEngine:
    """
    Executes local actions.
    """

    def __init__(self):

        self.app_launcher = AppLauncher()

        self.website_launcher = WebsiteLauncher()

    def execute(self, intent: Intent, text: str):

        if intent == Intent.OPEN_APP:

            return self.app_launcher.open_application(text)

        elif intent == Intent.OPEN_WEBSITE:

            return self.website_launcher.open_website(text)

        elif intent == Intent.PLAY_MUSIC:

            print("🎵 Music feature coming next sprint.")

            return True

        print("No local action executed.")

        return False