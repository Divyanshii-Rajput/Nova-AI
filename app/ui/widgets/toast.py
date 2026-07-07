"""
Nova AI Desktop Assistant
-------------------------

Toast Notification Widget

Modern floating toast notification inspired by
Windows 11, ChatGPT Desktop and Arc Browser.

Features
--------
- Success / Error / Warning / Info
- Auto dismiss
- Manual close
- Queue friendly
- Fade ready
"""

from __future__ import annotations

from enum import Enum

from PySide6.QtCore import (
    QTimer,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    ICON_16,
    SPACE_12,
    SPACE_16,
    TOAST_DURATION,
    TOAST_HEIGHT,
    TOAST_WIDTH,
)
from app.ui.resources import resources


class ToastType(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Toast(QFrame):
    """
    Floating toast notification widget.
    """

    closed = Signal()

    def __init__(
        self,
        message: str,
        toast_type: ToastType = ToastType.INFO,
        duration: int = TOAST_DURATION,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._message = message

        self._type = toast_type

        self._duration = duration

        self.setObjectName("Toast")

        self.setFixedSize(
            TOAST_WIDTH,
            TOAST_HEIGHT,
        )

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed,
        )

        self._timer = QTimer(self)

        self._timer.setSingleShot(True)

        self._timer.timeout.connect(self.closeToast)

        self._build_ui()

        self._apply_type()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            SPACE_16,
            SPACE_12,
            SPACE_16,
            SPACE_12,
        )

        layout.setSpacing(SPACE_12)

        self.iconLabel = QLabel()

        layout.addWidget(self.iconLabel)

        content = QVBoxLayout()

        self.messageLabel = QLabel(self._message)

        self.messageLabel.setWordWrap(True)

        self.messageLabel.setObjectName(
            "ToastMessage"
        )

        content.addWidget(self.messageLabel)

        layout.addLayout(content)

        layout.addStretch()

        self.closeButton = QPushButton()

        self.closeButton.setFlat(True)

        self.closeButton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.closeButton.setIcon(
            resources.icon("fa6s.xmark")
        )

        self.closeButton.setIconSize(
            Qt.QSize(
                ICON_16,
                ICON_16,
            )
        )

        self.closeButton.clicked.connect(
            self.closeToast
        )

        layout.addWidget(self.closeButton)

    # ======================================================
    # Appearance
    # ======================================================

    def _apply_type(self) -> None:

        if self._type == ToastType.SUCCESS:

            icon = "fa6s.circle-check"
            color = "#2ECC71"

        elif self._type == ToastType.WARNING:

            icon = "fa6s.triangle-exclamation"
            color = "#F4B400"

        elif self._type == ToastType.ERROR:

            icon = "fa6s.circle-exclamation"
            color = "#FF5C5C"

        else:

            icon = "fa6s.circle-info"
            color = "#5B8CFF"

        self.iconLabel.setPixmap(

            resources.icon(
                icon,
                color=color,
            ).pixmap(
                20,
                20,
            )

        )
    
        # ======================================================
    # Public API
    # ======================================================

    def showToast(self) -> None:
        """
        Show the toast notification.
        """

        self.show()

        if self._duration > 0:
            self._timer.start(self._duration)

    def closeToast(self) -> None:
        """
        Close the toast notification.
        """

        self._timer.stop()

        self.hide()

        self.closed.emit()

    def setMessage(
        self,
        message: str,
    ) -> None:
        """
        Update the toast message.
        """

        self._message = message

        self.messageLabel.setText(message)

    def message(self) -> str:
        """
        Return the current message.
        """

        return self._message

    def setType(
        self,
        toast_type: ToastType,
    ) -> None:
        """
        Update the toast type.
        """

        self._type = toast_type

        self._apply_type()

    def toastType(self) -> ToastType:
        """
        Return the current toast type.
        """

        return self._type

    def setDuration(
        self,
        duration: int,
    ) -> None:
        """
        Set auto-dismiss duration in milliseconds.
        """

        self._duration = max(0, duration)

    def duration(self) -> int:
        """
        Return the current auto-dismiss duration.
        """

        return self._duration

    # ======================================================
    # Events
    # ======================================================

    def enterEvent(self, event) -> None:
        """
        Pause auto-dismiss while hovered.
        """

        if self._timer.isActive():
            self._timer.stop()

        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """
        Resume auto-dismiss after hover.
        """

        if self._duration > 0:
            self._timer.start(self._duration)

        super().leaveEvent(event)

    # ======================================================
    # Utilities
    # ======================================================

    def reset(self) -> None:
        """
        Restore the default state.
        """

        self._timer.stop()

        self._message = ""

        self.messageLabel.clear()

        self.setType(ToastType.INFO)

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(
            TOAST_WIDTH,
            TOAST_HEIGHT,
        )

    def minimumSizeHint(self):
        return self.sizeHint()


__all__ = [
    "Toast",
    "ToastType",
]