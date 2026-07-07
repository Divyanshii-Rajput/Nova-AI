from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal, Slot

from app.services.voice_engine import VoiceEngine
from app.ui.thread_manager import thread_manager

logger = logging.getLogger(__name__)


class VoiceBridge(QObject):
    """
    Bridge between the Desktop UI and the Voice Engine.
    """

    speech_recognized = Signal(str)

    listening_started = Signal()

    listening_finished = Signal()

    error = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.engine = VoiceEngine()

    @Slot()
    def listen(self) -> None:
        """
        Start voice recognition asynchronously.
        """

        self.listening_started.emit()

        self._worker = thread_manager.submit_with_callbacks(
            self._listen,
            on_result=self._on_result,
            on_error=self._on_error,
            on_finished=self.listening_finished.emit,
        )

    def _listen(self) -> str:
        """
        Execute the voice pipeline.
        """

        return self.engine.listen()

    def _on_result(
        self,
        text: str,
    ) -> None:

        text = text.strip()

        if text:
            self.speech_recognized.emit(text)

    def _on_error(
        self,
        error: str,
    ) -> None:

        logger.error(error)

        self.error.emit(error)


__all__ = [
    "VoiceBridge",
]