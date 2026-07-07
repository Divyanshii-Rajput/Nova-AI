"""
Nova AI Desktop Assistant
-------------------------

Navigation Manager

Centralized navigation controller for the desktop UI.

Responsibilities
----------------
- Page registration
- Page switching
- Navigation history
- Back/Forward navigation
- Synchronization with QStackedWidget
"""

from __future__ import annotations

import logging
from collections import deque
from typing import Dict

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QStackedWidget, QWidget

from app.ui.constants import (
    ABOUT_PAGE,
    BROWSER_PAGE,
    CHAT_PAGE,
    DEFAULT_PAGE,
    FILES_PAGE,
    HISTORY_PAGE,
    HOME_PAGE,
    MUSIC_PAGE,
    SETTINGS_PAGE,
)

logger = logging.getLogger(__name__)


class NavigationManager(QObject):
    """
    Controls navigation between application pages.
    """

    page_changed = Signal(str)

    history_changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._stack: QStackedWidget | None = None

        self._pages: Dict[str, QWidget] = {}

        self._history: deque[str] = deque()

        self._forward: deque[str] = deque()

        self._current_page: str = DEFAULT_PAGE

    # ==========================================================
    # Stack
    # ==========================================================

    def set_stack(
        self,
        stack: QStackedWidget,
    ) -> None:
        """
        Attach the application's QStackedWidget.
        """

        self._stack = stack

    @property
    def stack(self) -> QStackedWidget | None:
        return self._stack

    # ==========================================================
    # Registration
    # ==========================================================

    def register_page(
        self,
        page_id: str,
        widget: QWidget,
    ) -> None:
        """
        Register a page.
        """

        if page_id in self._pages:
            logger.warning(
                "Page '%s' already registered.",
                page_id,
            )
            return

        self._pages[page_id] = widget

        if self._stack is not None:
            self._stack.addWidget(widget)

    def unregister_page(
        self,
        page_id: str,
    ) -> None:
        """
        Remove a page from the registry.
        """

        widget = self._pages.pop(page_id, None)

        if (
            widget is not None
            and self._stack is not None
        ):
            self._stack.removeWidget(widget)

    # ==========================================================
    # Queries
    # ==========================================================

    def has_page(
        self,
        page_id: str,
    ) -> bool:
        return page_id in self._pages

    def widget(
        self,
        page_id: str,
    ) -> QWidget | None:
        return self._pages.get(page_id)

    @property
    def current_page(self) -> str:
        return self._current_page

    @property
    def pages(self) -> tuple[str, ...]:
        return tuple(self._pages.keys())

    # ==========================================================
    # Navigation
    # ==========================================================

    def navigate(
        self,
        page_id: str,
        *,
        record_history: bool = True,
    ) -> bool:
        """
        Navigate to a page.
        """

        if page_id not in self._pages:
            logger.error(
                "Unknown page '%s'.",
                page_id,
            )
            return False

        if page_id == self._current_page:
            return True

        if record_history:
            self._history.append(self._current_page)
            self._forward.clear()

        self._current_page = page_id

        if self._stack is not None:
            self._stack.setCurrentWidget(
                self._pages[page_id]
            )

        self.page_changed.emit(page_id)

        self.history_changed.emit()

        logger.info(
            "Navigated to '%s'.",
            page_id,
        )

        return True

    def home(self) -> bool:
        """
        Navigate to the Home page.
        """

        return self.navigate(HOME_PAGE)
    
    def back(self) -> bool:
        """
        Navigate to the previous page.
        """

        if not  self._history:
            return False

        previous = self._history.pop()

        self._forward.append(self._current_page)

        return self.navigate(
            previous,
            record_history=False,
        )

    def forward(self) -> bool:
        """
        Navigate to the next page in the forward history.
        """

        if not self._forward:
            return False

        page = self._forward.pop()

        self._history.append(self._current_page)

        return self.navigate(
            page,
            record_history=False,
        )

    # ==========================================================
    # History
    # ==========================================================

    def clear_history(self) -> None:
        """
        Clear navigation history.
        """

        self._history.clear()
        self._forward.clear()

        self.history_changed.emit()

    @property
    def can_go_back(self) -> bool:
        return bool(self._history)

    @property
    def can_go_forward(self) -> bool:
        return bool(self._forward)

    def history(self) -> tuple[str, ...]:
        """
        Return backward navigation history.
        """

        return tuple(self._history)

    def forward_history(self) -> tuple[str, ...]:
        """
        Return forward navigation history.
        """

        return tuple(self._forward)

    # ==========================================================
    # Utilities
    # ==========================================================

    def reset(self) -> None:
        """
        Reset the navigation manager.
        """

        self.clear_history()

        self._current_page = DEFAULT_PAGE

    def register_default_pages(self) -> None:
        """
        Validate expected page identifiers.
        Registration of widgets is performed elsewhere.
        """

        expected_pages = (
            HOME_PAGE,
            CHAT_PAGE,
            BROWSER_PAGE,
            FILES_PAGE,
            MUSIC_PAGE,
            SETTINGS_PAGE,
            HISTORY_PAGE,
            ABOUT_PAGE,
        )

        for page in expected_pages:
            logger.debug("Expected page: %s", page)

    def __contains__(self, page_id: str) -> bool:
        return page_id in self._pages

    def __len__(self) -> int:
        return len(self._pages)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"pages={len(self)}, "
            f"current='{self._current_page}')"
        )


# ==========================================================
# Singleton
# ==========================================================

navigation_manager = NavigationManager()


def get_navigation_manager() -> NavigationManager:
    """
    Return the global NavigationManager instance.
    """

    return navigation_manager


__all__ = [
    "NavigationManager",
    "navigation_manager",
    "get_navigation_manager",
]