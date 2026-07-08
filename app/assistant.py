from __future__ import annotations

import logging
from typing import Any

from app.audio.speaker import Speaker
from app.services.voice_engine import VoiceEngine

from app.models.command import Command
from app.models.intent import Intent
from app.models.response import Response

from app.nlp.text_cleaner import TextCleaner
from app.nlp.alias_matcher import AliasMatcher
from app.nlp.intent_detector import IntentDetector
from app.nlp.entity_extractor import EntityExtractor

from app.services.action_engine import ActionEngine


logger = logging.getLogger(__name__)


class Assistant:
    """
    Nova AI Assistant

    Main Coordinator

        Voice
          ↓
      Text Cleaner
          ↓
      Alias Matcher
          ↓
     Intent Detector
          ↓
    Entity Extractor
          ↓
        Command
          ↓
     Action Engine
          ↓
       Response
          ↓
        Speaker
    """

    def __init__(self) -> None:

        # -------------------------------------------------
        # Voice
        # -------------------------------------------------

        self.voice = VoiceEngine()
        self.speaker = Speaker()

        # -------------------------------------------------
        # NLP
        # -------------------------------------------------

        self.cleaner = TextCleaner()
        self.alias = AliasMatcher()
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()

        # -------------------------------------------------
        # Action Engine
        # -------------------------------------------------

        self.engine = ActionEngine()

        # -------------------------------------------------
        # Conversation State
        # -------------------------------------------------

        self.running = True

        self.last_command: Command | None = None

        self.last_results: list[Any] = []

        self.awaiting_choice = False

        self.awaiting_confirmation = False

    # =====================================================
    # Command Pipeline
    # =====================================================

    def build_command(
        self,
        text: str,
    ) -> Command:

        original = text

        cleaned = self.cleaner.clean(text)

        logger.info(
            "Cleaned Text : %s",
            cleaned,
        )

        cleaned = self.alias.normalize(cleaned)

        logger.info(
            "Normalized Text : %s",
            cleaned,
        )

        intent = self.intent_detector.detect(
            cleaned,
        )

        entity = self.entity_extractor.extract(
            cleaned,
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

            original_text=original,

            cleaned_text=cleaned,

            intent=intent,

            entity=entity,

            confidence=confidence,

        )

    # =====================================================
    # Process
    # =====================================================

    def process(
        self,
        text: str,
    ) -> bool:

        command = self.build_command(text)

        self.last_command = command

        response = self.engine.execute(command)

        if not isinstance(response, Response):

            logger.error(
                "ActionEngine returned %s instead of Response.",
                type(response).__name__,
            )

            response = Response(
                success=False,
                message="Internal assistant error.",
            )

        self.respond(response.message)

        if command.intent == Intent.EXIT:

            return False

        return True

    # =====================================================
    # Respond
    # =====================================================

    def respond(
        self,
        message: str,
    ) -> None:

        if not message:
            return

        print()
        print(f"Nova : {message}")
        print()

        try:

            self.speaker.speak(message)

        except Exception:

            logger.exception(
                "Failed to speak response."
            )

    # =====================================================
    # Listen
    # =====================================================

    def listen(
        self,
    ) -> str | None:

        print()
        print("[Listening...]")
        print()

        try:

            text = self.voice.listen()

        except Exception:

            logger.exception(
                "Voice recognition failed."
            )

            return None

        if not text:
            return None

        text = text.strip()

        if not text:
            return None

        print(f"You : {text}")

        return text

    # =====================================================
    # Step
    # =====================================================

    def step(
        self,
    ) -> bool:

        text = self.listen()

        if text is None:

            return True

        return self.process(text)

    # =====================================================
    # Startup
    # =====================================================

    def startup(
        self,
    ) -> None:

        print("=" * 60)
        print("Nova AI Started")
        print("=" * 60)

        logger.info(
            "Nova initialized successfully."
        )

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        print()
        print("Goodbye!")
        print()

        logger.info(
            "Nova shutdown complete."
        )

    # =====================================================
    # Main Loop
    # =====================================================

    def run(
        self,
    ) -> None:

        self.startup()

        while self.running:

            try:

                self.running = self.step()

            except KeyboardInterrupt:

                logger.info(
                    "Interrupted by user."
                )

                break

            except Exception:

                logger.exception(
                    "Unexpected assistant error."
                )

                self.respond(
                    "Sorry, something went wrong."
                )

        self.shutdown()
        # =====================================================
    # Conversation Helpers
    # =====================================================

    def remember_results(
        self,
        results: list[Any],
    ) -> None:
        """
        Remember the latest search results.

        Example
        -------
        Open resume
            ↓
        5 matching files

        User:
            open second one
        """

        self.last_results = list(results)

    def clear_results(
        self,
    ) -> None:

        self.last_results.clear()

    def has_results(
        self,
    ) -> bool:

        return bool(self.last_results)

    def result(
        self,
        index: int,
    ) -> Any | None:

        if index < 0:
            return None

        if index >= len(self.last_results):
            return None

        return self.last_results[index]

    # =====================================================
    # Confirmation Handling
    # =====================================================

    def ask_confirmation(
        self,
        question: str,
    ) -> None:

        self.awaiting_confirmation = True

        self.respond(question)

    def clear_confirmation(
        self,
    ) -> None:

        self.awaiting_confirmation = False

    def confirmed(
        self,
        text: str,
    ) -> bool:

        if not text:
            return False

        text = text.lower().strip()

        positive = {

            "yes",
            "yeah",
            "yup",
            "yep",
            "sure",
            "ok",
            "okay",
            "confirm",
            "do it",
            "go ahead",

        }

        return text in positive

    # =====================================================
    # Choice Parsing
    # =====================================================

    def parse_choice(
        self,
        text: str,
    ) -> int | None:

        if not text:
            return None

        text = text.lower().strip()

        words = {

            "first": 0,
            "second": 1,
            "third": 2,
            "fourth": 3,
            "fifth": 4,
            "sixth": 5,
            "seventh": 6,
            "eighth": 7,
            "ninth": 8,
            "tenth": 9,

        }

        for word, index in words.items():

            if word in text:
                return index

        if text.isdigit():

            value = int(text)

            if value > 0:

                return value - 1

        return None

    # =====================================================
    # Utilities
    # =====================================================

    def reset_conversation(
        self,
    ) -> None:

        self.last_command = None

        self.last_results.clear()

        self.awaiting_choice = False

        self.awaiting_confirmation = False

    def stats(
        self,
    ) -> dict:

        return {

            "running": self.running,

            "last_intent": (
                self.last_command.intent.name
                if self.last_command
                else None
            ),

            "last_entity": (
                self.last_command.entity
                if self.last_command
                else None
            ),

            "last_confidence": (
                self.last_command.confidence
                if self.last_command
                else 0.0
            ),

            "stored_results": len(self.last_results),

            "awaiting_choice": self.awaiting_choice,

            "awaiting_confirmation":
                self.awaiting_confirmation,

        }