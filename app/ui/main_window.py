"""
Nova AI Desktop Assistant
-------------------------

Main Window

Primary application window.

Responsibilities
----------------
- Own application pages
- Manage navigation
- Host title bar
- Host sidebar
- Coordinate UI interactions
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    ABOUT_PAGE,
    BROWSER_PAGE,
    CHAT_PAGE,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    FILES_PAGE,
    HISTORY_PAGE,
    MINIMUM_WINDOW_HEIGHT,
    MINIMUM_WINDOW_WIDTH,
    MUSIC_PAGE,
    SETTINGS_PAGE,
    WINDOW_TITLE,
    HOME_PAGE,
)

from app.ui.navigation import navigation_manager
from app.ui.signals import ui_signals

from app.ui.widgets.sidebar import Sidebar
from app.ui.widgets.titlebar import TitleBar

from app.ui.pages.home_page import HomePage
from app.ui.pages.chat_page import ChatPage
from app.ui.pages.browser_page import BrowserPage
from app.ui.pages.files_page import FilesPage
from app.ui.pages.music_page import MusicPage
from app.ui.pages.history_page import HistoryPage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.about_page import AboutPage

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Nova application's main window.
    """

    def __init__(self) -> None:
        super().__init__()

        self._central_widget = None
        self._main_layout = None

        self._sidebar = None
        self._title_bar = None

        self._stack = None

        self._initialize_window()
        self._create_ui()
        self._register_pages()
        self._connect_signals()

        navigation_manager.navigate(
            HOME_PAGE
        )

    # ==========================================================
    # Window
    # ==========================================================

    def _initialize_window(self) -> None:
        self.setWindowTitle(
            WINDOW_TITLE
        )

        self.resize(
            DEFAULT_WINDOW_WIDTH,
            DEFAULT_WINDOW_HEIGHT,
        )

        self.setMinimumSize(
            MINIMUM_WINDOW_WIDTH,
            MINIMUM_WINDOW_HEIGHT,
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

    # ==========================================================
    # UI Creation
    # ==========================================================

    def _create_ui(self) -> None:

        self._central_widget = QWidget()

        self.setCentralWidget(
            self._central_widget
        )

        self._main_layout = QVBoxLayout(
            self._central_widget
        )

        self._main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self._main_layout.setSpacing(
            0
        )

        # Title bar

        self._title_bar = TitleBar()

        self._main_layout.addWidget(
            self._title_bar
        )


        # Body

        body = QWidget()

        body_layout = QHBoxLayout(
            body
        )

        body_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        body_layout.setSpacing(
            0
        )


        # Sidebar

        self._sidebar = Sidebar()

        body_layout.addWidget(
            self._sidebar
        )


        # Pages

        self._stack = QStackedWidget()

        navigation_manager.set_stack(
            self._stack
        )

        body_layout.addWidget(
            self._stack
        )


        self._main_layout.addWidget(
            body
        )


        logger.info(
            "Main window UI created."
        )


    # ==========================================================
    # Pages
    # ==========================================================

    def _register_pages(self) -> None:
        """
        Register all application pages.
        """

        self.pages = {

            HOME_PAGE: HomePage(),

            CHAT_PAGE: ChatPage(),

            BROWSER_PAGE: BrowserPage(),

            FILES_PAGE: FilesPage(),

            MUSIC_PAGE: MusicPage(),

            HISTORY_PAGE: HistoryPage(),

            SETTINGS_PAGE: SettingsPage(),

            ABOUT_PAGE: AboutPage(),

        }

        for page_id, widget in self.pages.items():

            navigation_manager.register_page(
                page_id,
                widget,
            )


    # ==========================================================
    # Signals
    # ==========================================================

    def _connect_signals(self) -> None:

        self._sidebar.pageRequested.connect(
            navigation_manager.navigate
        )

        navigation_manager.page_changed.connect(
            self._on_page_changed
        )


        ui_signals.minimize_requested.connect(
            self.showMinimized
        )

        ui_signals.maximize_requested.connect(
            self._toggle_maximize
        )

        ui_signals.restore_requested.connect(
            self.showNormal
        )

        ui_signals.close_requested.connect(
            self.close
        )


    # ==========================================================
    # Navigation
    # ==========================================================

    def add_page(
        self,
        page_id: str,
        widget: QWidget,
    ) -> None:

        navigation_manager.register_page(
            page_id,
            widget,
        )


    def navigate(
        self,
        page_id: str,
    ) -> bool:

        return navigation_manager.navigate(
            page_id
        )


    def current_page(self) -> str:

        return navigation_manager.current_page


    # ==========================================================
    # Slots
    # ==========================================================

    def _on_page_changed(
        self,
        page_id: str,
    ) -> None:

        if self._sidebar:
            self._sidebar.set_current_page(
                page_id
            )

        # Refresh history whenever user opens it
        if page_id == HISTORY_PAGE:

            history_page = self.pages[HISTORY_PAGE]

            history_page.refresh()

        logger.info(
            "Current page: %s",
            page_id,
        )


    def _toggle_maximize(self) -> None:

        if self.isMaximized():
            self.showNormal()

        else:
            self.showMaximized()


    # ==========================================================
    # Events
    # ==========================================================

    def closeEvent(
        self,
        event,
    ) -> None:

        ui_signals.application_closing.emit()

        super().closeEvent(
            event
        )

        ui_signals.application_closed.emit()


    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def stacked_widget(self):

        return self._stack


    @property
    def sidebar(self):

        return self._sidebar


    @property
    def title_bar(self):

        return self._title_bar


__all__ = [
    "MainWindow",
]