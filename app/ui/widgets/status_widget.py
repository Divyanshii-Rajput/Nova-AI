"""
Nova AI Desktop Assistant
-------------------------

Status Widget

Displays the current assistant status.

Examples:
- Ready
- Listening...
- Thinking...
- Speaking...
- Executing...
- Error

Supports animated busy indicator and status icon.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from app.ui.constants import (
    ICON_18,
    SPACE_12,
    SPACE_16,
    STATUS_WIDGET_HEIGHT,
)

from app.ui.resources import resources


class StatusWidget(QFrame):
    """
    Assistant status widget.
    """

    clicked = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName(
            "StatusWidget"
        )

        self.setFixedHeight(
            STATUS_WIDGET_HEIGHT
        )

        self._status = "Ready"

        self._busy = False

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            SPACE_16,
            0,
            SPACE_16,
            0,
        )

        layout.setSpacing(
            SPACE_12
        )

        self.iconLabel = QLabel()

        self.iconLabel.setPixmap(
            resources.icon(
                "fa6s.circle-check",
                color="#2ECC71",
            ).pixmap(
                ICON_18,
                ICON_18,
            )
        )

        layout.addWidget(
            self.iconLabel
        )

        self.statusLabel = QLabel(
            self._status
        )

        self.statusLabel.setObjectName(
            "StatusText"
        )

        layout.addWidget(
            self.statusLabel
        )

        layout.addStretch()

        self.activityLabel = QLabel()

        self.activityLabel.hide()

        layout.addWidget(
            self.activityLabel
        )

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

    # ======================================================
    # Status
    # ======================================================

    def setStatus(
        self,
        text: str,
    ) -> None:

        self._status = text

        self.statusLabel.setText(
            text
        )


    def status(self) -> str:

        return self._status


    def setBusy(
        self,
        busy: bool,
    ) -> None:

        self._busy = busy

        self.activityLabel.setVisible(
            busy
        )

        if busy:

            self.activityLabel.setPixmap(
                resources.icon(
                    "fa6s.spinner",
                    color="#5B8CFF",
                ).pixmap(
                    ICON_18,
                    ICON_18,
                )
            )

        else:

            self.activityLabel.clear()


    def isBusy(self) -> bool:
        """
        Return current busy state.
        """

        return self._busy


    # ======================================================
    # Preset States
    # ======================================================

    def setReady(self) -> None:

        self.setStatus(
            "Ready"
        )

        self.setBusy(
            False
        )


    def setListening(self) -> None:

        self.setStatus(
            "Listening..."
        )

        self.setBusy(
            True
        )


    def setThinking(self) -> None:

        self.setStatus(
            "Thinking..."
        )

        self.setBusy(
            True
        )


    def setSpeaking(self) -> None:

        self.setStatus(
            "Speaking..."
        )

        self.setBusy(
            True
        )


    def setError(
        self,
        message: str = "Error",
    ) -> None:

        self.setStatus(
            message
        )

        self.setBusy(
            False
        )


    # ======================================================
    # Events
    # ======================================================

    def mousePressEvent(
        self,
        event,
    ) -> None:

        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(
            event
        )


    # ======================================================
    # Utilities
    # ======================================================

    def reset(self) -> None:

        self.setReady()


    def sizeHint(self):

        from PySide6.QtCore import QSize

        return QSize(
            280,
            STATUS_WIDGET_HEIGHT,
        )


    def minimumSizeHint(self):

        return self.sizeHint()


__all__ = [
    "StatusWidget",
]