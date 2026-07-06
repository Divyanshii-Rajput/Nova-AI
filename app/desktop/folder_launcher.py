import json
import os
from pathlib import Path

from rapidfuzz import process


class FolderLauncher:
    """
    Opens Windows folders using aliases defined in config/folders.json.
    Supports both standard Windows folders and OneDrive redirected folders.
    """

    def __init__(self):

        self.folders = {}
        self.alias_map = {}

        self.load_folders()

    def load_folders(self):

        config_path = Path("config/folders.json")

        if not config_path.exists():
            print("⚠ folders.json not found.")
            return

        with open(config_path, "r", encoding="utf-8") as file:
            self.folders = json.load(file)

        self.alias_map.clear()

        for key, value in self.folders.items():

            self.alias_map[key.lower()] = key

            for alias in value.get("aliases", []):

                self.alias_map[alias.lower()] = key

    def get_best_match(self, folder_name: str):

        if not self.alias_map:
            return None

        result = process.extractOne(
            folder_name.lower(),
            self.alias_map.keys(),
            score_cutoff=60,
        )

        if result is None:
            return None

        return self.alias_map[result[0]]

    def resolve_special_folder(self, folder: str):

        home = Path.home()

        standard_locations = {
            "desktop": home / "Desktop",
            "downloads": home / "Downloads",
            "documents": home / "Documents",
            "pictures": home / "Pictures",
            "videos": home / "Videos",
            "music": home / "Music",
        }

        key = folder.lower()

        if key not in standard_locations:
            return None

        path = standard_locations[key]

        if path.exists():
            return path

        # OneDrive fallback
        one_drive_path = home / "OneDrive" / path.name

        if one_drive_path.exists():
            return one_drive_path

        return path

    def open(self, folder_name: str):

        folder_name = folder_name.strip().lower()

        match = self.get_best_match(folder_name)

        if match is None:
            print("❌ Folder not found.")
            return False

        folder_info = self.folders[match]

        configured_path = folder_info["path"]

        special_folder = self.resolve_special_folder(configured_path)

        if special_folder is not None:
            folder = special_folder
        else:
            folder = Path(os.path.expandvars(configured_path))

        if not folder.exists():
            print(f"❌ Folder does not exist:\n{folder}")
            return False

        try:

            os.startfile(folder)

            print(f"📂 Opening {match}")

            return True

        except Exception as error:

            print(f"❌ Failed to open folder: {match}")
            print(error)

            return False