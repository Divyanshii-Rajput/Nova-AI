"""
Nova AI Desktop Assistant
-------------------------

History Page

Displays previous assistant interactions.

Responsibilities
----------------
- Conversation history
- Search history
- Session history
- Clear history
- Open previous conversations

Backend integration is implemented in Sprint 5.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    PAGE_SPACING,
    SPACE_12,
    SPACE_16,
)
from app.ui.resources import resources
from app.ui.widgets.search_bar import SearchBar
from app.memory.conversation_memory import conversation_memory

class HistoryPage(QWidget):
    """
    Assistant history page.
    """

    historySelected = Signal(str)

    clearRequested = Signal()

    searchRequested = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)
        self.memory = conversation_memory
        self.setObjectName("HistoryPage")

        self._build_ui()
        self.refresh()

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

        self.searchBar = SearchBar(
            "Search history..."
        )

        root.addWidget(
            self.searchBar
        )

        body = QHBoxLayout()

        body.setSpacing(
            SPACE_12
        )

        # ==================================================
        # History List
        # ==================================================

        self.historyList = QListWidget()

        body.addWidget(
            self.historyList,
            1,
        )

        # ==================================================
        # Preview
        # ==================================================

        preview = QFrame()

        previewLayout = QVBoxLayout(
            preview
        )

        previewLayout.setContentsMargins(
            SPACE_16,
            SPACE_16,
            SPACE_16,
            SPACE_16,
        )

        self.titleLabel = QLabel(
            "Conversation"
        )

        self.titleLabel.setObjectName(
            "SectionTitle"
        )

        previewLayout.addWidget(
            self.titleLabel
        )

        self.previewText = QTextEdit()

        self.previewText.setReadOnly(True)

        self.previewText.setPlaceholderText(
            "Select a conversation..."
        )

        previewLayout.addWidget(
            self.previewText
        )

        body.addWidget(
            preview,
            2,
        )

        root.addLayout(
            body
        )

        # ==================================================
        # Bottom Bar
        # ==================================================

        bottom = QHBoxLayout()

        self.clearButton = QPushButton(
            "Clear History"
        )

        self.clearButton.setIcon(
            resources.icon(
                "fa6s.trash"
            )
        )

        bottom.addStretch()

        bottom.addWidget(
            self.clearButton
        )

        root.addLayout(
            bottom
        )

        # ==================================================
        # Signals
        # ==================================================

        self.searchBar.searchRequested.connect(
            self.searchRequested
        )

        self.historyList.itemClicked.connect(
            self._history_selected
        )

        self.clearButton.clicked.connect(
            self._clear
        )
    
    # ======================================================
    # Slots
    # ======================================================

    def _clear(self):

        self.memory.clear()

        self.clear_history()

        self.previewText.setPlainText(
            "No conversation history available."
        )
        
        
    def _history_selected(
        self,
        item: QListWidgetItem,
    ) -> None:
        """
        Display the selected conversation.
        """

        index = self.historyList.row(item)

        history = self.memory.all()

        if index >= len(history):
            return

        conversation = history[index]

        self.set_preview(
            f"""👤 User

    {conversation.user}

    🤖 Nova

    {conversation.assistant}
    """
        )

    # ======================================================
    # Public API
    # ======================================================

    def add_history(
        self,
        title: str,
    ) -> None:
        """
        Add a history entry.
        """

        self.historyList.addItem(title)

    def add_histories(
        self,
        entries: list[str],
    ) -> None:
        """
        Add multiple history entries.
        """

        self.historyList.addItems(entries)

    def clear_history(self) -> None:
        """
        Remove all history entries.
        """

        self.historyList.clear()

        self.previewText.clear()

    def set_preview(
        self,
        text: str,
    ) -> None:
        """
        Display the selected conversation.
        """

        self.previewText.setPlainText(text)

    def selected_history(self) -> str | None:
        """
        Return the selected history item.
        """

        item = self.historyList.currentItem()

        return item.text() if item else None

    def history_count(self) -> int:
        """
        Return the number of history entries.
        """

        return self.historyList.count()

    def remove_selected(self) -> None:
        """
        Remove the currently selected history entry.
        """

        row = self.historyList.currentRow()

        if row >= 0:
            self.historyList.takeItem(row)
    
    def refresh(self):

        self.clear_history()

        history = self.memory.all()

        if not history:

            self.previewText.setPlainText(
                "No conversation history available."
            )

            return

        for conversation in history:

            self.add_history(
                conversation.title
            )

        self.previewText.setPlainText(
            "Select a conversation to view."
        )

    # ======================================================
    # Utilities
    # ======================================================

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(1200, 800)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(900, 600)


__all__ = [
    "HistoryPage",
]