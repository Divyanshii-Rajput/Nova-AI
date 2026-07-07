from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from rapidfuzz import fuzz

from app.files.file_indexer import (
    FileEntry,
    FileIndexer,
)


logger = logging.getLogger(__name__)


class FileSearch:
    """
    Intelligent File Search Engine.

    Ranking Priority

    1. Exact filename
    2. Starts With
    3. Contains
    4. Fuzzy
    5. Recently Modified
    """

    EXACT_SCORE = 100

    PREFIX_SCORE = 90

    CONTAINS_SCORE = 75

    FUZZY_THRESHOLD = 80

    RECENT_BONUS = 5

    MAX_RESULTS = 20

    def __init__(self):

        self.indexer = FileIndexer()

        self.indexer.initialize()

    # -------------------------------------------------
    # Public Search
    # -------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = MAX_RESULTS,
    ) -> List[FileEntry]:

        query = query.strip().lower()

        if not query:

            return []

        logger.info(

            "Searching '%s'",

            query,

        )

        ranked = self.rank(query)

        return [

            item[1]

            for item in ranked[:limit]

        ]

    # -------------------------------------------------
    # Ranking
    # -------------------------------------------------

    def rank(
        self,
        query: str,
    ):

        ranked = []

        for file in self.indexer:

            score = self.score(

                query,

                file,

            )

            if score <= 0:

                continue

            ranked.append(

                (

                    score,

                    file,

                )

            )

        ranked.sort(

            reverse=True,

            key=lambda x: (

                x[0],

                x[1].modified,

            ),

        )

        return ranked

    # -------------------------------------------------
    # Score
    # -------------------------------------------------

    def score(
        self,
        query: str,
        file: FileEntry,
    ) -> int:

        filename = file.name.lower()

        stem = Path(filename).stem

        score = 0

        # -------------------------
        # Exact
        # -------------------------

        if filename == query:

            return self.EXACT_SCORE

        if stem == query:

            return self.EXACT_SCORE

        # -------------------------
        # Prefix
        # -------------------------

        if filename.startswith(query):

            score = max(

                score,

                self.PREFIX_SCORE,

            )

        # -------------------------
        # Contains
        # -------------------------

        if query in filename:

            score = max(

                score,

                self.CONTAINS_SCORE,

            )

        # -------------------------
        # Fuzzy
        # -------------------------

        fuzzy = fuzz.partial_ratio(

            query,

            filename,

        )

        if fuzzy >= self.FUZZY_THRESHOLD:

            score = max(

                score,

                fuzzy,

            )

        # -------------------------
        # Recent Bonus
        # -------------------------

        if score:

            score += self.RECENT_BONUS

        return score
    
        # -------------------------------------------------
    # Top Result
    # -------------------------------------------------

    def best_match(
        self,
        query: str,
    ) -> FileEntry | None:

        results = self.search(query, 1)

        if not results:

            return None

        return results[0]

    # -------------------------------------------------
    # Search By Extension
    # -------------------------------------------------

    def search_extension(
        self,
        extension: str,
        limit: int = MAX_RESULTS,
    ) -> List[FileEntry]:

        files = self.indexer.filter_extension(extension)

        files.sort(

            key=lambda x: x.modified,

            reverse=True,

        )

        return files[:limit]

    # -------------------------------------------------
    # Folder Priority
    # -------------------------------------------------

    def folder_bonus(
        self,
        directory: str,
    ) -> int:

        directory = directory.lower()

        if "documents" in directory:
            return 12

        if "desktop" in directory:
            return 10

        if "downloads" in directory:
            return 8

        if "pictures" in directory:
            return 6

        if "videos" in directory:
            return 5

        return 0

    # -------------------------------------------------
    # Extension Bonus
    # -------------------------------------------------

    def extension_bonus(
        self,
        extension: str,
    ) -> int:

        extension = extension.lower()

        bonuses = {

            ".pdf": 12,

            ".docx": 10,

            ".pptx": 9,

            ".xlsx": 8,

            ".txt": 6,

            ".py": 6,

            ".cpp": 6,

            ".java": 6,

            ".ipynb": 5,

            ".jpg": 4,

            ".png": 4,

        }

        return bonuses.get(

            extension,

            0,

        )

    # -------------------------------------------------
    # Score Update
    # -------------------------------------------------

    def score(
        self,
        query: str,
        file: FileEntry,
    ) -> int:

        filename = file.name.lower()

        stem = Path(filename).stem

        score = 0

        # Exact

        if filename == query:

            return 1000

        if stem == query:

            return 980

        # Starts With

        if filename.startswith(query):

            score = max(score, 900)

        # Contains

        elif query in filename:

            score = max(score, 750)

        # Fuzzy

        fuzzy = fuzz.partial_ratio(

            query,

            filename,

        )

        if fuzzy >= self.FUZZY_THRESHOLD:

            # Ignore weak fuzzy matches
            if fuzzy < 85 and query not in filename:
                return 0

            score = max(
                score,
                fuzzy * 7,
            )

        if score == 0:

            return 0

        score += self.folder_bonus(

            file.directory,

        )

        score += self.extension_bonus(

            file.extension,

        )

        score += self.RECENT_BONUS

        return score
    
        # -------------------------------------------------
    # Confidence
    # -------------------------------------------------

    def confidence(
        self,
        query: str,
    ) -> float:
        """
        Returns confidence (0-100)
        of the best search result.
        """

        ranked = self.rank(query)

        if not ranked:
            return 0.0

        best_score = ranked[0][0]

        return min(
            round(best_score / 10, 2),
            100.0,
        )

    # -------------------------------------------------
    # Recent Documents
    # -------------------------------------------------

    def recent_documents(
        self,
        limit: int = 20,
    ) -> List[FileEntry]:

        docs = [

            file

            for file in self.indexer

            if file.extension in {

                ".pdf",

                ".doc",

                ".docx",

                ".ppt",

                ".pptx",

                ".xlsx",

                ".txt",

            }

        ]

        docs.sort(

            key=lambda x: x.modified,

            reverse=True,

        )

        return docs[:limit]

    # -------------------------------------------------
    # Duplicate Removal
    # -------------------------------------------------

    def unique_results(
        self,
        results: List[FileEntry],
    ) -> List[FileEntry]:

        seen = set()

        unique = []

        for file in results:

            key = (

                file.name.lower(),

                file.extension.lower(),

            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(file)

        return unique

    # -------------------------------------------------
    # Refresh
    # -------------------------------------------------

    def refresh(self):

        logger.info(
            "Refreshing search index..."
        )

        self.indexer.refresh()

    # -------------------------------------------------
    # Information
    # -------------------------------------------------

    def info(self):

        return {

            "indexed_files":

                len(self.indexer),

            "directories":

                self.indexer.directories(),

            "extensions":

                len(

                    self.indexer.extensions()

                ),

        }

    # -------------------------------------------------
    # Magic Methods
    # -------------------------------------------------

    def __len__(self):

        return len(self.indexer)

    def __iter__(self):

        return iter(self.indexer)

    # -------------------------------------------------
    # Debug
    # -------------------------------------------------

    def print_results(
        self,
        query: str,
        limit: int = 10,
    ):

        results = self.search(

            query,

            limit,

        )

        print("\nSearch Results\n")

        for i, file in enumerate(

            results,

            start=1,

        ):

            print(

                f"{i}. "

                f"{file.name}"

            )

            print(

                f"   {file.path}"

            )

            print()