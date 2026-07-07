"""
Nova AI Desktop Assistant
-------------------------

Modern Chat Bubble

Uses QLabel instead of QTextBrowser for
correct automatic sizing.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    CHAT_AVATAR_SIZE,
    CHAT_MARGIN,
    CHAT_SPACING,
    ICON_16,
    SPACE_8,
    SPACE_12,
)

from app.ui.resources import resources


class ChatBubble(QFrame):

    def __init__(
        self,
        message: str,
        *,
        is_user: bool,
        timestamp: datetime | None = None,
        parent: QWidget | None = None,
    ):

        super().__init__(parent)

        self._message = message
        self._is_user = is_user
        self._timestamp = timestamp or datetime.now()

        self.setFrameShape(QFrame.Shape.NoFrame)

        self.setObjectName(
            "UserBubble"
            if is_user
            else "AssistantBubble"
        )

        self._build_ui()

    # -------------------------------------------------

    def _build_ui(self):

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
                    "fa6s.user"
                ).pixmap(
                    CHAT_AVATAR_SIZE,
                    CHAT_AVATAR_SIZE,
                )
            )

        else:

            avatar.setPixmap(
                resources.icon(
                    "fa6s.robot"
                ).pixmap(
                    CHAT_AVATAR_SIZE,
                    CHAT_AVATAR_SIZE,
                )
            )

        bubble = QFrame()

        bubble.setObjectName(
            "BubbleContainer"
        )

        bubble.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

        layout = QVBoxLayout(bubble)

        layout.setContentsMargins(
            SPACE_12,
            SPACE_12,
            SPACE_12,
            SPACE_12,
        )

        layout.setSpacing(8)

        self.messageLabel = QLabel(
            self._message
        )

        self.messageLabel.setWordWrap(True)

        self.messageLabel.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.messageLabel.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

        self.messageLabel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout.addWidget(
            self.messageLabel
        )

        footer = QHBoxLayout()

        self.timeLabel = QLabel(
            self._timestamp.strftime("%H:%M")
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

        layout.addLayout(
            footer
        )

        if self._is_user:

            root.addStretch()

            root.addWidget(
                bubble,
                1,
            )

            root.addWidget(
                avatar
            )

        else:

            root.addWidget(
                avatar
            )

            root.addWidget(
                bubble,
                1,
            )

            root.addStretch()

        self.copyButton.clicked.connect(
            self.copyMessage
        )
    
        # ======================================================
    # Public API
    # ======================================================

    def message(self) -> str:
        """
        Return current message.
        """
        return self._message

    def setMessage(
        self,
        message: str,
    ) -> None:
        """
        Replace message.
        """

        self._message = message

        self.messageLabel.setText(
            message
        )

        self.updateGeometry()

    def appendMessage(
        self,
        text: str,
    ) -> None:
        """
        Append streamed text.
        """

        self._message += text

        self.messageLabel.setText(
            self._message
        )

        self.updateGeometry()

    def isUser(self) -> bool:
        """
        Returns True if this is a user bubble.
        """

        return self._is_user

    def setTimestamp(
        self,
        timestamp: datetime,
    ) -> None:

        self._timestamp = timestamp

        self.timeLabel.setText(
            timestamp.strftime("%H:%M")
        )

    # ======================================================
    # Actions
    # ======================================================

    def copyMessage(self) -> None:
        """
        Copy message to clipboard.
        """

        QApplication.clipboard().setText(
            self._message
        )

    # ======================================================
    # Appearance
    # ======================================================

    def setSelectable(
        self,
        enabled: bool,
    ) -> None:

        self.messageLabel.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            if enabled
            else Qt.TextInteractionFlag.NoTextInteraction
        )

    def setReadOnly(
        self,
        read_only: bool,
    ) -> None:
        """
        Compatibility with previous API.
        QLabel is always read-only.
        """
        return

    # ======================================================
    # Utilities
    # ======================================================

    def clear(self) -> None:

        self._message = ""

        self.messageLabel.clear()

    def sizeHint(self) -> QSize:

        hint = self.messageLabel.sizeHint()

        return QSize(
            min(
                max(
                    hint.width() + 60,
                    320,
                ),
                700,
            ),
            hint.height() + 70,
        )

    def minimumSizeHint(self) -> QSize:

        hint = self.messageLabel.sizeHint()

        return QSize(
            320,
            hint.height() + 70,
        )


__all__ = [
    "ChatBubble",
]