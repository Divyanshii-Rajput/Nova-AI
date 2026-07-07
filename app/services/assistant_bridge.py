from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal, Slot

from app.assistant import Assistant


logger = logging.getLogger(__name__)


class AssistantBridge(QObject):
    """
    Connects Nova backend with Desktop UI.
    """

    response_ready = Signal(str)

    processing_started = Signal()

    processing_finished = Signal()


    def __init__(self):

        super().__init__()

        self.assistant = Assistant()


    @Slot(str)
    def process_message(
        self,
        message: str,
    ) -> None:
        """
        Process user text from UI.
        """

        if not message.strip():
            return

        self.processing_started.emit()

        try:

            response = self._process(message)

            self.response_ready.emit(
                response
            )

        except Exception:

            logger.exception(
                "Assistant processing failed"
            )

            self.response_ready.emit(
                "Sorry, something went wrong."
            )

        finally:

            self.processing_finished.emit()


    def _process(
        self,
        message: str,
    ) -> str:
        """
        Run backend pipeline.
        """

        command = self.assistant.build_command(
            message
        )

        response = self.assistant.engine.execute(command)

        print("DEBUG RESPONSE:", response)
        print("SUCCESS:", response.success)
        print("MESSAGE:", repr(response.message))
        print("DATA:", response.data)

        return response.message or "Command executed successfully."


__all__ = [
    "AssistantBridge",
]