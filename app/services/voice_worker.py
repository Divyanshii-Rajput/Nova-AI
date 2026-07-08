"""
Nova AI Desktop Assistant
-------------------------

Voice Worker

Runs voice recognition in a background thread.

Responsibilities
----------------
- Record microphone input
- Convert speech to text
- Emit recognized command
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from app.services.voice_engine import VoiceEngine


class VoiceWorker(QObject):
    """
    Background worker for speech recognition.
    """

    finished = Signal()

    command_recognized = Signal(str)

    error_occurred = Signal(str)

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.engine = VoiceEngine()

    @Slot()
    def run(self):
        """
        Execute one voice recognition cycle.
        """

        try:

            text = self.engine.listen()

            if text:

                self.command_recognized.emit(
                    text
                )

            else:

                self.error_occurred.emit(
                    "No speech detected."
                )

        except Exception as e:

            self.error_occurred.emit(
                str(e)
            )

        finally:

            self.finished.emit()