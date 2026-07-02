from playwright.sync_api import sync_playwright


class BrowserManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.playwright = None
            cls._instance.browser = None
            cls._instance.context = None
            cls._instance.page = None

        return cls._instance

    def get_page(self):

        if self.browser is None:

            self.playwright = sync_playwright().start()

            self.browser = self.playwright.chromium.launch(
                headless=False
            )

            self.context = self.browser.new_context()

            self.page = self.context.new_page()

        return self.page

    def close(self):

        try:

            if self.browser:

                self.browser.close()

        except:
            pass

        try:

            if self.playwright:

                self.playwright.stop()

        except:
            pass

        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None