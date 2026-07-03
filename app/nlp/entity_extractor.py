class EntityExtractor:
    """
    Extracts useful entity from a command.
    """

    REMOVE_WORDS = {

        "open",
        "launch",
        "start",

        "play",
        "music",
        "song",

        "search",
        "google",

        "please",

        "show",

        "find",

        "the",

        "a",

        "an",

        "to",

        "for",

        "on",

        "in"

    }

    def extract(self, text: str) -> str:

        words = []

        for word in text.split():

            if word not in self.REMOVE_WORDS:

                words.append(word)

        return " ".join(words)