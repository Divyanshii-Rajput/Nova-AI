import os
import platform
import subprocess
from pathlib import Path


class FileOpener:
    """
    Opens files using the operating system's
    default application.
    """

    def open(self, file_path: str) -> bool:

        if not file_path:
            print("❌ Empty file path.")
            return False

        path = Path(file_path)

        if not path.exists():

            print("❌ File does not exist.")

            return False

        try:

            system = platform.system()

            if system == "Windows":

                os.startfile(path)

            elif system == "Darwin":

                subprocess.Popen(["open", str(path)])

            else:

                subprocess.Popen(["xdg-open", str(path)])

            print(f"📄 Opening:\n{path}")

            return True

        except Exception as error:

            print(error)

            return False