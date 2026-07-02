from urllib.parse import quote_plus
from app.browser.browser_engine import BrowserEngine


class YouTubePlayer:

    def __init__(self):

        self.browser = BrowserEngine()

        self.page = self.browser.get_page()

    def play(self, song: str):

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(song)
        )

        self.page.goto(url)

        self.page.wait_for_timeout(3000)

        videos = self.page.locator("a#video-title")

        if videos.count() == 0:

            print("No video found.")

            return False

        videos.first.click()

        print(f"🎵 Playing {song}")

        return True