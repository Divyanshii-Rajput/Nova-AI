from __future__ import annotations

import re

from app.models.intent import Intent


class EntityExtractor:
    """
    Extracts the target entity from a normalized command.

    Pipeline
    --------
    Input
        ↓
    Normalize
        ↓
    Remove command prefix
        ↓
    Remove filler words
        ↓
    Remove generic leading words
        ↓
    Entity

    Examples
    --------
    "open calculator"
        -> "calculator"

    "open the vscode application"
        -> "vscode"

    "search binary search"
        -> "binary search"

    "play believer song"
        -> "believer"

    "visit github website"
        -> "github"

    "explain dynamic programming"
        -> "dynamic programming"
    """

    COMMAND_PREFIXES = {

        Intent.OPEN_APP: [
            "open",
            "launch",
            "start",
            "run",
        ],

        Intent.OPEN_FOLDER: [
            "open",
            "show",
        ],

        Intent.OPEN_FILE: [
            "open",
        ],

        Intent.OPEN_WEBSITE: [
            "open",
            "visit",
            "go to",
        ],

        Intent.SEARCH_WEB: [
            "search",
            "google",
            "find",
            "look up",
        ],

        Intent.PLAY_MUSIC: [
            "play",
            "listen to",
        ],

        Intent.AI_CHAT: [
            "explain",
            "tell me",
            "what is",
            "who is",
            "how to",
            "why",
        ],

        Intent.SYSTEM_CONTROL: [
            "increase",
            "decrease",
            "raise",
            "lower",
            "mute",
            "unmute",
            "shutdown",
            "restart",
            "sleep",
            "lock",
            "logout",
        ],

        Intent.TAKE_SCREENSHOT: [
            "take",
            "capture",
        ],

        Intent.EXIT: [
            "exit",
            "quit",
            "stop",
            "goodbye",
        ],
    }

    FILLER_WORDS = {
        "the",
        "a",
        "an",
        "please",
        "my",
        "for",
        "to",
        "of",
    }

    GENERIC_PREFIXES = (
        "song ",
        "music ",
        "website ",
        "site ",
        "webpage ",
        "page ",
        "app ",
        "application ",
        "folder ",
        "directory ",
        "file ",
        "document ",
    )

    POLITE_PHRASES = (
        "can you",
        "could you",
        "would you",
        "will you",
        "please",
        "kindly",
        "for me",
        "i want to",
        "i would like to",
        "can u",
    )

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize text before entity extraction.
        """

        if not text:
            return ""

        text = text.lower().strip()

        text = re.sub(
            r"[^\w\s]",
            " ",
            text,
        )

        for phrase in self.POLITE_PHRASES:
            text = text.replace(
                phrase,
                " ",
            )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def _remove_fillers(
        self,
        text: str,
    ) -> str:
        """
        Remove filler words while preserving order.
        """

        return " ".join(
            word
            for word in text.split()
            if word not in self.FILLER_WORDS
        )

    def _remove_prefix(
        self,
        text: str,
        intent: Intent,
    ) -> str:
        """
        Remove the command prefix for the detected intent.
        """

        prefixes = sorted(
            self.COMMAND_PREFIXES.get(intent, []),
            key=len,
            reverse=True,
        )

        for prefix in prefixes:

            if text.startswith(prefix + " "):
                return text[len(prefix):].strip()

            if text == prefix:
                return ""

        return text

    def _remove_generic_prefixes(
        self,
        text: str,
    ) -> str:
        """
        Remove generic words from the beginning of
        the extracted entity.
        """

        changed = True

        while changed:

            changed = False

            for prefix in self.GENERIC_PREFIXES:

                if text.startswith(prefix):
                    text = text[len(prefix):].strip()
                    changed = True

        return text

    def extract(
        self,
        text: str,
        intent: Intent,
    ) -> str:
        """
        Extract the entity from a normalized command.
        """

        text = self.normalize(text)

        if not text:
            return ""

        text = self._remove_prefix(
            text,
            intent,
        )

        text = self._remove_fillers(text)

        text = self._remove_generic_prefixes(text)

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    def extract_many(
        self,
        texts,
        intent: Intent,
    ):
        """
        Extract entities from multiple commands.
        """

        return [
            self.extract(
                text,
                intent,
            )
            for text in texts
        ]