"""
Nova AI Desktop Assistant
-------------------------

Files Page

Desktop file management interface.

Responsibilities
----------------
- Search files
- Display search results
- Preview selected files
- Execute file operations

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
    QSplitter,
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
from app.files.file_engine import FileEngine

class FilesPage(QWidget):
    """
    File manager page.
    """

    fileOpened = Signal(str)

    fileSelected = Signal(str)

    searchRequested = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)
        self.engine = FileEngine()

        self.setObjectName("FilesPage")

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

        self.searchBar = SearchBar(
            "Search files..."
        )

        root.addWidget(self.searchBar)

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        root.addWidget(splitter)

        # ==================================================
        # File List
        # ==================================================

        left = QWidget()

        left_layout = QVBoxLayout(left)

        left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        left_layout.setSpacing(
            SPACE_12
        )

        self.fileList = QListWidget()

        left_layout.addWidget(
            self.fileList
        )

        self.openButton = QPushButton(
            "Open"
        )

        self.openButton.setIcon(
            resources.icon(
                "fa6s.folder-open"
            )
        )

        left_layout.addWidget(
            self.openButton
        )

        splitter.addWidget(left)

        # ==================================================
        # Preview
        # ==================================================

        right = QWidget()

        right_layout = QVBoxLayout(
            right
        )

        right_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        right_layout.setSpacing(
            SPACE_12
        )

        self.previewTitle = QLabel(
            "Preview"
        )

        self.previewTitle.setObjectName(
            "SectionTitle"
        )

        right_layout.addWidget(
            self.previewTitle
        )

        self.preview = QTextEdit()

        self.preview.setReadOnly(True)

        self.preview.setPlaceholderText(
            "Select a file to preview..."
        )

        right_layout.addWidget(
            self.preview
        )

        splitter.addWidget(right)

        splitter.setStretchFactor(0, 1)

        splitter.setStretchFactor(1, 2)

        # ==================================================
        # Signals
        # ==================================================

        self.searchBar.searchRequested.connect(
            self._search
        )

        self.fileList.itemClicked.connect(
            self._item_selected
        )

        self.fileList.itemDoubleClicked.connect(
            self._item_opened
        )

        self.openButton.clicked.connect(
            self._open_selected
        )
    
        # ======================================================
    # Slots
    # ======================================================

    def _item_selected(
        self,
        item: QListWidgetItem,
    ) -> None:
        """
        Handle file selection.
        """

        file = item.data(Qt.ItemDataRole.UserRole)

        if file is None:
            return

        self.fileSelected.emit(file.path)

        self.set_preview(
            f"""Name      : {file.name}

    Path      : {file.path}

    Extension : {file.extension}

    Directory : {file.directory}"""
        )

    def _item_opened(
        self,
        item: QListWidgetItem,
    ) -> None:
        """
        Handle double-click.
        """

        file = item.data(Qt.ItemDataRole.UserRole)

        if file is None:
            return

        self.engine._open_file(file)
        
    def _open_selected(self) -> None:
        """
        Open the currently selected file.
        """

        item = self.fileList.currentItem()

        if item is None:
            return

        file = item.data(Qt.ItemDataRole.UserRole)

        if file is None:
            return

        self.engine._open_file(file)

    def _search(
        self,
        query: str,
    ) -> None:

        query = query.strip()

        if not query:
            return

        self.clear_files()

        results = self.engine.search(query)

        if not results:

            self.clear_files()

            self.set_preview(
                "No matching files found."
            )

            return

        for file in results:

            item = QListWidgetItem(file.name)
            item.setData(Qt.ItemDataRole.UserRole, file)
            self.fileList.addItem(item)

        self.set_preview(
            f"{len(results)} file(s) found."
        )
    
    
    # ======================================================
    # Public API
    # ======================================================

    # def add_file(
    #     self,
    #     filename: str,
    # ) -> None:
    #     """
    #     Add a file to the list.
    #     """

    #     self.fileList.addItem(filename)

    # def add_files(
    #     self,
    #     filenames: list[str],
    # ) -> None:
    #     """
    #     Add multiple files.
    #     """

    #     self.fileList.addItems(filenames)

    def clear_files(self) -> None:
        """
        Remove all listed files.
        """

        self.fileList.clear()

    def set_preview(
        self,
        text: str,
    ) -> None:
        """
        Update the preview pane.
        """

        self.preview.setPlainText(text)

    def selected_file(self) -> str | None:
        """
        Return the currently selected filename.
        """

        item = self.fileList.currentItem()

        return item.text() if item else None

    def file_count(self) -> int:
        """
        Return the number of displayed files.
        """

        return self.fileList.count()

    def clear_preview(self) -> None:
        """
        Clear the preview area.
        """

        self.preview.clear()

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
    "FilesPage",
]