import pyperclip


class ClipboardManager:
    """
    Read and write clipboard.
    """

    def copy(self, text: str):

        try:

            pyperclip.copy(text)

            print("📋 Copied to clipboard.")

            return True

        except Exception as error:

            print(error)

            return False

    def paste(self):

        try:

            text = pyperclip.paste()

            return text

        except Exception as error:

            print(error)

            return None

    def clear(self):

        try:

            pyperclip.copy("")

            print("🗑 Clipboard cleared.")

            return True

        except Exception as error:

            print(error)

            return False