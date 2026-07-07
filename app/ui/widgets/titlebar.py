"""
Nova AI Desktop Assistant
-------------------------

Custom Title Bar

Modern frameless title bar inspired by
ChatGPT Desktop, Cursor and Arc Browser.
"""

from __future__ import annotations
from PySide6.QtCore import QPoint, Qt, Signal, QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from app.ui.constants import (
    ICON_16,
    ICON_18,
    ICON_20,
    SPACE_12,
    SPACE_16,
    TITLEBAR_HEIGHT,
    WINDOW_TITLE,
)
from app.ui.resources import resources
from app.ui.signals import ui_signals


class TitleBar(QFrame):
    """
    Custom frameless title bar.
    """

    minimizeClicked = Signal()

    maximizeClicked = Signal()

    closeClicked = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._drag_position = QPoint()

        self._pressed = False

        self.setObjectName("TitleBar")

        self.setFixedHeight(TITLEBAR_HEIGHT)

        self._build_ui()

        self._connect_signals()

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            SPACE_16,
            0,
            SPACE_16,
            0,
        )

        layout.setSpacing(SPACE_12)

        # ------------------------------------------------------

        self.logoLabel = QLabel()

        self.logoLabel.setPixmap(
            resources.pixmap("logo.png")
        )

        self.logoLabel.setFixedSize(24, 24)

        layout.addWidget(self.logoLabel)

        # ------------------------------------------------------

        self.titleLabel = QLabel(WINDOW_TITLE)

        self.titleLabel.setObjectName("WindowTitle")

        layout.addWidget(self.titleLabel)

        layout.addStretch()

        # ------------------------------------------------------

        self.minButton = QPushButton()

        self.minButton.setIcon(
            resources.icon(
                "fa6s.window-minimize"
            )
        )

        self.minButton.setIconSize(
            QSize(
                ICON_16,
                ICON_16,
            )
        )

        layout.addWidget(self.minButton)

        # ------------------------------------------------------

        self.maxButton = QPushButton()

        self.maxButton.setIcon(
            resources.icon(
                "fa6s.window-maximize"
            )
        )

        self.maxButton.setIconSize(
            QSize(
                ICON_18,
                ICON_18,
            )
        )

        layout.addWidget(self.maxButton)

        # ------------------------------------------------------

        self.closeButton = QPushButton()

        self.closeButton.setObjectName(
            "CloseButton"
        )

        self.closeButton.setIcon(
            resources.icon(
                "fa6s.xmark"
            )
        )

        self.closeButton.setIconSize(
            QSize(
                ICON_20,
                ICON_20,
            )
        )

        layout.addWidget(self.closeButton)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

    # ==========================================================
    # Signals
    # ==========================================================

    def _connect_signals(self) -> None:

        self.minButton.clicked.connect(
            self._minimize
        )

        self.maxButton.clicked.connect(
            self._maximize
        )

        self.closeButton.clicked.connect(
            self._close
        )
    
        # ==========================================================
    # Slots
    # ==========================================================

    def _minimize(self) -> None:
        """
        Handle minimize action.
        """

        self.minimizeClicked.emit()

        ui_signals.minimize_requested.emit()

    def _maximize(self) -> None:
        """
        Handle maximize / restore action.
        """

        self.maximizeClicked.emit()

        ui_signals.maximize_requested.emit()

    def _close(self) -> None:
        """
        Handle close action.
        """

        self.closeClicked.emit()

        ui_signals.close_requested.emit()

    # ==========================================================
    # Public API
    # ==========================================================

    def set_title(self, title: str) -> None:
        """
        Update the window title.
        """

        self.titleLabel.setText(title)

    def title(self) -> str:
        """
        Return the current title.
        """

        return self.titleLabel.text()

    # ==========================================================
    # Mouse Events
    # ==========================================================

    def mousePressEvent(self, event) -> None:
        """
        Begin dragging the frameless window.
        """

        if event.button() == Qt.LeftButton:
            self._pressed = True
            self._drag_position = (
                event.globalPosition().toPoint()
            )

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        """
        Drag the parent window.
        """

        if (
            self._pressed
            and self.window().isWindow()
            and not self.window().isMaximized()
        ):
            delta = (
                event.globalPosition().toPoint()
                - self._drag_position
            )

            self.window().move(
                self.window().pos() + delta
            )

            self._drag_position = (
                event.globalPosition().toPoint()
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """
        Finish dragging.
        """

        self._pressed = False

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        """
        Double-click toggles maximize.
        """

        if event.button() == Qt.LeftButton:
            self._maximize()

        super().mouseDoubleClickEvent(event)


__all__ = [
    "TitleBar",
]