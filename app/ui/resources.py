"""
Nova AI Desktop Assistant
-------------------------

UI Resource Manager

Centralized access to application resources.

Responsibilities
----------------
* Resolve asset paths
* Load icons
* Load pixmaps
* Load fonts
* Verify resource existence
* Cache frequently used resources
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import qtawesome as qta

from PySide6.QtGui import (
    QColor,
    QFont,
    QFontDatabase,
    QIcon,
    QPixmap,
)

from app.ui.constants import (
    ASSETS_DIR,
    FONTS_DIR,
    ICONS_DIR,
    IMAGES_DIR,
    SVG_DIR,
)


class ResourceManager:
    """Central resource loader."""

    def __init__(self) -> None:
        self._font_loaded = False

    # ==========================================================
    # Paths
    # ==========================================================

    @staticmethod
    def asset_path(*parts: str) -> Path:
        return ASSETS_DIR.joinpath(*parts)

    @staticmethod
    def icon_path(name: str) -> Path:
        return ICONS_DIR / name

    @staticmethod
    def svg_path(name: str) -> Path:
        return SVG_DIR / name

    @staticmethod
    def image_path(name: str) -> Path:
        return IMAGES_DIR / name

    @staticmethod
    def font_path(name: str) -> Path:
        return FONTS_DIR / name

    # ==========================================================
    # Existence
    # ==========================================================

    @staticmethod
    def exists(path: Path) -> bool:
        return path.exists()

    # ==========================================================
    # Fonts
    # ==========================================================

    def load_fonts(self) -> None:
        """
        Load every font inside assets/fonts.
        """

        if self._font_loaded:
            return

        if not FONTS_DIR.exists():
            self._font_loaded = True
            return

        for file in FONTS_DIR.iterdir():

            if file.suffix.lower() not in (
                ".ttf",
                ".otf",
            ):
                continue

            QFontDatabase.addApplicationFont(str(file))

        self._font_loaded = True

    @staticmethod
    def font(
        family: str,
        size: int,
        bold: bool = False,
    ) -> QFont:
        f = QFont(family, size)
        f.setBold(bold)
        return f

    # ==========================================================
    # Icons
    # ==========================================================

    @staticmethod
    @lru_cache(maxsize=256)
    def icon(
        name: str,
        color: str | QColor | None = None,
    ) -> QIcon:
        """
        Returns QtAwesome icon if available,
        otherwise loads SVG/PNG from assets.
        """

        try:
            if color is None:
                color = "#B7BCC7"
            icon = qta.icon(name, color=color)
            return icon
        except Exception:
            pass

        svg = ICONS_DIR / f"{name}.svg"

        if svg.exists():
            return QIcon(str(svg))

        png = ICONS_DIR / f"{name}.png"

        if png.exists():
            return QIcon(str(png))

        return QIcon()

    # ==========================================================
    # Pixmaps
    # ==========================================================

    @staticmethod
    @lru_cache(maxsize=128)
    def pixmap(
        filename: str,
    ) -> QPixmap:

        path = IMAGES_DIR / filename

        if path.exists():
            return QPixmap(str(path))

        return QPixmap()

        # ==========================================================
    # Convenience Methods
    # ==========================================================

    @staticmethod
    def svg(filename: str) -> QIcon:
        """
        Load an SVG icon from the assets directory.
        """
        path = SVG_DIR / filename

        if path.exists():
            return QIcon(str(path))

        return QIcon()

    @staticmethod
    def image(filename: str) -> QPixmap:
        """
        Load an image from the assets directory.
        """
        path = IMAGES_DIR / filename

        if path.exists():
            return QPixmap(str(path))

        return QPixmap()

    @staticmethod
    def icon_exists(name: str) -> bool:
        """
        Check whether an icon exists.
        """
        return (
            (ICONS_DIR / f"{name}.svg").exists()
            or (ICONS_DIR / f"{name}.png").exists()
        )

    @staticmethod
    def image_exists(name: str) -> bool:
        """
        Check whether an image exists.
        """
        return (IMAGES_DIR / name).exists()

    @staticmethod
    def font_exists(name: str) -> bool:
        """
        Check whether a font file exists.
        """
        return (FONTS_DIR / name).exists()

    # ==========================================================
    # Cache
    # ==========================================================

    @staticmethod
    def clear_cache() -> None:
        """
        Clear all cached icons and pixmaps.
        """
        ResourceManager.icon.cache_clear()
        ResourceManager.pixmap.cache_clear()

    # ==========================================================
    # Diagnostics
    # ==========================================================

    @staticmethod
    def available_fonts() -> list[str]:
        """
        Return all available application font families.
        """
        return QFontDatabase.families()

    @staticmethod
    def assets_root() -> Path:
        """
        Return the assets root directory.
        """
        return ASSETS_DIR

    @staticmethod
    def icons_root() -> Path:
        return ICONS_DIR

    @staticmethod
    def images_root() -> Path:
        return IMAGES_DIR

    @staticmethod
    def fonts_root() -> Path:
        return FONTS_DIR


# ==========================================================
# Global Resource Manager
# ==========================================================

resources = ResourceManager()


def get_resource_manager() -> ResourceManager:
    """
    Return the singleton ResourceManager instance.
    """
    return resources


__all__ = [
    "ResourceManager",
    "resources",
    "get_resource_manager",
]