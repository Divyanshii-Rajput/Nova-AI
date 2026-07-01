from app.config.settings import settings


class NovaAssistant:
    """
    Main controller for the Nova AI Assistant.
    Coordinates initialization and future services.
    """

    def __init__(self):
        self.app_name = settings.APP_NAME
        self.version = settings.VERSION

    def start(self):
        print("=" * 50)
        print(f"🚀 Welcome to {self.app_name}")
        print(f"Version : {self.version}")
        print("=" * 50)
        print("Nova AI has started successfully!")