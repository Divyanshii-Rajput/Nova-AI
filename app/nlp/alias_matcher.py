import re


class AliasMatcher:
    """
    Converts common Whisper mistakes into valid names.
    """

    ALIASES = {

        "lead code": "leetcode",
        "lead core": "leetcode",
        "lead course": "leetcode",
        "leet code": "leetcode",

        "chat gpt": "chatgpt",
        "chat g p t": "chatgpt",

        "g f g": "geeksforgeeks",
        "geeks for geeks": "geeksforgeeks",

        "you tube": "youtube",

        "calculate": "calculator",
        "calc": "calculator",

        "vs code": "vscode",

        "good bye": "goodbye",

    }

    def normalize(self, text: str) -> str:

        for alias, actual in self.ALIASES.items():

            pattern = r"\b" + re.escape(alias) + r"\b"

            text = re.sub(pattern, actual, text)

        return text