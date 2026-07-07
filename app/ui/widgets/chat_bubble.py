"""
Nova AI Desktop Assistant
-------------------------

Chat Bubble

Modern message bubble inspired by
ChatGPT Desktop and Cursor.

Supports

- User messages
- Assistant messages
- Markdown-ready text
- Timestamp
- Avatar
- Copy support
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    CHAT_AVATAR_SIZE,
    CHAT_BUBBLE_RADIUS,
    CHAT_MARGIN,
    CHAT_SPACING,
    ICON_16,
    SPACE_12,
    SPACE_8,
)
from app.ui.resources import resources


class ChatBubble(QFrame):
    """
    Single chat message widget.
    """

    def __init__(
        self,
        message: str,
        *,
        is_user: bool,
        timestamp: datetime | None = None,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._message = message

        self._is_user = is_user

        self._timestamp = (
            timestamp
            or datetime.now()
        )

        self.setObjectName(
            "UserBubble"
            if is_user
            else "AssistantBubble"
        )

        self.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:

        root = QHBoxLayout(self)

        root.setContentsMargins(
            CHAT_MARGIN,
            SPACE_8,
            CHAT_MARGIN,
            SPACE_8,
        )

        root.setSpacing(CHAT_SPACING)

        avatar = QLabel()

        avatar.setFixedSize(
            CHAT_AVATAR_SIZE,
            CHAT_AVATAR_SIZE,
        )

        if self._is_user:

            avatar.setPixmap(
                resources.icon(
                    "fa6s.user",
                ).pixmap(
                    CHAT_AVATAR_SIZE,
                    CHAT_AVATAR_SIZE,
                )
            )

        else:

            avatar.setPixmap(
                resources.icon(
                    "fa6s.robot",
                ).pixmap(
                    CHAT_AVATAR_SIZE,
                    CHAT_AVATAR_SIZE,
                )
            )

        bubble = QFrame()

        bubble.setObjectName(
            "BubbleContainer"
        )

        bubble_layout = QVBoxLayout(
            bubble
        )

        bubble_layout.setContentsMargins(
            SPACE_12,
            SPACE_12,
            SPACE_12,
            SPACE_12,
        )

        bubble_layout.setSpacing(6)

        self.messageView = QTextBrowser()

        self.messageView.setOpenExternalLinks(
            True
        )

        self.messageView.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.messageView.setMarkdown(
            self._message
        )

        bubble_layout.addWidget(
            self.messageView
        )

        footer = QHBoxLayout()

        self.timeLabel = QLabel(
            self._timestamp.strftime(
                "%H:%M"
            )
        )

        footer.addWidget(
            self.timeLabel
        )

        footer.addStretch()

        self.copyButton = QPushButton()

        self.copyButton.setFlat(True)

        self.copyButton.setIcon(
            resources.icon(
                "fa6s.copy"
            )
        )

        self.copyButton.setIconSize(
            QSize(
                ICON_16,
                ICON_16,
            )
        )

        footer.addWidget(
            self.copyButton
        )

        bubble_layout.addLayout(
            footer
        )

        if self._is_user:

            root.addStretch()

            root.addWidget(bubble)

            root.addWidget(avatar)

        else:

            root.addWidget(avatar)

            root.addWidget(bubble)

            root.addStretch()

        self.copyButton.clicked.connect(
            self.copyMessage
        )
    
        # ======================================================
    # Public API
    # ======================================================

    def message(self) -> str:
        """
        Return the message text.
        """

        return self._message

    def setMessage(
        self,
        message: str,
    ) -> None:
        """
        Update the displayed message.
        """

        self._message = message

        self.messageView.setMarkdown(message)

    def appendMessage(
        self,
        text: str,
    ) -> None:
        """
        Append streamed text to the current message.
        """

        self._message += text

        self.messageView.setMarkdown(self._message)

    def isUser(self) -> bool:
        """
        Return True if this is a user message.
        """

        return self._is_user

    def setTimestamp(
        self,
        timestamp: datetime,
    ) -> None:
        """
        Update the timestamp.
        """

        self._timestamp = timestamp

        self.timeLabel.setText(
            timestamp.strftime("%H:%M")
        )

    # ======================================================
    # Actions
    # ======================================================

    def copyMessage(self) -> None:
        """
        Copy the message to the clipboard.
        """

        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setText(self._message)

    # ======================================================
    # Appearance
    # ======================================================

    def setSelectable(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable text selection.
        """

        self.messageView.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            if enabled
            else Qt.TextInteractionFlag.NoTextInteraction
        )

    def setReadOnly(
        self,
        read_only: bool,
    ) -> None:
        """
        Set the message view read-only state.
        """

        self.messageView.setReadOnly(read_only)

    # ======================================================
    # Utilities
    # ======================================================

    def clear(self) -> None:
        """
        Clear the message contents.
        """

        self._message = ""

        self.messageView.clear()

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(700, 120)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(320, 90)


__all__ = [
    "ChatBubble",
]