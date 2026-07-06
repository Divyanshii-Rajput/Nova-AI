from datetime import datetime
from pathlib import Path

import pyautogui


class Screenshot:

    def __init__(self):

        self.output = Path("screenshots")

        self.output.mkdir(exist_ok=True)

    def capture(self):

        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"

        path = self.output / filename

        image = pyautogui.screenshot()

        image.save(path)

        print(f"📸 Screenshot saved:\n{path}")

        return str(path)