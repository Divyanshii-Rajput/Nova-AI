import json
import subprocess
from pathlib import Path


class AppLauncher:

    def __init__(self):

        config_path = Path("config/apps.json")

        with open(config_path, "r") as file:

            self.apps = json.load(file)

    def open_application(self, text: str):

        text = text.lower()

        for keyword, command in self.apps.items():

            if keyword in text:

                try:

                    subprocess.Popen(command)

                    print(f"✅ Opening {keyword}")

                    return True

                except Exception as e:

                    print(e)

                    return False

        print("❌ Application not found")

        return False