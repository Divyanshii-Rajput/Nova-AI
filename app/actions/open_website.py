import json
import webbrowser
from pathlib import Path


class WebsiteLauncher:

    def __init__(self):

        config_path = Path("config/websites.json")

        with open(config_path, "r") as file:

            self.websites = json.load(file)

    def open_website(self, text: str):

        text = text.lower()

        for website, url in self.websites.items():

            if website in text:

                webbrowser.open(url)

                print(f"🌐 Opening {website}")

                return True

        print("❌ Website not found")

        return False