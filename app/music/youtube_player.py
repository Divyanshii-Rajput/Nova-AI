from urllib.parse import quote_plus

from app.browser.browser_manager import BrowserManager


class YouTubePlayer:

    def __init__(self):

        self.browser = BrowserManager()

    def play(self, song):

        page = self.browser.get_page()

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(song)
        )

        page.goto(url)

        page.wait_for_timeout(3000)

        videos = page.locator("a#video-title")

        if videos.count():

            videos.first.click()

            print(f"🎵 Playing {song}")

            return True

        print("Video not found.")

        return False