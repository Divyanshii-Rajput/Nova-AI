class AliasMatcher:
    """
    Converts common speech variations into canonical words.
    """

    ALIASES = {

        # ChatGPT

        "chat gpt": "chatgpt",
        "chat g p t": "chatgpt",
        "chat gpd": "chatgpt",
        "chat g p d": "chatgpt",

        # LeetCode

        "lead code": "leetcode",
        "lead core": "leetcode",
        "lead course": "leetcode",
        "leet code": "leetcode",
        "gleat call": "leetcode",

        # GeeksforGeeks

        "geeks for geeks": "geeksforgeeks",
        "gfg": "geeksforgeeks",
        "g f g": "geeksforgeeks",

        # YouTube

        "you tube": "youtube",
        "u tube": "youtube",

        # Calculator

        "calculate": "calculator",
        "calc": "calculator",

        # Exit

        "good bye": "goodbye"
    }

    def normalize(self, text: str) -> str:

        for alias, original in self.ALIASES.items():

            text = text.replace(alias, original)

        return text