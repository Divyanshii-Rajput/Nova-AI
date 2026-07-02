import webbrowser


class WebsiteLauncher:
    """
    Opens websites.
    """

    WEBSITES = {

        "youtube": "https://www.youtube.com",

        "spotify": "https://open.spotify.com",

        "gmail": "https://mail.google.com",

        "github": "https://github.com",

        "linkedin": "https://linkedin.com",

        "leetcode": "https://leetcode.com",

        "chatgpt": "https://chat.openai.com",

        "geeksforgeeks": "https://www.geeksforgeeks.org"

    }

    def open_website(self, text: str):

        text = text.lower()

        for website, url in self.WEBSITES.items():

            if website in text:

                webbrowser.open(url)

                print(f"🌍 Opening {website.title()}")

                return True

        return False