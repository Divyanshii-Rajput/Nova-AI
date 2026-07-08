from __future__ import annotations

import logging
import re
from typing import Dict, List, Pattern, Tuple

logger = logging.getLogger(__name__)


class AliasMatcher:
    """
    Corrects common Whisper/STT recognition mistakes.

    Pipeline
    --------
    TextCleaner
        ↓
    AliasMatcher
        ↓
    IntentDetector

    The matcher uses compiled regular expressions and
    replaces longer aliases before shorter ones to avoid
    partial replacements.
    """

    ALIASES: Dict[str, str] = {

        # --------------------------------
        # ChatGPT
        # --------------------------------

        "chat gpt": "chatgpt",
        "chat g p t": "chatgpt",
        "char gpt": "chatgpt",
        "char g p t": "chatgpt",
        "chat gpd": "chatgpt",
        "gpt chat": "chatgpt",
        "g p t": "chatgpt",

        # --------------------------------
        # Gemini
        # --------------------------------

        "google gemini": "gemini",

        # --------------------------------
        # VS Code
        # --------------------------------

        "vs code": "vscode",
        "visual studio code": "vscode",
        "visual studio": "vscode",
        "v s code": "vscode",

        # --------------------------------
        # LeetCode
        # --------------------------------

        "leet code": "leetcode",
        "lead code": "leetcode",
        "lead core": "leetcode",
        "lead course": "leetcode",
        "fleet code": "leetcode",

        # --------------------------------
        # GeeksForGeeks
        # --------------------------------

        "g f g": "geeksforgeeks",
        "geeks for geeks": "geeksforgeeks",

        # --------------------------------
        # Browser
        # --------------------------------

        "you tube": "youtube",

        # --------------------------------
        # Calculator
        # --------------------------------

        "calculate": "calculator",
        "calc": "calculator",

        # --------------------------------
        # DBMS
        # --------------------------------

        "db ms": "dbms",
        "d b m s": "dbms",
        "dvms": "dbms",
        "dpms": "dbms",

        # --------------------------------
        # Goodbye
        # --------------------------------

        "good bye": "goodbye",
    }

    def __init__(self) -> None:

        self._compiled: List[
            Tuple[Pattern[str], str]
        ] = []

        self._compile_patterns()

    # -------------------------------------------------
    # Compile
    # -------------------------------------------------

    def _compile_patterns(self) -> None:
        """
        Compile aliases.

        Longest aliases are compiled first so that
        'visual studio code' is matched before
        'visual studio'.
        """

        self._compiled.clear()

        aliases = sorted(
            self.ALIASES.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

        for alias, replacement in aliases:

            pattern = re.compile(
                rf"\b{re.escape(alias)}\b",
                flags=re.IGNORECASE,
            )

            self._compiled.append(
                (
                    pattern,
                    replacement,
                )
            )

    # -------------------------------------------------
    # Normalize
    # -------------------------------------------------

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Replace all registered aliases.
        """

        if not text:
            return ""

        normalized = text.strip()

        for pattern, replacement in self._compiled:

            normalized = pattern.sub(
                replacement,
                normalized,
            )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized.strip()

    # -------------------------------------------------
    # Backward Compatibility
    # -------------------------------------------------

    def replace(
        self,
        text: str,
    ) -> str:
        """
        Older API kept for compatibility.
        """

        return self.normalize(text)

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    def register(
        self,
        alias: str,
        actual: str,
    ) -> None:
        """
        Register a runtime alias.
        """

        alias = alias.lower().strip()
        actual = actual.lower().strip()

        if not alias or not actual:
            return

        previous = self.ALIASES.get(alias)

        self.ALIASES[alias] = actual

        self._compile_patterns()

        if previous is None:

            logger.info(
                "Registered alias '%s' -> '%s'",
                alias,
                actual,
            )

        elif previous != actual:

            logger.info(
                "Updated alias '%s' : '%s' -> '%s'",
                alias,
                previous,
                actual,
            )

    # -------------------------------------------------
    # Remove
    # -------------------------------------------------

    def unregister(
        self,
        alias: str,
    ) -> bool:
        """
        Remove an alias.
        """

        alias = alias.lower().strip()

        if alias not in self.ALIASES:
            return False

        del self.ALIASES[alias]

        self._compile_patterns()

        return True

    # -------------------------------------------------
    # Queries
    # -------------------------------------------------

    def exists(
        self,
        alias: str,
    ) -> bool:

        return alias.lower().strip() in self.ALIASES

    def resolve(
        self,
        alias: str,
    ) -> str:

        alias = alias.lower().strip()

        return self.ALIASES.get(
            alias,
            alias,
        )

    def aliases(self) -> Dict[str, str]:

        return dict(self.ALIASES)

    def count(self) -> int:

        return len(self.ALIASES)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def stats(self) -> dict:

        return {
            "aliases": len(self.ALIASES),
            "compiled_patterns": len(self._compiled),
        }

    # -------------------------------------------------
    # Debug
    # -------------------------------------------------

    def debug(
        self,
        text: str,
    ) -> None:

        print()
        print("=" * 60)
        print("Original   :", text)
        print("Normalized :", self.normalize(text))
        print("Aliases    :", self.count())
        print("=" * 60)
        print()