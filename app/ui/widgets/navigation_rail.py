"""
Nova AI Desktop Assistant
-------------------------

Navigation Rail

Compact icon-only navigation rail used when the sidebar
is collapsed. Designed for quick navigation while
maximizing content space.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
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
    SIDEBAR_WIDTH,
    SPACE_12,
    SPACE_16,
)
from app.ui.resources import resources


@dataclass(slots=True, frozen=True)
class RailItem:
    """Navigation rail item."""

    page: str
    tooltip: str
    icon: str


class RailButton(QPushButton):
    """Single navigation rail button."""

    pageRequested = Signal(str)

    def __init__(
        self,
        item: RailItem,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.item = item

        self.setObjectName("NavigationRailButton")

        self.setCursor(Qt.PointingHandCursor)

        self.setCheckable(True)

        self.setToolTip(item.tooltip)

        self.setFixedSize(48, 48)

        self.setIcon(resources.icon(item.icon))

        self.setIconSize(Qt.QSize(ICON_20, ICON_20))

        self.clicked.connect(
            lambda: self.pageRequested.emit(item.page)
        )


class NavigationRail(QFrame):
    """
    Compact icon-only navigation rail.
    """

    pageRequested = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("NavigationRail")

        self.setFixedWidth(SIDEBAR_WIDTH)

        self._buttons: dict[str, RailButton] = {}

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

        layout.setSpacing(10)

        items = [

            RailItem(
                HOME_PAGE,
                "Home",
                "fa6s.house",
            ),

            RailItem(
                CHAT_PAGE,
                "Chat",
                "fa6s.comments",
            ),

            RailItem(
                BROWSER_PAGE,
                "Browser",
                "fa6s.globe",
            ),

            RailItem(
                FILES_PAGE,
                "Files",
                "fa6s.folder",
            ),

            RailItem(
                MUSIC_PAGE,
                "Videos",
                "fa6s.video",
            ),

            RailItem(
                HISTORY_PAGE,
                "History",
                "fa6s.clock-rotate-left",
            ),
        ]

        for item in items:

            button = RailButton(item)

            button.pageRequested.connect(
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

        settings = RailButton(
            RailItem(
                SETTINGS_PAGE,
                "Settings",
                "fa6s.gear",
            )
        )

        settings.pageRequested.connect(
            self.pageRequested
        )

        layout.addWidget(settings)

        self._buttons[SETTINGS_PAGE] = settings

        about = RailButton(
            RailItem(
                ABOUT_PAGE,
                "About",
                "fa6s.circle-info",
            )
        )

        about.pageRequested.connect(
            self.pageRequested
        )

        layout.addWidget(about)

        self._buttons[ABOUT_PAGE] = about
    
        # ==========================================================
    # Public API
    # ==========================================================

    def set_current_page(
        self,
        page: str,
    ) -> None:
        """
        Highlight the currently active page.
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
    ) -> RailButton | None:
        """
        Return the button associated with a page.
        """

        return self._buttons.get(page)

    def buttons(self) -> tuple[RailButton, ...]:
        """
        Return all rail buttons.
        """

        return tuple(self._buttons.values())

    # ==========================================================
    # Selection
    # ==========================================================

    def clear_selection(self) -> None:
        """
        Clear the current page selection.
        """

        for button in self._buttons.values():
            button.setChecked(False)

    # ==========================================================
    # Utilities
    # ==========================================================

    def page_count(self) -> int:
        """
        Return the number of registered pages.
        """

        return len(self._buttons)

    def has_page(
        self,
        page: str,
    ) -> bool:
        """
        Check whether a page exists.
        """

        return page in self._buttons

    def __contains__(self, page: str) -> bool:
        return page in self._buttons

    def __len__(self) -> int:
        return len(self._buttons)

    def __iter__(self):
        return iter(self._buttons.values())


__all__ = [
    "RailItem",
    "RailButton",
    "NavigationRail",
]