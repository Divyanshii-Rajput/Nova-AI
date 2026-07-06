from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


logger = logging.getLogger(__name__)


@dataclass(slots=True)
class FileEntry:
    """
    Represents one indexed file.
    """

    name: str

    path: str

    extension: str

    size: int

    modified: float

    directory: str


class FileIndexer:
    """
    Production File Indexer.

    Features

    ✓ Multi-drive indexing

    ✓ Cache

    ✓ Incremental refresh

    ✓ Ignore Windows folders

    ✓ Fast loading

    ✓ Metadata
    """

    CACHE_FILE = Path(
        "assets/cache/file_index.json"
    )

    IGNORE_FOLDERS = {

        "$recycle.bin",

        "system volume information",

        "windows",

        "programdata",

        "appdata",

        "temp",

        "tmp",

        ".git",

        "__pycache__",

        "node_modules",

        ".venv",

        "venv",

    }

    def __init__(self):

        self.files: Dict[
            str,
            FileEntry,
        ] = {}

    # -------------------------------------------------
    # Startup
    # -------------------------------------------------

    def load(self):

        """
        Load existing cache.

        Returns

        -------

        bool

        True if cache exists.
        """

        if not self.CACHE_FILE.exists():

            return False

        try:

            with open(

                self.CACHE_FILE,

                "r",

                encoding="utf8",

            ) as file:

                data = json.load(file)

            self.files.clear()

            for item in data:

                entry = FileEntry(**item)

                self.files[
                    entry.path
                ] = entry

            logger.info(

                "Loaded %d indexed files.",

                len(self.files),

            )

            return True

        except Exception as e:

            logger.exception(e)

            return False

    # -------------------------------------------------

    def save(self):

        """
        Save cache.
        """

        self.CACHE_FILE.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with open(

            self.CACHE_FILE,

            "w",

            encoding="utf8",

        ) as file:

            json.dump(

                [

                    asdict(x)

                    for x in self.files.values()

                ],

                file,

                indent=2,

            )

    # -------------------------------------------------
    # Utilities
    # -------------------------------------------------

    @staticmethod
    def valid_folder(folder: str) -> bool:

        folder = folder.lower()

        return folder not in FileIndexer.IGNORE_FOLDERS

    @staticmethod
    def make_entry(path: Path):

        stat = path.stat()

        return FileEntry(

            name=path.name,

            path=str(path),

            extension=path.suffix.lower(),

            size=stat.st_size,

            modified=stat.st_mtime,

            directory=str(path.parent),

        )
    
        # -------------------------------------------------
    # Drives
    # -------------------------------------------------

    def available_drives(self) -> List[Path]:
        """
        Return all available Windows drives.

        Example:
            C:\
            D:\
            E:\
        """

        drives = []

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            drive = Path(f"{letter}:\\")

            if drive.exists():

                drives.append(drive)

        return drives

    # -------------------------------------------------
    # Index
    # -------------------------------------------------

    def build(self):

        """
        Build complete file index.
        """

        logger.info("Building file index...")

        self.files.clear()

        total = 0

        for drive in self.available_drives():

            logger.info(
                "Scanning drive %s",
                drive,
            )

            total += self._scan_drive(drive)

        logger.info(
            "Indexed %d files.",
            total,
        )

        self.save()

    # -------------------------------------------------

    def _scan_drive(
        self,
        drive: Path,
    ) -> int:

        indexed = 0

        for root, dirs, files in os.walk(
            drive,
            topdown=True,
        ):

            # -------------------------
            # Ignore folders
            # -------------------------

            dirs[:] = [

                d

                for d in dirs

                if self.valid_folder(d)

            ]

            root = Path(root)

            for file in files:

                try:

                    path = root / file

                    if not path.exists():

                        continue

                    entry = self.make_entry(path)

                    self.files[
                        entry.path
                    ] = entry

                    indexed += 1

                except (
                    PermissionError,
                    FileNotFoundError,
                    OSError,
                ):

                    continue

        return indexed

    # -------------------------------------------------
    # Incremental
    # -------------------------------------------------

    def refresh(self):

        """
        Refresh cache.

        Currently performs
        a full rebuild.
        """

        self.build()

    # -------------------------------------------------
    # Extensions
    # -------------------------------------------------

    def filter_extension(
        self,
        extension: str,
    ) -> List[FileEntry]:

        extension = extension.lower()

        if not extension.startswith("."):

            extension = "." + extension

        return [

            file

            for file in self.files.values()

            if file.extension == extension

        ]

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def count(self) -> int:

        return len(self.files)

    def directories(self) -> int:

        return len({

            file.directory

            for file in self.files.values()

        })

    def extensions(self):

        result = {}

        for file in self.files.values():

            result.setdefault(

                file.extension,

                0,

            )

            result[file.extension] += 1

        return result
    
        # -------------------------------------------------
    # Searching
    # -------------------------------------------------

    def search_by_name(
        self,
        filename: str,
    ) -> List[FileEntry]:
        """
        Exact filename search.
        """

        filename = filename.lower()

        return [

            file

            for file in self.files.values()

            if file.name.lower() == filename

        ]

    def search_contains(
        self,
        keyword: str,
    ) -> List[FileEntry]:
        """
        Search files containing keyword.
        """

        keyword = keyword.lower()

        return [

            file

            for file in self.files.values()

            if keyword in file.name.lower()

        ]

    # -------------------------------------------------
    # Recent Files
    # -------------------------------------------------

    def recent_files(
        self,
        limit: int = 20,
    ) -> List[FileEntry]:

        return sorted(

            self.files.values(),

            key=lambda x: x.modified,

            reverse=True,

        )[:limit]

    # -------------------------------------------------
    # Largest Files
    # -------------------------------------------------

    def largest_files(
        self,
        limit: int = 20,
    ) -> List[FileEntry]:

        return sorted(

            self.files.values(),

            key=lambda x: x.size,

            reverse=True,

        )[:limit]

    # -------------------------------------------------
    # Cleanup
    # -------------------------------------------------

    def remove_missing(self):

        """
        Remove deleted files from cache.
        """

        deleted = []

        for path in self.files:

            if not Path(path).exists():

                deleted.append(path)

        for path in deleted:

            del self.files[path]

        if deleted:

            logger.info(

                "Removed %d missing files.",

                len(deleted),

            )

            self.save()

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def values(self) -> List[FileEntry]:

        return list(self.files.values())

    def paths(self) -> List[str]:

        return list(self.files.keys())

    # -------------------------------------------------
    # Magic Methods
    # -------------------------------------------------

    def __len__(self):

        return len(self.files)

    def __contains__(
        self,
        filepath: str,
    ):

        return filepath in self.files

    def __iter__(self):

        return iter(self.files.values())

    # -------------------------------------------------
    # Build If Needed
    # -------------------------------------------------

    def initialize(self):
        """
        Load cache.
        Build cache if missing.
        """

        if not self.load():

            logger.info(
                "No cache found."
            )

            self.build()

    # -------------------------------------------------
    # Information
    # -------------------------------------------------

    def info(self):

        return {

            "files": len(self.files),

            "directories": self.directories(),

            "extensions": len(self.extensions()),

        }