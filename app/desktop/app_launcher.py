from __future__ import annotations

import json
import logging
import os
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from rapidfuzz import fuzz

from app.models.response import Response

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AppEntry:
    """
    Represents one launchable application.
    """

    name: str
    path: str
    source: str = "unknown"
    aliases: list[str] | None = None

    def __post_init__(self) -> None:

        if self.aliases is None:
            self.aliases = []

    def score(
        self,
        query: str,
    ) -> float:
        """
        Hybrid fuzzy score.
        """

        query = query.lower().strip()

        best = fuzz.ratio(
            query,
            self.name.lower(),
        )

        best = max(
            best,
            fuzz.partial_ratio(
                query,
                self.name.lower(),
            ),
        )

        best = max(
            best,
            fuzz.token_sort_ratio(
                query,
                self.name.lower(),
            ),
        )

        for alias in self.aliases:

            alias = alias.lower()

            best = max(
                best,
                fuzz.ratio(
                    query,
                    alias,
                ),
            )

            best = max(
                best,
                fuzz.partial_ratio(
                    query,
                    alias,
                ),
            )

        return best / 100.0


class AppLauncher:
    """
    Intelligent Windows application launcher.
    """

    CACHE_FILE = Path(
        "assets/cache/apps_cache.json"
    )

    CONFIG_FILE = Path(
        "assets/config/apps.json"
    )

    SCORE_THRESHOLD = 0.90

    BUILTIN_APPS = {

        "calculator": "calc",
        "calc": "calc",

        "notepad": "notepad",

        "paint": "mspaint",

        "wordpad": "write",

        "cmd": "cmd",

        "command prompt": "cmd",

        "powershell": "powershell",

        "terminal": "wt",

        "windows terminal": "wt",

        "explorer": "explorer",

        "file explorer": "explorer",

        "task manager": "taskmgr",

        "registry editor": "regedit",

        "regedit": "regedit",

        "control panel": "control",

        "control": "control",

        "cp": "control",

        "cpc": "control",

        "settings": "ms-settings:",

        "device manager": "devmgmt.msc",

        "disk management": "diskmgmt.msc",

        "services": "services.msc",

        "event viewer": "eventvwr",

        "task scheduler": "taskschd.msc",

        "snipping tool": "snippingtool",

        "camera": "microsoft.windows.camera:",

        "photos": "ms-photos:",

        "magnifier": "magnify",

        "on screen keyboard": "osk",

        "remote desktop": "mstsc",

        "system information": "msinfo32",

        "resource monitor": "resmon",

        "performance monitor": "perfmon",

        "dxdiag": "dxdiag",

        "disk cleanup": "cleanmgr",

    }

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Initializing AppLauncher..."
        )

        self.apps: dict[
            str,
            AppEntry,
        ] = {}

        self.start_menu_locations = [

            Path(
                r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
            ),

            Path(
                os.path.expandvars(
                    r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"
                )
            ),

        ]

        self.desktop_locations = [

            Path.home() / "Desktop",

            Path(
                os.path.expandvars(
                    r"%PUBLIC%\Desktop"
                )
            ),

        ]

        self.program_locations = [

            Path(
                r"C:\Program Files"
            ),

            Path(
                r"C:\Program Files (x86)"
            ),

        ]

        self._load()

    # =====================================================
    # Loading
    # =====================================================

    def _load(
        self,
    ) -> None:

        self.apps.clear()

        #
        # Load cache first
        #

        if self.CACHE_FILE.exists():

            try:

                with open(
                    self.CACHE_FILE,
                    "r",
                    encoding="utf-8",
                ) as file:

                    cached = json.load(
                        file
                    )

                for item in cached:

                    name = item.get(
                        "name"
                    )

                    path = item.get(
                        "path"
                    )

                    if not name or not path:
                        continue

                    self.apps[
                        name.lower()
                    ] = AppEntry(

                        name=name,

                        path=path,

                        source=item.get(
                            "source",
                            "cache",
                        ),

                        aliases=item.get(
                            "aliases",
                            [],
                        ),

                    )

            except Exception:

                logger.exception(
                    "Unable to load apps cache."
                )
    
            #
        # Load user configuration
        # (Overrides cached entries)
        #

        if self.CONFIG_FILE.exists():

            try:

                with open(
                    self.CONFIG_FILE,
                    "r",
                    encoding="utf-8",
                ) as file:

                    config = json.load(
                        file
                    )

                for item in config:

                    name = item.get(
                        "name"
                    )

                    path = item.get(
                        "path"
                    )

                    if not name or not path:
                        continue

                    self.apps[
                        name.lower()
                    ] = AppEntry(

                        name=name,

                        path=path,

                        source="config",

                        aliases=item.get(
                            "aliases",
                            [],
                        ),

                    )

            except Exception:

                logger.exception(
                    "Unable to load configured applications."
                )

        #
        # First run
        #

        if not self.apps:

            self.refresh()

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> None:

        logger.info(
            "Refreshing application index..."
        )

        found: dict[
            str,
            AppEntry,
        ] = {}

        #
        # Start Menu
        #

        for directory in self.start_menu_locations:

            if not directory.exists():
                continue

            try:

                for root, _, files in os.walk(directory):

                    for file in files:

                        name, ext = os.path.splitext(
                            file
                        )

                        if ext.lower() not in (
                            ".lnk",
                            ".exe",
                            ".url",
                        ):
                            continue

                        entry = AppEntry(

                            name=name,

                            path=os.path.join(
                                root,
                                file,
                            ),

                            source="start_menu",

                        )

                        found[
                            name.lower()
                        ] = entry

            except Exception:

                logger.exception(
                    "Unable to scan %s",
                    directory,
                )

        #
        # Desktop
        #

        for directory in self.desktop_locations:

            if not directory.exists():
                continue

            try:

                for root, _, files in os.walk(directory):

                    for file in files:

                        name, ext = os.path.splitext(
                            file
                        )

                        if ext.lower() not in (
                            ".lnk",
                            ".exe",
                            ".url",
                        ):
                            continue

                        found[
                            name.lower()
                        ] = AppEntry(

                            name=name,

                            path=os.path.join(
                                root,
                                file,
                            ),

                            source="desktop",

                        )

            except Exception:

                logger.exception(
                    "Unable to scan %s",
                    directory,
                )

        #
        # Program Files
        #

        for directory in self.program_locations:

            if not directory.exists():
                continue

            try:

                for root, _, files in os.walk(directory):

                    for file in files:

                        if not file.lower().endswith(
                            ".exe"
                        ):
                            continue

                        name = os.path.splitext(
                            file
                        )[0]

                        found[
                            name.lower()
                        ] = AppEntry(

                            name=name,

                            path=os.path.join(
                                root,
                                file,
                            ),

                            source="program_files",

                        )

            except Exception:

                logger.exception(
                    "Unable to scan %s",
                    directory,
                )

        self.apps = found

        try:

            self.CACHE_FILE.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                self.CACHE_FILE,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(

                    [
                        asdict(app)
                        for app in self.apps.values()
                    ],

                    file,

                    indent=4,

                )

        except Exception:

            logger.exception(
                "Unable to save application cache."
            )
    
        # =====================================================
    # Search
    # =====================================================

    def find_best_match(
        self,
        query: str,
    ) -> AppEntry | None:

        query = query.strip().lower()

        if not query:
            return None

        best_entry: AppEntry | None = None
        best_score = 0.0

        for entry in self.apps.values():

            score = entry.score(query)

            #
            # Exact match shortcut
            #

            if entry.name.lower() == query:

                return entry

            if score > best_score:

                best_score = score
                best_entry = entry

        if best_score >= self.SCORE_THRESHOLD:

            logger.info(
                "Matched '%s' -> '%s' (%.2f)",
                query,
                best_entry.name,
                best_score,
            )

            return best_entry

        logger.info(
            "No application matched '%s'",
            query,
        )

        return None

    # =====================================================
    # Public API
    # =====================================================

    def open(
        self,
        query: str,
    ) -> Response:

        query = query.strip().lower()

        if not query:

            return Response(
                success=False,
                message="No application specified.",
            )

        #
        # Built-in Windows applications
        #

        if query in self.BUILTIN_APPS:

            target = self.BUILTIN_APPS[query]

            try:

                #
                # URI based launchers
                #

                if (
                    target.startswith("ms-")
                    or target.endswith(":")
                ):

                    os.startfile(target)

                else:

                    subprocess.Popen(
                        target,
                        shell=True,
                    )

                return Response(

                    success=True,

                    message=f"Opened {query}.",

                    data=query,

                )

            except Exception:

                logger.exception(
                    "Unable to launch built-in app."
                )

                return Response(

                    success=False,

                    message=f"Failed to launch {query}.",

                )

        #
        # Installed applications
        #

        app = self.find_best_match(
            query
        )

        if app is None:

            return Response(

                success=False,

                message=f"No application found for '{query}'.",

            )

        try:

            if hasattr(
                os,
                "startfile",
            ):

                os.startfile(
                    app.path
                )

            else:

                subprocess.Popen(
                    [app.path]
                )

            logger.info(
                "Launched %s",
                app.name,
            )

            return Response(

                success=True,

                message=f"Opened {app.name}.",

                data=app.path,

            )

        except Exception:

            logger.exception(
                "Unable to launch %s",
                app.path,
            )

            return Response(

                success=False,

                message=f"Failed to launch {app.name}.",

            )

    # =====================================================
    # Compatibility API
    # =====================================================

    def all(
        self,
    ) -> list[AppEntry]:

        return list(
            self.apps.values()
        )

    def exists(
        self,
        query: str,
    ) -> bool:

        return (
            self.find_best_match(
                query
            )
            is not None
        )

    def launch(
        self,
        query: str,
    ) -> bool:
        """
        Backward compatibility for
        older DesktopEngine versions.
        """

        return self.open(
            query
        ).success

    def __len__(
        self,
    ) -> int:

        return len(
            self.apps
        )
    
        # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:

        return {

            "applications":
                len(self.apps),

            "cache":
                str(self.CACHE_FILE),

            "config":
                str(self.CONFIG_FILE),

            "threshold":
                self.SCORE_THRESHOLD,

        }

    # =====================================================
    # Cleanup
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "AppLauncher shutdown."
        )

    # =====================================================
    # Representation
    # =====================================================

    def __iter__(
        self,
    ):

        return iter(
            self.apps.values()
        )

    def __contains__(
        self,
        item: str,
    ) -> bool:

        return self.exists(
            item
        )

    def __repr__(
        self,
    ) -> str:

        return (

            "AppLauncher("

            f"apps={len(self.apps)}, "

            f"threshold={self.SCORE_THRESHOLD}"

            ")"

        )