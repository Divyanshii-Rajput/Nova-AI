"""
Nova AI Desktop Assistant
-------------------------

Chat Page

Primary conversational interface.

Responsibilities
----------------
- Display conversation history
- Stream assistant responses
- Accept user input
- Send messages
- Auto-scroll
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
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

        self.setObjectName("ChatPage")

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

        root.setSpacing(PAGE_SPACING)

        self.scrollArea = QScrollArea()

        self.scrollArea.setWidgetResizable(True)

        self.scrollArea.setFrameShape(
            QFrame.Shape.NoFrame
        )

        root.addWidget(self.scrollArea)

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

        # ==================================================
        # Input
        # ==================================================

        inputRow = QHBoxLayout()

        inputRow.setSpacing(
            SPACE_12
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
        """
        Send the current message.
        """

        message = self.messageEdit.text().strip()

        if not message:
            return

        self.add_user_message(message)

        self.messageSent.emit(message)

        self.messageEdit.clear()

    def add_user_message(
        self,
        message: str,
    ) -> ChatBubble:
        """
        Add a user message bubble.
        """

        bubble = ChatBubble(
            message,
            is_user=True,
        )

        self._insert_bubble(bubble)

        return bubble

    def add_assistant_message(
        self,
        message: str,
    ) -> ChatBubble:
        """
        Add an assistant message bubble.
        """

        bubble = ChatBubble(
            message,
            is_user=False,
        )

        self._insert_bubble(bubble)

        return bubble

    def _insert_bubble(
        self,
        bubble: ChatBubble,
    ) -> None:
        """
        Insert a bubble before the bottom stretch.
        """

        index = max(
            0,
            self.chatLayout.count() - 1,
        )

        self.chatLayout.insertWidget(
            index,
            bubble,
        )

        self.scroll_to_bottom()

    # ======================================================
    # Utilities
    # ======================================================

    def clear_chat(self) -> None:
        """
        Remove all chat bubbles.
        """

        while self.chatLayout.count() > 1:

            item = self.chatLayout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def scroll_to_bottom(self) -> None:
        """
        Scroll to the latest message.
        """

        scrollbar = self.scrollArea.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def message_count(self) -> int:
        """
        Return the number of displayed messages.
        """

        return max(
            0,
            self.chatLayout.count() - 1,
        )

    def set_input_enabled(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable the input controls.
        """

        self.messageEdit.setEnabled(enabled)

        self.sendButton.setEnabled(enabled)

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(1200, 800)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(900, 600)


__all__ = [
    "ChatPage",
]