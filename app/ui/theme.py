"""
Nova AI Desktop Assistant
-------------------------

Theme Manager

Handles:

- Dark / Light theme switching
- QSS loading
- Accent color management
- Qt palette updates
- Application font loading
- Theme persistence hooks

This module contains no widget-specific styling logic.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QColor, QGuiApplication, QPalette
from PySide6.QtWidgets import QApplication

from app.ui.constants import (
    THEME_DIR,
    ThemeMode,
)
from app.ui.resources import resources

logger = logging.getLogger(__name__)


class ThemeManager(QObject):
    """
    Global application theme manager.

    Responsible for applying themes across the application.
    """

    theme_changed = Signal(str)

    accent_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self._theme = ThemeMode.DARK
        self._accent = "#5B8CFF"

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def current_theme(self) -> ThemeMode:
        return self._theme

    @property
    def accent_color(self) -> str:
        return self._accent

    # ==========================================================
    # Public API
    # ==========================================================

    def initialize(self, app: QApplication) -> None:
        """
        Initialize UI theme.
        """

        resources.load_fonts()

        self.apply_theme(app, self._theme)

    def apply_theme(
        self,
        app: QApplication,
        theme: ThemeMode | str,
    ) -> None:
        """
        Apply application theme.
        """

        if isinstance(theme, str):
            theme = ThemeMode(theme)

        self._theme = theme

        if theme == ThemeMode.DARK:
            self._apply_dark(app)

        elif theme == ThemeMode.LIGHT:
            self._apply_light(app)

        else:
            self._apply_system(app)

        self.theme_changed.emit(theme.value)

        logger.info(
            "Theme changed -> %s",
            theme.value,
        )

    def toggle_theme(
        self,
        app: QApplication,
    ) -> None:
        """
        Toggle between dark and light.
        """

        if self._theme == ThemeMode.DARK:
            self.apply_theme(
                app,
                ThemeMode.LIGHT,
            )

        else:
            self.apply_theme(
                app,
                ThemeMode.DARK,
            )

    def set_accent(self, color: str) -> None:
        """
        Update accent color.
        """

        self._accent = color

        self.accent_changed.emit(color)

    # ==========================================================
    # Theme Application
    # ==========================================================

    def _apply_dark(
        self,
        app: QApplication,
    ) -> None:
        """
        Apply dark application theme.
        """

        self._apply_qss(
            app,
            "dark.qss",
        )

    def _apply_light(
        self,
        app: QApplication,
    ) -> None:
        """
        Apply light application theme.
        """

        self._apply_qss(
            app,
            "light.qss",
        )

    def _apply_system(
        self,
        app: QApplication,
    ) -> None:
        """
        Apply operating system theme.
        """

        color_scheme = (
            QGuiApplication
            .styleHints()
            .colorScheme()
        )

        if color_scheme == Qt.ColorScheme.Dark:
            self._apply_dark(app)

        else:
            self._apply_light(app)

    # ==========================================================
    # QSS
    # ==========================================================

    def _apply_qss(
        self,
        app: QApplication,
        filename: str,
    ) -> None:
        """
        Load and apply a QSS stylesheet.
        """

        qss_file = THEME_DIR / filename

        if not qss_file.exists():
            logger.warning(
                "Theme file not found: %s",
                qss_file,
            )
            return

        try:
            stylesheet = qss_file.read_text(
                encoding="utf-8",
            )

            stylesheet = stylesheet.replace(
                "{ACCENT_COLOR}",
                self._accent,
            )

            app.setStyleSheet(stylesheet)

        except Exception:
            logger.exception(
                "Unable to load stylesheet: %s",
                filename,
            )

    # ==========================================================
    # Palette
    # ==========================================================

    def set_palette(
        self,
        app: QApplication,
        palette: QPalette,
    ) -> None:
        """
        Apply custom Qt palette.
        """

        app.setPalette(palette)

    @staticmethod
    def create_palette(
        background: str,
        foreground: str,
    ) -> QPalette:
        """
        Create a minimal application palette.
        """

        palette = QPalette()

        palette.setColor(
            QPalette.ColorRole.Window,
            QColor(background),
        )

        palette.setColor(
            QPalette.ColorRole.WindowText,
            QColor(foreground),
        )

        palette.setColor(
            QPalette.ColorRole.Base,
            QColor(background),
        )

        palette.setColor(
            QPalette.ColorRole.Text,
            QColor(foreground),
        )

        return palette

    # ==========================================================
    # Utilities
    # ==========================================================

    def is_dark(self) -> bool:
        """
        Return True if current theme is dark.
        """

        return self._theme == ThemeMode.DARK

    def is_light(self) -> bool:
        """
        Return True if current theme is light.
        """

        return self._theme == ThemeMode.LIGHT


# ==========================================================
# Global Theme Manager
# ==========================================================

theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    """
    Return global ThemeManager instance.
    """

    return theme_manager


__all__ = [
    "ThemeManager",
    "theme_manager",
    "get_theme_manager",
]