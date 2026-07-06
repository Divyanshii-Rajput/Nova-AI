from __future__ import annotations

import logging

from app.models.command import Command
from app.models.intent import Intent

from app.nlp.text_cleaner import TextCleaner
from app.nlp.alias_matcher import AliasMatcher
from app.nlp.intent_detector import IntentDetector
from app.nlp.entity_extractor import EntityExtractor

logger = logging.getLogger(__name__)


class CommandParser:
    """
    Converts raw user speech into a Command object.

    Pipeline
    --------
    Raw Text
        ↓
    TextCleaner
        ↓
    AliasMatcher
        ↓
    IntentDetector
        ↓
    EntityExtractor
        ↓
    Command
    """

    def __init__(self) -> None:

        self.cleaner = TextCleaner()

        self.alias_matcher = AliasMatcher()

        self.intent_detector = IntentDetector()

        self.entity_extractor = EntityExtractor()

    def parse(
        self,
        text: str,
    ) -> Command:
        """
        Parse raw text into a Command object.
        """

        original_text = text or ""

        cleaned_text = self.cleaner.clean(original_text)

        cleaned_text = self.alias_matcher.normalize(
            cleaned_text
        )

        intent = self.intent_detector.detect(
            cleaned_text
        )

        entity = self.entity_extractor.extract(
            cleaned_text,
            intent,
        )

        confidence = self.intent_detector.confidence()

        logger.info(
            "Intent=%s Entity=%s Confidence=%.2f",
            intent.name,
            entity,
            confidence,
        )

        return Command(
            original_text=original_text,
            cleaned_text=cleaned_text,
            intent=intent,
            entity=entity,
            confidence=confidence,
        )

    def parse_many(
        self,
        texts: list[str],
    ) -> list[Command]:
        """
        Parse multiple commands.
        """

        return [
            self.parse(text)
            for text in texts
        ]

    def debug(
        self,
        text: str,
    ) -> None:
        """
        Print parser output.
        """

        command = self.parse(text)

        print()
        print("=" * 60)
        print("Original   :", command.original_text)
        print("Cleaned    :", command.cleaned_text)
        print("Intent     :", command.intent.name)
        print("Entity     :", command.entity)
        print("Confidence :", command.confidence)
        print("=" * 60)
        print()

    def stats(self) -> dict:
        """
        Parser statistics.
        """

        return {
            "intent_confidence":
                self.intent_detector.confidence(),
        }