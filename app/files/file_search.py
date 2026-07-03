from rapidfuzz import fuzz

from app.files.file_indexer import FileIndexer


class FileSearcher:

    def __init__(self):

        self.indexer = FileIndexer()

        self.indexer.build_index()

    def search(self, text):

        text = text.lower()

        remove_words = [

            "open",

            "file",

            "document",

            "notes",

            "report",

            "resume",

            "folder"

        ]

        for word in remove_words:

            text = text.replace(word, "")

        query = text.strip()

        best_score = 0

        best_match = None

        for file in self.indexer.get_index():

            score = fuzz.partial_ratio(

                query,

                file["name"]

            )

            if score > best_score:

                best_score = score

                best_match = file

        if best_score < 70:

            return None

        return best_match["path"]