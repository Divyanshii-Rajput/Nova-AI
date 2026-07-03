import re
import string


class TextCleaner:
    """
    Cleans Whisper output before NLP processing.
    """

    def clean(self, text: str) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        text = re.sub(r"\s+", " ", text)

        return text