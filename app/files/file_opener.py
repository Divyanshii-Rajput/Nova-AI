import os


class FileOpener:

    def open(self, path):

        if path is None:

            print("❌ File not found.")

            return False

        os.startfile(path)

        print(f"📂 Opened:\n{path}")

        return True