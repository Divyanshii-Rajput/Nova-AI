from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Iterator

from app.files.file_search import FileSearch
from app.files.file_indexer import FileEntry
from app.models.response import Response

logger = logging.getLogger(__name__)


class FileEngine:
    """
    High-level file engine.

    Responsibilities
    ----------------
    • Search indexed files
    • Open files
    • Return Response objects
    • Refresh index

    This class never performs indexing itself.
    """

    DEFAULT_LIMIT = 10

    CONFIDENCE_THRESHOLD = 70

    def __init__(self) -> None:

        logger.info(
            "Initializing FileEngine..."
        )

        self.search_engine = FileSearch()

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _success(
        message: str,
        data=None,
    ) -> Response:

        return Response(
            success=True,
            message=message,
            data=data,
        )

    @staticmethod
    def _failure(
        message: str,
    ) -> Response:

        return Response(
            success=False,
            message=message,
        )

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> list[FileEntry]:

        if not query:

            return []

        logger.info(
            "Searching files: %s",
            query,
        )

        try:

            return self.search_engine.search(
                query.strip(),
                limit,
            )

        except Exception:

            logger.exception(
                "File search failed."
            )

            return []

    # =====================================================
    # Best Match
    # =====================================================

    def best_match(
        self,
        query: str,
    ) -> FileEntry | None:

        if not query:

            return None

        try:

            return self.search_engine.best_match(
                query.strip(),
            )

        except Exception:

            logger.exception(
                "Best-match search failed."
            )

            return None

    # =====================================================
    # Open
    # =====================================================

    def open(
        self,
        query: str,
    ) -> Response:

        if query is None:

            return self._failure(
                "No file specified."
            )

        query = query.strip()

        if not query:

            return self._failure(
                "No file specified."
            )

        logger.info(
            "Opening file: %s",
            query,
        )

        try:

            confidence = self.search_engine.confidence(
                query,
            )

        except Exception:

            logger.exception(
                "Confidence calculation failed."
            )

            return self._failure(
                "Unable to search files."
            )

        logger.info(
            "Search confidence: %s",
            confidence,
        )

        if confidence < self.CONFIDENCE_THRESHOLD:

            return self._failure(
                f"No confident match found for '{query}'."
            )

        file = self.best_match(query)

        if file is None:

            return self._failure(
                f"No file found for '{query}'."
            )

        return self._open_file(file)

    # =====================================================
    # Open File
    # =====================================================

    def _open_file(
        self,
        file: FileEntry,
    ) -> Response:

        try:

            path = Path(file.path)

            if not path.exists():

                logger.warning(
                    "Missing file: %s",
                    path,
                )

                return self._failure(
                    "File no longer exists."
                )

            os.startfile(str(path))

            logger.info(
                "Opened file: %s",
                path,
            )

            return self._success(
                f"Opened '{file.name}'.",
                file,
            )

        except Exception:

            logger.exception(
                "Unable to open file."
            )

            return self._failure(
                "Unable to open file."
            )
    
        # =====================================================
    # Open Multiple
    # =====================================================

    def open_multiple(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Response]:
        """
        Open the first N matching files.
        """

        if not query:
            return []

        responses: list[Response] = []

        try:

            results = self.search(
                query,
                limit,
            )

            logger.info(
                "Opening %d matching files.",
                len(results),
            )

            for file in results:

                responses.append(
                    self._open_file(file)
                )

        except Exception:

            logger.exception(
                "Failed while opening multiple files."
            )

            responses.append(
                self._failure(
                    "Unable to open matching files."
                )
            )

        return responses

    # =====================================================
    # Recent Documents
    # =====================================================

    def recent_documents(
        self,
        limit: int = DEFAULT_LIMIT,
    ) -> list[FileEntry]:

        try:

            return self.search_engine.recent_documents(
                limit,
            )

        except Exception:

            logger.exception(
                "Unable to fetch recent documents."
            )

            return []

    # =====================================================
    # Extension Search
    # =====================================================

    def search_extension(
        self,
        extension: str,
        limit: int = 20,
    ) -> list[FileEntry]:

        if not extension:
            return []

        extension = extension.strip().lower()

        if not extension.startswith("."):
            extension = "." + extension

        try:

            return self.search_engine.search_extension(
                extension,
                limit,
            )

        except Exception:

            logger.exception(
                "Extension search failed."
            )

            return []

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> Response:

        logger.info(
            "Refreshing file index..."
        )

        try:

            self.search_engine.refresh()

            logger.info(
                "File index refreshed successfully."
            )

            return self._success(
                "File index refreshed."
            )

        except Exception:

            logger.exception(
                "Failed to refresh file index."
            )

            return self._failure(
                "Unable to refresh file index."
            )

    # =====================================================
    # Information
    # =====================================================

    def info(
        self,
    ) -> dict:

        try:

            return self.search_engine.info()

        except Exception:

            logger.exception(
                "Unable to retrieve file index information."
            )

            return {}

    # =====================================================
    # Utilities
    # =====================================================

    def exists(
        self,
        query: str,
    ) -> bool:

        if not query:
            return False

        return self.best_match(query) is not None

    def count(
        self,
    ) -> int:

        try:

            return len(self.search_engine)

        except Exception:

            logger.exception(
                "Unable to count indexed files."
            )

            return 0

    def __len__(
        self,
    ) -> int:

        return self.count()

    def __iter__(
        self,
    ) -> Iterator[FileEntry]:

        try:

            return iter(self.search_engine)

        except Exception:

            logger.exception(
                "Unable to iterate over file index."
            )

            return iter(())

    # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:

        return {

            "indexed_files":
                self.count(),

            "confidence_threshold":
                self.CONFIDENCE_THRESHOLD,

            "search_engine":
                type(self.search_engine).__name__,

        }

    # =====================================================
    # Cleanup
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "FileEngine shutdown."
        )