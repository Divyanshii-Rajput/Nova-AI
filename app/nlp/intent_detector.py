from __future__ import annotations

import logging
import re
from typing import Dict

from app.models.intent import Intent

logger = logging.getLogger(__name__)


class IntentDetector:
    """
    Rule-based intent detector.

    The detector assigns weighted scores to every intent.
    The intent with the highest score is selected.

    Pipeline
    --------
    Normalized Text
            ↓
       Rule Matching
            ↓
      Score Aggregation
            ↓
      Highest Score Wins
            ↓
         Confidence
    """

    INTENT_RULES: Dict[Intent, Dict[str, int]] = {

        Intent.OPEN_APP: {
            "open": 10,
            "launch": 10,
            "start": 9,
            "run": 9,
        },

        Intent.OPEN_FILE: {
            "file": 10,
            "document": 10,
            "pdf": 10,
            "resume": 9,
            "assignment": 9,
            "report": 9,
            "notes": 8,
        },

        Intent.OPEN_FOLDER: {
            "folder": 10,
            "directory": 9,
        },

        Intent.OPEN_WEBSITE: {
            "website": 10,
            "visit": 10,
            "go to": 9,
        },

        Intent.SEARCH_WEB: {
            "search": 10,
            "google": 10,
            "find": 8,
            "look up": 9,
        },

        Intent.PLAY_MUSIC: {
            "play": 10,
            "music": 9,
            "song": 9,
            "listen": 8,
        },

        Intent.SYSTEM_CONTROL: {
            "volume": 10,
            "brightness": 10,
            "shutdown": 10,
            "restart": 10,
            "sleep": 10,
            "lock": 10,
            "mute": 10,
            "unmute": 10,
        },

        Intent.TAKE_SCREENSHOT: {
            "screenshot": 10,
            "screen shot": 10,
            "capture": 8,
        },

        Intent.EXIT: {
            "exit": 10,
            "quit": 10,
            "goodbye": 10,
            "bye": 8,
            "stop": 8,
        },

        Intent.AI_CHAT: {
            "explain": 10,
            "what is": 10,
            "who is": 10,
            "why": 9,
            "how": 9,
            "tell me": 8,
            "define": 8,
        },
    }

    def __init__(self) -> None:

        self.last_confidence = 0.0

        self._compiled: Dict[
            Intent,
            list[tuple[re.Pattern[str], int]]
        ] = {}

        self._compile_rules()

    # -------------------------------------------------
    # Compile Rules
    # -------------------------------------------------

    def _compile_rules(self) -> None:

        self._compiled.clear()

        for intent, rules in self.INTENT_RULES.items():

            compiled_rules = []

            for phrase, weight in sorted(
                rules.items(),
                key=lambda item: len(item[0]),
                reverse=True,
            ):

                pattern = re.compile(
                    rf"\b{re.escape(phrase)}\b",
                    flags=re.IGNORECASE,
                )

                compiled_rules.append(
                    (
                        pattern,
                        weight,
                    )
                )

            self._compiled[intent] = compiled_rules

    # -------------------------------------------------
    # Detect Intent
    # -------------------------------------------------

    def detect(
        self,
        text: str,
    ) -> Intent:

        if not text:

            self.last_confidence = 0.0
            return Intent.AI_CHAT

        text = text.lower().strip()

        scores: Dict[Intent, int] = {}

        for intent, rules in self._compiled.items():

            score = 0

            for pattern, weight in rules:

                if pattern.search(text):
                    score += weight

            scores[intent] = score

        best_intent = Intent.AI_CHAT
        best_score = -1

        for intent, score in scores.items():

            if score > best_score:

                best_score = score
                best_intent = intent

        total_score = sum(scores.values())

        if total_score == 0:

            self.last_confidence = 0.0

            logger.info(
                "No intent matched. Falling back to AI_CHAT."
            )

            return Intent.AI_CHAT

        self.last_confidence = round(
            best_score / total_score,
            2,
        )

        logger.info(
            "Intent=%s Score=%d Confidence=%.2f",
            best_intent.name,
            best_score,
            self.last_confidence,
        )

        return best_intent

    # -------------------------------------------------
    # Confidence
    # -------------------------------------------------

    def confidence(self) -> float:

        return self.last_confidence

    # -------------------------------------------------
    # Register Rule
    # -------------------------------------------------

    def register(
        self,
        intent: Intent,
        keyword: str,
        weight: int = 5,
    ) -> None:

        keyword = keyword.lower().strip()

        self.INTENT_RULES.setdefault(
            intent,
            {},
        )[keyword] = weight

        self._compile_rules()

    # -------------------------------------------------
    # Remove Rule
    # -------------------------------------------------

    def unregister(
        self,
        intent: Intent,
        keyword: str,
    ) -> bool:

        keyword = keyword.lower().strip()

        rules = self.INTENT_RULES.get(intent)

        if not rules:
            return False

        if keyword not in rules:
            return False

        del rules[keyword]

        self._compile_rules()

        return True

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def stats(self) -> dict:

        return {

            "intents": len(self.INTENT_RULES),

            "compiled_rules": sum(
                len(rules)
                for rules in self._compiled.values()
            ),

            "confidence": self.last_confidence,
        }

    # -------------------------------------------------
    # Debug
    # -------------------------------------------------

    def debug(
        self,
        text: str,
    ) -> None:

        intent = self.detect(text)

        print()
        print("=" * 60)
        print("Text       :", text)
        print("Intent     :", intent.name)
        print("Confidence :", self.last_confidence)
        print("=" * 60)
        print()

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset(self) -> None:

        self.last_confidence = 0.0