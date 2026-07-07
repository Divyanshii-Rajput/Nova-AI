"""
Nova AI Desktop Assistant
-------------------------

Sidebar

Modern navigation sidebar inspired by
ChatGPT Desktop, Cursor IDE and Arc Browser.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    ABOUT_PAGE,
    BROWSER_PAGE,
    CHAT_PAGE,
    FILES_PAGE,
    HISTORY_PAGE,
    HOME_PAGE,
    ICON_20,
    MUSIC_PAGE,
    SETTINGS_PAGE,
    SIDEBAR_EXPANDED_WIDTH,
    SIDEBAR_WIDTH,
    SPACE_12,
    SPACE_16,
)
from app.ui.resources import resources


@dataclass(slots=True, frozen=True)
class NavigationItem:
    """
    Navigation metadata.
    """

    page: str

    title: str

    icon: str


class NavigationButton(QPushButton):
    """
    Sidebar navigation button.
    """

    clickedPage = Signal(str)

    def __init__(
        self,
        item: NavigationItem,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.item = item

        self.setObjectName("SidebarButton")

        self.setCursor(Qt.PointingHandCursor)

        self.setCheckable(True)

        self.setMinimumHeight(46)

        self.setIcon(
            resources.icon(item.icon)
        )

        self.setIconSize(
            QSize(
                ICON_20,
                ICON_20,
            )
        )

        self.setText(item.title)

        self.clicked.connect(
            lambda: self.clickedPage.emit(
                item.page
            )
        )


class Sidebar(QFrame):
    """
    Left navigation sidebar.
    """

    pageRequested = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("Sidebar")

        self.setFixedWidth(
            SIDEBAR_EXPANDED_WIDTH
        )

        self._buttons: dict[
            str,
            NavigationButton,
        ] = {}

        self._build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            SPACE_12,
            SPACE_16,
            SPACE_12,
            SPACE_16,
        )

        layout.setSpacing(8)

        self.logo = QLabel("Nova AI")

        self.logo.setObjectName(
            "SidebarLogo"
        )

        layout.addWidget(self.logo)

        layout.addSpacing(18)

        items = [

            NavigationItem(
                HOME_PAGE,
                "Home",
                "fa6s.house",
            ),

            NavigationItem(
                CHAT_PAGE,
                "Chat",
                "fa6s.comments",
            ),

            NavigationItem(
                BROWSER_PAGE,
                "Browser",
                "fa6s.globe",
            ),

            NavigationItem(
                FILES_PAGE,
                "Files",
                "fa6s.folder",
            ),

            NavigationItem(
                MUSIC_PAGE,
                "Music",
                "fa6s.music",
            ),

            NavigationItem(
                HISTORY_PAGE,
                "History",
                "fa6s.clock-rotate-left",
            ),
        ]

        for item in items:

            button = NavigationButton(item)

            button.clickedPage.connect(
                self.pageRequested
            )

            layout.addWidget(button)

            self._buttons[item.page] = button

        layout.addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Minimum,
                QSizePolicy.Expanding,
            )
        )

        settings = NavigationButton(

            NavigationItem(
                SETTINGS_PAGE,
                "Settings",
                "fa6s.gear",
            )

        )

        settings.clickedPage.connect(
            self.pageRequested
        )

        layout.addWidget(settings)

        self._buttons[
            SETTINGS_PAGE
        ] = settings

        about = NavigationButton(

            NavigationItem(
                ABOUT_PAGE,
                "About",
                "fa6s.circle-info",
            )

        )

        about.clickedPage.connect(
            self.pageRequested
        )

        layout.addWidget(about)

        self._buttons[
            ABOUT_PAGE
        ] = about
    
        # ==========================================================
    # Public API
    # ==========================================================

    def set_current_page(
        self,
        page: str,
    ) -> None:
        """
        Highlight the currently selected page.
        """

        for button in self._buttons.values():
            button.setChecked(False)

        current = self._buttons.get(page)

        if current is not None:
            current.setChecked(True)

    def current_page(self) -> str | None:
        """
        Return the currently selected page.
        """

        for page, button in self._buttons.items():
            if button.isChecked():
                return page

        return None

    def button(
        self,
        page: str,
    ) -> NavigationButton | None:
        """
        Return the navigation button for a page.
        """

        return self._buttons.get(page)

    def buttons(self) -> tuple[NavigationButton, ...]:
        """
        Return all navigation buttons.
        """

        return tuple(self._buttons.values())

    # ==========================================================
    # Sidebar Mode
    # ==========================================================

    def collapse(self) -> None:
        """
        Collapse the sidebar.
        """

        self.setFixedWidth(SIDEBAR_WIDTH)

        self.logo.hide()

        for button in self._buttons.values():
            button.setText("")
            button.setToolTip(button.item.title)

    def expand(self) -> None:
        """
        Expand the sidebar.
        """

        self.setFixedWidth(SIDEBAR_EXPANDED_WIDTH)

        self.logo.show()

        for button in self._buttons.values():
            button.setText(button.item.title)
            button.setToolTip("")

    def toggle(self) -> None:
        """
        Toggle sidebar expansion state.
        """

        if self.width() == SIDEBAR_WIDTH:
            self.expand()
        else:
            self.collapse()

    @property
    def is_collapsed(self) -> bool:
        """
        Returns True if the sidebar is collapsed.
        """

        return self.width() == SIDEBAR_WIDTH

    # ==========================================================
    # Utilities
    # ==========================================================

    def clear_selection(self) -> None:
        """
        Clear the current selection.
        """

        for button in self._buttons.values():
            button.setChecked(False)

    def page_count(self) -> int:
        """
        Return the number of registered pages.
        """

        return len(self._buttons)

    def __len__(self) -> int:
        return len(self._buttons)

    def __contains__(self, page: str) -> bool:
        return page in self._buttons


__all__ = [
    "NavigationItem",
    "NavigationButton",
    "Sidebar",
]