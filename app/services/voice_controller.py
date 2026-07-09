"""
Nova AI Desktop Assistant
-------------------------

Voice Controller

Coordinates the complete voice assistant workflow.
"""

from __future__ import annotations

import re
from PySide6.QtCore import QObject, Signal, QThread


from app.audio.speaker import Speaker
from app.services.assistant_bridge import AssistantBridge
from app.services.voice_worker import VoiceWorker


class VoiceController(QObject):
    """
    Controls the complete voice assistant workflow.

    Responsibilities
    ----------------
    - Start/stop listening
    - Manage worker thread
    - Forward speech to AssistantBridge
    - Speak assistant responses
    """

    # ----------------------------
    # UI Signals
    # ----------------------------

    listening_started = Signal()
    listening_finished = Signal()

    processing_started = Signal()
    processing_finished = Signal()

    command_recognized = Signal(str)
    response_ready = Signal(str)

    error_occurred = Signal(str)
    state_changed = Signal(str)

    # ----------------------------

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.assistant: AssistantBridge | None = None

        self.speaker = Speaker()

        self.thread: QThread | None = None
        self.worker: VoiceWorker | None = None

        self._running = False
        self._is_speaking = False
        self._is_processing = False
        self._is_standby = True
        self._should_stop_after_speaking = False


    def set_assistant_bridge(
        self,
        bridge: AssistantBridge,
    ) -> None:
        """
        Inject the application's AssistantBridge.
        """

        self.assistant = bridge

        self.assistant.processing_started.connect(
            self._on_processing_started
        )

        self.assistant.processing_finished.connect(
            self._on_processing_finished
        )

        self.assistant.response_ready.connect(
            self._on_response
        )

        self.assistant.speaking_started.connect(
            self._on_speaking_started
        )

        self.assistant.speaking_finished.connect(
            self._on_speaking_finished
        )
        
    # ======================================================
    # Public API
    # ======================================================

    def start(self) -> None:

        if self._running:
            return

        self._running = True
        self._is_standby = True

        self.listen_once()


    
    def stop(self) -> None:

        self._running = False
        self.speaker.stop()

        self.state_changed.emit(
            "Paused"
        )

        if self.worker and hasattr(self.worker, 'engine') and self.worker.engine:
            self.worker.engine.recorder.should_stop = True

        self.speaker.stop()
        if self.assistant and hasattr(self.assistant, 'assistant') and self.assistant.assistant:
            try:
                self.assistant.assistant.speaker.stop()
            except Exception:
                pass

        if self.thread:
            self.thread.quit()
            # Do NOT block the GUI thread with wait()
            self.thread = None
            self.worker = None

    
    def is_running(self):

        return self._running

    # ======================================================
    # Voice Pipeline
    # ======================================================

    def listen_once(self) -> None:
        """
        Start one voice recognition cycle.
        """

        if not self._running:
            return

        if self.assistant is None:

            self.error_occurred.emit(
                "AssistantBridge not configured."
            )

            return

        # Prevent multiple workers from running.
        if self.thread is not None:
            return

        self.speaker.stop()

        self.listening_started.emit()

        
        if self._is_standby:
            self.state_changed.emit('Standby (Say "Hey Nova")')
        else:
            self.state_changed.emit("Listening...")


        self.thread = QThread()

        self.worker = VoiceWorker()

        self.worker.moveToThread(
            self.thread
        )

        # ----------------------------
        # Thread lifecycle
        # ----------------------------

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.command_recognized.connect(
            self._on_command
        )

        self.worker.error_occurred.connect(
            self.error_occurred.emit
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self._cleanup_thread
        )

        self.thread.finished.connect(
            self.listening_finished.emit
        )

        self.thread.start()

    # ======================================================
    # Worker callbacks
    # ======================================================

    def _on_command(
        self,
        command: str,
    ) -> None:
        clean_text = command.lower().strip()

        if self._is_standby:
            # Check for wake word and its common phonetic mishearings
            wake_match = re.search(r"\b(?:hey\s+)?(?:nova|noha|noah|nowa|lova|ova|noba|no\s+va)\b", clean_text)
            if wake_match:
                self._is_standby = False
                
                # Extract command after wake word if any
                start_idx = wake_match.end()
                sub_command = clean_text[start_idx:].strip()
                # Remove leading/trailing punctuation (like commas or periods) from command
                sub_command = re.sub(r"^[^\w]+|[^\w]+$", "", sub_command).strip()

                if sub_command:
                    self._is_processing = True
                    self.command_recognized.emit(sub_command)

                else:
                    # Just wake up and greet
                    self._is_speaking = True
                    self.state_changed.emit("Speaking...")
                    
                    from app.ui.thread_manager import thread_manager
                    thread_manager.submit_with_callbacks(
                        self.speaker.speak,
                        "Yes? How can I help you?",
                        on_finished=self._on_speaking_finished
                    )
            else:
                # No wake word, ignore and listen again
                self._is_processing = False
                self._check_and_resume_listening()
        else:
            # We are active. Check for sleep commands
            clean_text_clean = re.sub(r"[^\w\s]", "", clean_text)
            sleep_phrases = {
                "stop listening", "go to sleep", "ok you can now stop", "stop nova",
                "you can stop now", "bye bye nova", "ok stop", "stop listening nova", "stop",
                "goodbye", "exit", "bye", "quit"
            }
            if any(phrase in clean_text_clean for phrase in sleep_phrases):
                self._is_standby = True
                self._is_speaking = True
                self._should_stop_after_speaking = False
                self.state_changed.emit("Speaking...")

                from app.ui.thread_manager import thread_manager
                thread_manager.submit_with_callbacks(
                    self.speaker.speak,
                    "Goodbye!",
                    on_finished=self._on_speaking_finished
                )
            else:
                # Normal command execution
                self._is_processing = True
                self.command_recognized.emit(command)

    def _on_processing_started(self) -> None:
        self._is_processing = True
        self.state_changed.emit("Thinking...")
        self.processing_started.emit()

    def _on_response(
        self,
        response: str,
    ) -> None:
        """
        Assistant generated a response.
        """
        pass

    def _on_speaking_started(self, response: str) -> None:
        self._is_speaking = True
        self.state_changed.emit("Speaking...")
        self.response_ready.emit(response)

    def _on_speaking_finished(self) -> None:
        self._is_speaking = False
        if getattr(self, "_should_stop_after_speaking", False):
            self._should_stop_after_speaking = False
            self.stop()
        else:
            self._check_and_resume_listening()

    def _on_processing_finished(
        self,
    ) -> None:
        """
        Assistant finished processing.
        """
        self._is_processing = False
        self.processing_finished.emit()
        
        if not self._is_speaking:
            self._check_and_resume_listening()

    # ======================================================
    # Cleanup
    # ======================================================

    def _cleanup_thread(
        self,
    ) -> None:
        """
        Reset thread references.
        """

        if self.thread:
            self.thread.deleteLater()

        self.thread = None
        self.worker = None

        # Only resume listening here if we failed to detect speech or had an error
        self._check_and_resume_listening()

    def _check_and_resume_listening(self) -> None:
        """
        Checks state and triggers next listen_once cycle.
        """
        if self._running and not self._is_processing and not self._is_speaking:
            if self._is_standby:
                self.state_changed.emit('Standby (Say "Hey Nova")')
            else:
                self.state_changed.emit("Listening...")
            from PySide6.QtCore import QTimer
            QTimer.singleShot(
                250,
                self.listen_once,
            )