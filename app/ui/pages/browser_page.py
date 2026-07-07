"""
Nova AI Desktop Assistant
-------------------------

Browser Page

Embedded browser interface.

Responsibilities
----------------
- Address/search bar
- Navigation controls
- Browser content area
- Loading indicator
- Browser actions

The backend/browser engine is integrated in Sprint 5.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
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
    PAGE_SPACING,
    SPACE_12,
    SPACE_16,
)
from app.ui.resources import resources
from app.ui.widgets.loading_indicator import (
    LoadingIndicator,
)
from app.ui.widgets.search_bar import (
    SearchBar,
)


class BrowserPage(QWidget):
    """
    Browser page UI.
    """

    backRequested = Signal()

    forwardRequested = Signal()

    refreshRequested = Signal()

    homeRequested = Signal()

    urlRequested = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("BrowserPage")

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

        # ==================================================
        # Toolbar
        # ==================================================

        toolbar = QHBoxLayout()

        toolbar.setSpacing(
            SPACE_12
        )

        self.backButton = QPushButton()

        self.backButton.setIcon(
            resources.icon(
                "fa6s.arrow-left"
            )
        )

        toolbar.addWidget(
            self.backButton
        )

        self.forwardButton = QPushButton()

        self.forwardButton.setIcon(
            resources.icon(
                "fa6s.arrow-right"
            )
        )

        toolbar.addWidget(
            self.forwardButton
        )

        self.refreshButton = QPushButton()

        self.refreshButton.setIcon(
            resources.icon(
                "fa6s.rotate-right"
            )
        )

        toolbar.addWidget(
            self.refreshButton
        )

        self.homeButton = QPushButton()

        self.homeButton.setIcon(
            resources.icon(
                "fa6s.house"
            )
        )

        toolbar.addWidget(
            self.homeButton
        )

        self.searchBar = SearchBar(
            "Search or enter URL..."
        )

        toolbar.addWidget(
            self.searchBar
        )

        root.addLayout(
            toolbar
        )

        # ==================================================
        # Content
        # ==================================================

        self.browserFrame = QFrame()

        self.browserFrame.setObjectName(
            "BrowserFrame"
        )

        content = QVBoxLayout(
            self.browserFrame
        )

        content.setContentsMargins(
            SPACE_16,
            SPACE_16,
            SPACE_16,
            SPACE_16,
        )

        content.setSpacing(
            SPACE_16
        )

        self.placeholder = QLabel(
            "Browser engine will be connected during Sprint 5."
        )

        self.placeholder.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        content.addStretch()

        content.addWidget(
            self.placeholder
        )

        self.loadingIndicator = (
            LoadingIndicator(
                "Loading page..."
            )
        )

        self.loadingIndicator.hide()

        content.addWidget(
            self.loadingIndicator,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        content.addStretch()

        root.addWidget(
            self.browserFrame
        )

        # ==================================================
        # Signals
        # ==================================================

        self.backButton.clicked.connect(
            self.backRequested
        )

        self.forwardButton.clicked.connect(
            self.forwardRequested
        )

        self.refreshButton.clicked.connect(
            self.refreshRequested
        )

        self.homeButton.clicked.connect(
            self.homeRequested
        )

        self.searchBar.searchRequested.connect(
            self.urlRequested
        )
    
        # ======================================================
    # Public API
    # ======================================================

    def set_loading(
        self,
        loading: bool,
    ) -> None:
        """
        Show or hide the loading indicator.
        """

        self.loadingIndicator.setVisible(loading)

        if loading:
            self.loadingIndicator.start()
        else:
            self.loadingIndicator.stop()

    def set_placeholder_text(
        self,
        text: str,
    ) -> None:
        """
        Update the placeholder message.
        """

        self.placeholder.setText(text)

    def current_query(self) -> str:
        """
        Return the current search/URL text.
        """

        return self.searchBar.text()

    def set_query(
        self,
        text: str,
    ) -> None:
        """
        Update the search bar contents.
        """

        self.searchBar.setText(text)

    def set_navigation_enabled(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable navigation controls.
        """

        self.backButton.setEnabled(enabled)
        self.forwardButton.setEnabled(enabled)
        self.refreshButton.setEnabled(enabled)
        self.homeButton.setEnabled(enabled)
        self.searchBar.setEnabled(enabled)

    def clear(self) -> None:
        """
        Reset the browser page.
        """

        self.searchBar.clear()

        self.set_loading(False)

        self.placeholder.setText(
            "Browser engine will be connected during Sprint 5."
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
    "BrowserPage",
]