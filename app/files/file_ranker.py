from pathlib import Path

from rapidfuzz import fuzz


class FileRanker:
    """
    Ranks files according to how well they match the user's query.
    """

    EXTENSION_BONUS = {
        ".pdf": 15,
        ".docx": 14,
        ".doc": 13,
        ".pptx": 12,
        ".ppt": 11,
        ".xlsx": 10,
        ".xls": 9,
        ".txt": 5,
    }

    def score(self, query: str, file_path: str) -> int:

        query = query.lower().strip()

        filename = Path(file_path).stem.lower()

        extension = Path(file_path).suffix.lower()

        score = fuzz.token_sort_ratio(query, filename)

        if filename == query:
            score += 100

        elif filename.startswith(query):
            score += 40

        elif query in filename:
            score += 20

        score += self.EXTENSION_BONUS.get(extension, 0)

        return score

    def best_match(self, query: str, files: list[str]):

        if not files:
            return None

        ranked = []

        for file in files:

            ranked.append(
                (
                    self.score(query, file),
                    file,
                )
            )

        ranked.sort(reverse=True)

        return ranked[0][1]