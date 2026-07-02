from playwright.sync_api import sync_playwright


class BrowserEngine:
    """
    Singleton browser engine using Playwright.
    """

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

    def get_page(self):
        return self.page

    def close(self):
        self.browser.close()
        self.playwright.stop()