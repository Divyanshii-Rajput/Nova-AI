"""
Nova AI Desktop Assistant
-------------------------

Search Bar

Modern reusable search widget inspired by
ChatGPT Desktop, Cursor IDE and Arc Browser.

Features
--------
- Search icon
- Clear button
- Debounced search signal
- Placeholder support
- Keyboard shortcuts
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal, QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from app.ui.constants import (
    ICON_18,
    SEARCH_DEBOUNCE_MS,
    SEARCH_HEIGHT,
    SPACE_12,
)
from app.ui.resources import resources


class SearchBar(QFrame):
    """
    Reusable search widget.
    """

    searchRequested = Signal(str)

    textChangedDelayed = Signal(str)

    cleared = Signal()

    def __init__(
        self,
        placeholder: str = "Search...",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("SearchBar")

        self.setFixedHeight(SEARCH_HEIGHT)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self._timer = QTimer(self)

        self._timer.setSingleShot(True)

        self._timer.setInterval(
            SEARCH_DEBOUNCE_MS
        )

        self._timer.timeout.connect(
            self._emit_delayed
        )

        self._build_ui(placeholder)

        self._connect_signals()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(
        self,
        placeholder: str,
    ) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            SPACE_12,
            0,
            SPACE_12,
            0,
        )

        layout.setSpacing(8)

        self.searchButton = QPushButton()

        self.searchButton.setFlat(True)

        self.searchButton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.searchButton.setIcon(
            resources.icon(
                "fa6s.magnifying-glass"
            )
        )

        self.searchButton.setIconSize(
            QSize(
                ICON_18,
                ICON_18,
            )
        )

        layout.addWidget(
            self.searchButton
        )

        self.lineEdit = QLineEdit()

        self.lineEdit.setPlaceholderText(
            placeholder
        )

        self.lineEdit.setClearButtonEnabled(
            False
        )

        layout.addWidget(
            self.lineEdit
        )

        self.clearButton = QPushButton()

        self.clearButton.setFlat(True)

        self.clearButton.hide()

        self.clearButton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.clearButton.setIcon(
            resources.icon(
                "fa6s.xmark"
            )
        )

        self.clearButton.setIconSize(
            QSize(
                ICON_18,
                ICON_18,
            )
        )

        layout.addWidget(
            self.clearButton
        )

    # ======================================================
    # Signals
    # ======================================================

    def _connect_signals(self) -> None:

        self.searchButton.clicked.connect(
            self._emit_search
        )

        self.clearButton.clicked.connect(
            self.clear
        )

        self.lineEdit.returnPressed.connect(
            self._emit_search
        )

        self.lineEdit.textChanged.connect(
            self._on_text_changed
        )
    
        # ======================================================
    # Slots
    # ======================================================

    def _on_text_changed(
        self,
        text: str,
    ) -> None:
        """
        Handle text changes.
        """

        self.clearButton.setVisible(bool(text))

        self._timer.start()

    def _emit_search(self) -> None:
        """
        Emit an immediate search request.
        """

        self.searchRequested.emit(
            self.lineEdit.text().strip()
        )

    def _emit_delayed(self) -> None:
        """
        Emit the debounced text changed signal.
        """

        self.textChangedDelayed.emit(
            self.lineEdit.text().strip()
        )

    # ======================================================
    # Public API
    # ======================================================

    def text(self) -> str:
        """
        Return the current search text.
        """

        return self.lineEdit.text()

    def setText(
        self,
        text: str,
    ) -> None:
        """
        Set the search text.
        """

        self.lineEdit.setText(text)

    def placeholderText(self) -> str:
        """
        Return the placeholder text.
        """

        return self.lineEdit.placeholderText()

    def setPlaceholderText(
        self,
        text: str,
    ) -> None:
        """
        Update the placeholder text.
        """

        self.lineEdit.setPlaceholderText(text)

    def clear(self) -> None:
        """
        Clear the search field.
        """

        self.lineEdit.clear()

        self.clearButton.hide()

        self.cleared.emit()

    def setFocus(self) -> None:
        """
        Focus the input field.
        """

        self.lineEdit.setFocus()

    def selectAll(self) -> None:
        """
        Select all text.
        """

        self.lineEdit.selectAll()

    # ======================================================
    # Utilities
    # ======================================================

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(420, SEARCH_HEIGHT)

    def minimumSizeHint(self):
        return self.sizeHint()


__all__ = [
    "SearchBar",
]