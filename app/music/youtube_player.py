import time
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class YouTubePlayer:
    """
    Opens YouTube and plays the first search result.
    """

    def __init__(self):

        options = Options()

        options.add_experimental_option(
            "excludeSwitches",
            ["enable-logging"]
        )

        self.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

    def play(self, song: str):

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(song)
        )

        self.driver.get(url)

        time.sleep(3)

        videos = self.driver.find_elements(
            By.ID,
            "video-title"
        )

        if videos:

            videos[0].click()

            print(f"🎵 Playing {song}")

        else:

            print("No video found.")