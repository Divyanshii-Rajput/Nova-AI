import urllib.parse
import webbrowser


class GoogleSearch:
    """
    Opens a Google search in the default browser.
    """

    GOOGLE_URL = "https://www.google.com/search?q={}"

    def search(self, query: str) -> bool:

        query = query.strip()

        if not query:
            print("❌ Empty search query.")
            return False

        try:

            encoded_query = urllib.parse.quote_plus(query)

            url = self.GOOGLE_URL.format(encoded_query)

            webbrowser.open(url)

            print(f"🔍 Searching Google: {query}")

            return True

        except Exception as error:

            print(error)

            return False