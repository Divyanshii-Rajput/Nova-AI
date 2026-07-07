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

from app.ui.constants import (
    CHAT_INPUT_HEIGHT,
    PAGE_SPACING,
    SPACE_12,
    SPACE_16,
)

from app.ui.resources import resources
from app.ui.widgets.chat_bubble import ChatBubble
from app.ui.widgets.microphone_widget import MicrophoneWidget

from app.services.assistant_bridge import AssistantBridge
from app.services.voice_bridge import VoiceBridge


class ChatPage(QWidget):
    """
    Main chat interface.
    """

    messageSent = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName(
            "ChatPage"
        )

        self.bridge = AssistantBridge()
        self.voiceBridge = VoiceBridge()
        
        self.bridge.response_ready.connect(
            self._on_response
        )

        self.bridge.processing_started.connect(
            lambda: self.set_input_enabled(False)
        )

        self.bridge.processing_finished.connect(
            lambda: self.set_input_enabled(True)
        )
        
        self.voiceBridge.speech_recognized.connect(
            self._on_voice_text
        )

        self.voiceBridge.listening_started.connect(
            lambda: self.microphone.setListening(True)
        )

        self.voiceBridge.listening_finished.connect(
            lambda: self.microphone.reset()
        )

        self._build_ui()

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
            self.voiceBridge.listen
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

    def _on_voice_text(
        self,
        text: str,
    ) -> None:

        self.messageEdit.setText(
            text
        )

        self._send_message()
        
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