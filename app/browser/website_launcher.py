import json
import os
import webbrowser
from pathlib import Path

from rapidfuzz import process


class WebsiteLauncher:
    """
    Opens websites using aliases defined in config/websites.json.
    """

    def __init__(self):

        self.websites = {}
        self.alias_map = {}

        self.load_websites()

    def load_websites(self):

        config_path = Path("config/websites.json")

        if not config_path.exists():
            print("⚠ websites.json not found.")
            return

        with open(config_path, "r", encoding="utf-8") as file:
            self.websites = json.load(file)

        self.alias_map.clear()

        for key, value in self.websites.items():

            self.alias_map[key.lower()] = key

            for alias in value.get("aliases", []):

                self.alias_map[alias.lower()] = key

    def get_best_match(self, website: str):

        if not self.alias_map:
            return None

        result = process.extractOne(
            website.lower(),
            self.alias_map.keys(),
            score_cutoff=60,
        )

        if result is None:
            return None

        return self.alias_map[result[0]]

    def open(self, website: str):

        website = website.strip().lower()

        match = self.get_best_match(website)

        if match is None:

            print("❌ Website not found.")

            return False

        url = self.websites[match]["url"]

        try:

            webbrowser.open(url)

            print(f"🌐 Opening {match}")

            return True

        except Exception as error:

            print(error)

            return False