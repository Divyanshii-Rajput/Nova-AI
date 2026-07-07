from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal, Slot

from app.assistant import Assistant
from app.ui.thread_manager import thread_manager
from app.memory.conversation_memory import conversation_memory

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
        self.memory = conversation_memory

    @Slot(str)
    def process_message(
        self,
        message: str,
    ) -> None:

        if not message.strip():
            return

        self.processing_started.emit()

        self._worker = thread_manager.submit_with_callbacks(
            self._process,
            message,
            on_result=self.response_ready.emit,
            on_error=self._handle_error,
            on_finished=self.processing_finished.emit,
        )

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

        reply = response.message or "Command executed successfully."

        self.memory.add(
            message,
            reply,
        )

        print("History size:", len(self.memory.all()))
        
        return reply

    def _handle_error(
        self,
        error: str,
    ) -> None:

        logger.error(error)

        self.response_ready.emit(
            "Sorry, something went wrong."
        )
    
__all__ = [
    "AssistantBridge",
]