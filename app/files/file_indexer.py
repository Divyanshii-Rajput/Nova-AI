import json
import os
from pathlib import Path


class FileIndexer:
    """
    Builds an in-memory searchable file index.
    """

    # Only useful document/media types
    ALLOWED_EXTENSIONS = {

        ".pdf",

        ".doc",

        ".docx",

        ".ppt",

        ".pptx",

        ".xls",

        ".xlsx",

        ".txt",

        ".csv",

        ".jpg",

        ".jpeg",

        ".png",

        ".mp3",

        ".mp4",

        ".zip"

    }

    # Ignore these folders completely
    SKIP_FOLDERS = {

        ".git",

        "node_modules",

        "__pycache__",

        "venv",

        ".venv",

        "AppData",

        "Program Files",

        "Program Files (x86)",

        "Windows"

    }

    def __init__(self):

        self.index = []

        config = Path("config/folders.json")

        with open(config, "r") as f:

            self.folders = json.load(f)

    def build_index(self):

        self.index.clear()

        print("\n📂 Building Smart File Index...\n")

        total = 0

        for folder in self.folders.values():

            folder = os.path.expandvars(folder)

            if not os.path.exists(folder):
                continue

            for root, dirs, files in os.walk(folder):

                # Skip unwanted folders
                dirs[:] = [

                    d

                    for d in dirs

                    if d not in self.SKIP_FOLDERS

                ]

                for file in files:

                    extension = Path(file).suffix.lower()

                    if extension not in self.ALLOWED_EXTENSIONS:
                        continue

                    self.index.append({

                        "name": file.lower(),

                        "stem": Path(file).stem.lower(),

                        "extension": extension,

                        "path": os.path.join(root, file)

                    })

                    total += 1

        print(f"✅ Indexed {total} useful files.\n")

    def get_index(self):

        return self.index