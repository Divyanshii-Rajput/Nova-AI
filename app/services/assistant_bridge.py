from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal, Slot

from app.assistant import Assistant
from app.ui.thread_manager import thread_manager
from app.memory.conversation_memory import conversation_memory
from app.llm.llm_router import LLMRouter
from app.models.intent import Intent

logger = logging.getLogger(__name__)


class AssistantBridge(QObject):
    """
    Connects Nova backend with Desktop UI.
    """

    response_ready = Signal(str)

    processing_started = Signal()

    processing_finished = Signal()

    command_executed = Signal(object, object)


    speaking_started = Signal(str)

    speaking_finished = Signal()


    def __init__(self):

        super().__init__()

        self.assistant = Assistant()
        self.router = LLMRouter()
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

        if command.intent not in (Intent.AI_CHAT, Intent.UNKNOWN):
            response = self.assistant.engine.execute(command)
        else:
            response = self.router.generate(command.cleaned_text)

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
        
        self.command_executed.emit(command, response)

        # Centralized speaking for all assistant responses
        self.speaking_started.emit(reply)
        self.assistant.speaker.speak(reply)
        self.speaking_finished.emit()
        
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