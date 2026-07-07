"""
Nova AI Desktop Assistant
-------------------------

Application bootstrap.

Responsible for:

- QApplication creation
- High DPI initialization
- Theme initialization
- Thread manager initialization
- Resource loading
- Main window startup
"""

from __future__ import annotations

import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from app.ui.constants import (
    APP_NAME,
    APP_VERSION,
    ENABLE_HIGH_DPI,
)
from app.ui.resources import resources
from app.ui.theme import theme_manager
from app.ui.thread_manager import thread_manager

logger = logging.getLogger(__name__)


class NovaApplication:
    """
    Main Qt application bootstrap.
    """

    def __init__(self) -> None:
        self._app: QApplication | None = None

    # ==========================================================
    # QApplication
    # ==========================================================

    def create(self) -> QApplication:
        """
        Create and configure QApplication.
        """

        if QApplication.instance() is not None:
            self._app = QApplication.instance()
            return self._app

        if ENABLE_HIGH_DPI:
            QApplication.setAttribute(
                Qt.ApplicationAttribute.AA_EnableHighDpiScaling,
                True,
            )

            QApplication.setAttribute(
                Qt.ApplicationAttribute.AA_UseHighDpiPixmaps,
                True,
            )

        app = QApplication(sys.argv)

        app.setApplicationName(APP_NAME)

        app.setApplicationVersion(APP_VERSION)

        app.setOrganizationName("Nova")

        self._app = app

        logger.info("QApplication created.")

        return app

    # ==========================================================
    # Initialization
    # ==========================================================

    def initialize(self) -> QApplication:
        """
        Initialize application-wide services.
        """

        app = self.create()

        resources.load_fonts()

        theme_manager.initialize(app)

        _ = thread_manager

        logger.info("UI initialization complete.")

        return app

    @property
    def application(self) -> QApplication:
        if self._app is None:
            raise RuntimeError(
                "Application has not been created."
            )

        return self._app
    
        # ==========================================================
    # Main Window
    # ==========================================================

    def create_main_window(self):
        """
        Create and return the application's main window.
        """

        from app.ui.main_window import MainWindow

        window = MainWindow()

        return window

    # ==========================================================
    # Execution
    # ==========================================================

    def run(self) -> int:
        """
        Initialize and start the application.
        """

        app = self.initialize()

        window = self.create_main_window()

        window.show()

        logger.info("Nova AI Desktop Assistant started.")

        return app.exec()

    # ==========================================================
    # Shutdown
    # ==========================================================

    def shutdown(self) -> None:
        """
        Gracefully shut down UI services.
        """

        try:
            thread_manager.shutdown()

        except Exception:
            logger.exception(
                "Failed while shutting down ThreadManager."
            )

        logger.info("Application shutdown complete.")


# ==========================================================
# Public Helper
# ==========================================================

def run() -> int:
    """
    Application entry point.
    """

    return NovaApplication().run()


__all__ = [
    "NovaApplication",
    "run",
]