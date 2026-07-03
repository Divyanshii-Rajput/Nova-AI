import json
import os
from pathlib import Path


class FileIndexer:
    """
    Builds an in-memory index of files.
    """

    def __init__(self):

        self.index = []

        config = Path("config/folders.json")

        with open(config, "r") as f:

            self.folders = json.load(f)

    def build_index(self):

        self.index.clear()

        print("📂 Building file index...")

        total = 0

        for folder in self.folders.values():

            folder = os.path.expandvars(folder)

            if not os.path.exists(folder):
                continue

            for root, dirs, files in os.walk(folder):

                for file in files:

                    path = os.path.join(root, file)

                    self.index.append({

                        "name": file.lower(),

                        "path": path

                    })

                    total += 1

        print(f"✅ Indexed {total} files")

    def get_index(self):

        return self.index