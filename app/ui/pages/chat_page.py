"""
Nova AI Desktop Assistant
-------------------------

Chat Page

Primary conversational interface.

Responsibilities
----------------
- Display conversation history
- Accept user input
- Send messages to AssistantBridge
- Display backend responses
- Auto-scroll
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.assistant_bridge import AssistantBridge
from app.services.voice_controller import VoiceController
from app.ui.constants import (
    CHAT_INPUT_HEIGHT,
    PAGE_SPACING,
    SPACE_12,
    SPACE_16,
)

from app.ui.resources import resources
from app.ui.widgets.chat_bubble import ChatBubble
from app.ui.widgets.microphone_widget import MicrophoneWidget

class ChatPage(QWidget):
    """
    Main chat interface.
    """

    messageSent = Signal(str)

    def __init__(
        self,
        assistant_bridge: AssistantBridge,
        voice_controller: VoiceController,
        parent=None,
    ):

        super().__init__(parent)

        self.setObjectName(
            "ChatPage"
        )
        
        self.bridge = assistant_bridge
        self.voice_controller = voice_controller

        self._build_ui()

        self._connect_signals()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:

        root = QVBoxLayout(self)

        root.setContentsMargins(
            SPACE_16,
            SPACE_16,
            SPACE_16,
            SPACE_16,
        )

        root.setSpacing(
            PAGE_SPACING
        )

        self.scrollArea = QScrollArea()

        self.scrollArea.setWidgetResizable(
            True
        )

        self.scrollArea.setFrameShape(
            QFrame.Shape.NoFrame
        )

        root.addWidget(
            self.scrollArea
        )

        self.chatContainer = QWidget()

        self.chatLayout = QVBoxLayout(
            self.chatContainer
        )

        self.chatLayout.setSpacing(
            SPACE_12
        )

        self.chatLayout.addStretch()

        self.scrollArea.setWidget(
            self.chatContainer
        )


        inputRow = QHBoxLayout()

        inputRow.setSpacing(
            SPACE_12
        )

        self.microphone = MicrophoneWidget()

        self.microphone.clicked.connect(
            self._toggle_voice
        )

        inputRow.addWidget(
            self.microphone
        )

        self.messageEdit = QLineEdit()

        self.messageEdit.setPlaceholderText(
            "Message Nova..."
        )

        self.messageEdit.setMinimumHeight(
            CHAT_INPUT_HEIGHT
        )

        self.messageEdit.returnPressed.connect(
            self._send_message
        )

        inputRow.addWidget(
            self.messageEdit
        )


        self.sendButton = QPushButton()

        self.sendButton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.sendButton.setIcon(
            resources.icon(
                "fa6s.paper-plane"
            )
        )

        self.sendButton.clicked.connect(
            self._send_message
        )

        inputRow.addWidget(
            self.sendButton
        )


        root.addLayout(
            inputRow
        )

    def _connect_signals(self) -> None:

        # -----------------------------
        # AssistantBridge
        # -----------------------------

        self.bridge.response_ready.connect(
            self._on_response
        )

        self.bridge.processing_started.connect(
            lambda: self.set_input_enabled(False)
        )

        self.bridge.processing_finished.connect(
            lambda: self.set_input_enabled(True)
        )

        # -----------------------------
        # VoiceController
        # -----------------------------

        self.voice_controller.command_recognized.connect(
            self._on_voice_text
        )

        self.voice_controller.state_changed.connect(
            self._on_voice_state_changed
        )



    # ======================================================
    # Messaging
    # ======================================================

    def _send_message(self) -> None:

        message = (
            self.messageEdit
            .text()
            .strip()
        )

        if not message:
            return


        self.add_user_message(
            message
        )

        self.messageEdit.clear()


        self.messageSent.emit(
            message
        )


        self.bridge.process_message(
            message
        )
    
    def _toggle_voice(self):

        if self.voice_controller.is_running():

            self.voice_controller.stop()

        else:

            self.voice_controller.start()
            
    def _on_voice_text(
        self,
        text: str,
    ) -> None:

        self.messageEdit.setText(text)

        self.messageEdit.returnPressed.emit()

    def _on_voice_state_changed(self, state: str) -> None:
        """
        Animate microphone widget based on voice controller state.
        """
        if state == "Listening...":
            self.microphone.setListening(True)
            self.microphone.setThinking(False)
            self.microphone.setSpeaking(False)
        elif state == "Thinking...":
            self.microphone.setListening(False)
            self.microphone.setThinking(True)
            self.microphone.setSpeaking(False)
        elif state == "Speaking...":
            self.microphone.setListening(False)
            self.microphone.setThinking(False)
            self.microphone.setSpeaking(True)
        else:
            self.microphone.reset()

        
    def _on_response(
        self,
        response: str,
    ) -> None:

        self.add_assistant_message(
            response
        )


    def add_user_message(
        self,
        message: str,
    ) -> ChatBubble:

        bubble = ChatBubble(
            message,
            is_user=True,
        )

        self._insert_bubble(
            bubble
        )

        return bubble


    def add_assistant_message(
        self,
        message: str,
    ) -> ChatBubble:

        bubble = ChatBubble(
            message,
            is_user=False,
        )

        self._insert_bubble(
            bubble
        )

        return bubble


    def _insert_bubble(
        self,
        bubble: ChatBubble,
    ) -> None:

        index = max(
            0,
            self.chatLayout.count() - 1,
        )

        self.chatLayout.insertWidget(
            index,
            bubble,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        self.scroll_to_bottom()


    # ======================================================
    # Utilities
    # ======================================================

    def clear_chat(self) -> None:

        while self.chatLayout.count() > 1:

            item = self.chatLayout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()


    def scroll_to_bottom(self) -> None:

        scrollbar = (
            self.scrollArea
            .verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )


    def message_count(self) -> int:

        return max(
            0,
            self.chatLayout.count() - 1,
        )


    def set_input_enabled(
        self,
        enabled: bool,
    ) -> None:

        self.messageEdit.setEnabled(
            enabled
        )

        self.sendButton.setEnabled(
            enabled
        )


    def sizeHint(self):

        return QSize(
            1200,
            800,
        )


    def minimumSizeHint(self):

        return QSize(
            900,
            600,
        )


__all__ = [
    "ChatPage",
]