import re
import string


class TextCleaner:
    """
    Cleans Whisper output before intent detection.
    """

    def clean(self, text: str) -> str:

        if not text:
            return ""

        text = text.lower()

        text = text.translate(
            str.maketrans("", "", string.punctuation)
        )

        text = re.sub(r"\s+", " ", text)

        return text.strip()