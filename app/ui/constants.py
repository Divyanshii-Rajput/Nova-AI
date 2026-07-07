"""
Nova AI Desktop Assistant
-------------------------

UI Constants

This module contains all UI-wide immutable values used across the
desktop application.

The goal is to avoid magic numbers, duplicated strings and scattered
configuration values.

Only immutable constants belong here.
Runtime configuration belongs in config.py.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

# ============================================================================
# Project
# ============================================================================

APP_NAME: str = "Nova AI"
APP_FULL_NAME: str = "Nova AI Desktop Assistant"

APP_VERSION: str = "1.0.0"

ORGANIZATION_NAME: str = "Nova"

ORGANIZATION_DOMAIN: str = "nova.ai"

WINDOW_TITLE: str = APP_FULL_NAME

# ============================================================================
# Directories
# ============================================================================


# ==========================================================
# Root Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

APP_DIR = ROOT_DIR / "app"

UI_DIR = APP_DIR / "ui"


# ==========================================================
# UI Assets
# ==========================================================

ASSETS_DIR = UI_DIR / "assets"

ICONS_DIR = ASSETS_DIR / "icons"

IMAGES_DIR = ASSETS_DIR / "images"

SVG_DIR = ICONS_DIR

FONTS_DIR = ASSETS_DIR / "fonts"


# ==========================================================
# UI Styles
# ==========================================================

THEME_DIR = UI_DIR / "styles"


# ==========================================================
# Runtime Storage
# ==========================================================

CACHE_DIR = ROOT_DIR / "data" / "cache"

SCREENSHOT_DIR = ROOT_DIR / "screenshots"

DATA_DIR = ROOT_DIR / "data"

LOG_DIR = ROOT_DIR / "logs"


# ==========================================================
# Configuration
# ==========================================================

CONFIG_DIR = ROOT_DIR / "config"

# ============================================================================
# Window
# ============================================================================

DEFAULT_WINDOW_WIDTH = 1460

DEFAULT_WINDOW_HEIGHT = 920

MINIMUM_WINDOW_WIDTH = 1180

MINIMUM_WINDOW_HEIGHT = 760

SIDEBAR_WIDTH = 82

SIDEBAR_EXPANDED_WIDTH = 260

TITLEBAR_HEIGHT = 46

STATUS_BAR_HEIGHT = 34

TOP_MARGIN = 10

CONTENT_MARGIN = 18

CONTENT_SPACING = 16

PAGE_SPACING = 20

PAGE_RADIUS = 18

STACK_ANIMATION_DURATION = 220

# ============================================================================
# Navigation
# ============================================================================

HOME_PAGE = "home"

CHAT_PAGE = "chat"

BROWSER_PAGE = "browser"

FILES_PAGE = "files"

MUSIC_PAGE = "music"

SETTINGS_PAGE = "settings"

HISTORY_PAGE = "history"

ABOUT_PAGE = "about"

DEFAULT_PAGE = HOME_PAGE

# ============================================================================
# Icon Size
# ============================================================================

ICON_12 = 12
ICON_14 = 14
ICON_16 = 16
ICON_18 = 18
ICON_20 = 20
ICON_22 = 22
ICON_24 = 24
ICON_26 = 26
ICON_28 = 28
ICON_30 = 30
ICON_32 = 32
ICON_36 = 36
ICON_40 = 40
ICON_48 = 48
ICON_56 = 56
ICON_64 = 64

# ============================================================================
# Radius
# ============================================================================

RADIUS_SMALL = 8

RADIUS_MEDIUM = 12

RADIUS_LARGE = 18

RADIUS_XL = 24

RADIUS_PILL = 999

# ============================================================================
# Spacing
# ============================================================================

SPACE_2 = 2
SPACE_4 = 4
SPACE_6 = 6
SPACE_8 = 8
SPACE_10 = 10
SPACE_12 = 12
SPACE_14 = 14
SPACE_16 = 16
SPACE_18 = 18
SPACE_20 = 20
SPACE_24 = 24
SPACE_28 = 28
SPACE_32 = 32
SPACE_36 = 36
SPACE_40 = 40
SPACE_48 = 48
SPACE_56 = 56
SPACE_64 = 64

# ============================================================================
# Typography
# ============================================================================

FONT_FAMILY = "Segoe UI"

FONT_MONO = "Cascadia Code"

FONT_SMALL = 11

FONT_BODY = 13

FONT_MEDIUM = 14

FONT_TITLE = 16

FONT_HEADER = 18

FONT_SECTION = 22

FONT_DISPLAY = 30

FONT_HERO = 42

FONT_WEIGHT_LIGHT = 300

FONT_WEIGHT_NORMAL = 400

FONT_WEIGHT_MEDIUM = 500

FONT_WEIGHT_SEMIBOLD = 600

FONT_WEIGHT_BOLD = 700

# ============================================================================
# Animation
# ============================================================================

FAST_ANIMATION = 120

NORMAL_ANIMATION = 180

SLOW_ANIMATION = 260

PAGE_FADE_DURATION = 220

SIDEBAR_ANIMATION = 180

CARD_HOVER_DURATION = 120

BUTTON_ANIMATION = 100

RIPPLE_DURATION = 320

MIC_ANIMATION_DURATION = 180

WAVEFORM_FPS = 60

# ============================================================================
# Shadow
# ============================================================================

SHADOW_BLUR = 34

SHADOW_OFFSET_X = 0

SHADOW_OFFSET_Y = 10

SHADOW_ALPHA = 80

# ============================================================================
# Chat
# ============================================================================

MAX_CHAT_WIDTH = 860

CHAT_MARGIN = 22

CHAT_SPACING = 14

CHAT_AVATAR_SIZE = 36

CHAT_BUBBLE_RADIUS = 18

CHAT_INPUT_HEIGHT = 58

CHAT_HISTORY_LIMIT = 500

# ============================================================================
# Cards
# ============================================================================

CARD_RADIUS = 18

CARD_PADDING = 18

CARD_SPACING = 18

CARD_ICON_SIZE = 30

CARD_MIN_HEIGHT = 110

CARD_ELEVATION = 12

# ============================================================================
# Microphone
# ============================================================================

MIC_SIZE = 76

MIC_RING_SIZE = 92

MIC_IDLE_SCALE = 1.0

MIC_ACTIVE_SCALE = 1.12

MIC_MAX_SCALE = 1.22

WAVEFORM_BAR_COUNT = 42

WAVEFORM_BAR_WIDTH = 4

WAVEFORM_BAR_GAP = 3

WAVEFORM_MAX_HEIGHT = 58

# ============================================================================
# Search
# ============================================================================

SEARCH_HEIGHT = 42

SEARCH_RADIUS = 12

SEARCH_ICON_SIZE = 18

SEARCH_DEBOUNCE_MS = 250

# ============================================================================
# Sidebar
# ============================================================================

SIDEBAR_ICON_SIZE = 22

SIDEBAR_ITEM_HEIGHT = 48

SIDEBAR_ITEM_RADIUS = 12

SIDEBAR_BOTTOM_MARGIN = 18

SIDEBAR_TOP_MARGIN = 14

# ============================================================================
# Toast
# ============================================================================

TOAST_WIDTH = 360

TOAST_HEIGHT = 72

TOAST_RADIUS = 14

TOAST_DURATION = 3000

TOAST_SPACING = 12

# ============================================================================
# Loading
# ============================================================================

LOADER_SIZE = 48

LOADER_STROKE = 4

LOADER_SPEED = 1.0

# ============================================================================
# Status Widget
# ============================================================================

STATUS_ICON_SIZE = 18

STATUS_WIDGET_HEIGHT = 36

STATUS_WIDGET_RADIUS = 10

# ============================================================================
# Browser Page
# ============================================================================

BROWSER_SEARCH_HEIGHT = 46

BROWSER_CARD_WIDTH = 300

BROWSER_CARD_HEIGHT = 180

# ============================================================================
# Music
# ============================================================================

ALBUM_ART_SIZE = 180

PLAYER_BAR_HEIGHT = 86

PLAYER_BUTTON_SIZE = 42

# ============================================================================
# File Manager
# ============================================================================

FILE_ITEM_HEIGHT = 46

FILE_ICON_SIZE = 20

FILE_PREVIEW_SIZE = 72

# ============================================================================
# Colors
# ============================================================================

class Colors:
    """Central UI color tokens."""

    PRIMARY = "#5B8CFF"
    PRIMARY_HOVER = "#6B99FF"
    PRIMARY_PRESSED = "#4A79F5"

    SUCCESS = "#2ECC71"
    WARNING = "#F4B400"
    ERROR = "#FF5C5C"
    INFO = "#5BC0EB"

    TEXT_PRIMARY = "#F5F7FA"
    TEXT_SECONDARY = "#B3BAC7"
    TEXT_DISABLED = "#6E7582"

    BORDER = "#343A46"
    DIVIDER = "#2B303A"

    WINDOW_BG = "#171A20"
    SURFACE = "#1D2128"
    SURFACE_ALT = "#262B35"

    CHAT_USER = "#3A7AFE"
    CHAT_ASSISTANT = "#252A33"

    TRANSPARENT = "#00000000"

# ============================================================================
# Theme
# ============================================================================

class ThemeMode(str, Enum):
    DARK = "dark"
    LIGHT = "light"
    SYSTEM = "system"

# ============================================================================
# Navigation IDs
# ============================================================================

class NavigationID(str, Enum):
    HOME = HOME_PAGE
    CHAT = CHAT_PAGE
    BROWSER = BROWSER_PAGE
    FILES = FILES_PAGE
    MUSIC = MUSIC_PAGE
    SETTINGS = SETTINGS_PAGE
    HISTORY = HISTORY_PAGE
    ABOUT = ABOUT_PAGE

# ============================================================================
# Assistant States
# ============================================================================

class AssistantState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    EXECUTING = "executing"
    ERROR = "error"

# ============================================================================
# Window State
# ============================================================================

class WindowMode(str, Enum):
    NORMAL = "normal"
    MAXIMIZED = "maximized"
    FULLSCREEN = "fullscreen"

# ============================================================================
# Logging
# ============================================================================

UI_LOGGER_NAME = "nova.ui"

# ============================================================================
# High DPI
# ============================================================================

ENABLE_HIGH_DPI = True

ENABLE_HIGH_DPI_PIXMAPS = True

# ============================================================================
# Qt Properties
# ============================================================================

PROPERTY_ACCENT = "accent"

PROPERTY_ERROR = "error"

PROPERTY_SUCCESS = "success"

PROPERTY_WARNING = "warning"

PROPERTY_ACTIVE = "active"

PROPERTY_SELECTED = "selected"

PROPERTY_HOVER = "hover"

PROPERTY_PRESSED = "pressed"

PROPERTY_DISABLED = "disabled"

PROPERTY_DANGER = "danger"

PROPERTY_ROLE = "role"

PROPERTY_VARIANT = "variant"

# ============================================================================
# Z-Order
# ============================================================================

Z_BACKGROUND = 0

Z_CONTENT = 10

Z_FLOATING = 100

Z_OVERLAY = 500

Z_DIALOG = 1000

Z_TOAST = 2000

# ============================================================================
# Miscellaneous
# ============================================================================

DEFAULT_CORNER_RADIUS = RADIUS_LARGE

DEFAULT_PADDING = SPACE_16

DEFAULT_MARGIN = SPACE_16

DEFAULT_ICON_SIZE = ICON_20

DEFAULT_BUTTON_HEIGHT = 42

DEFAULT_INPUT_HEIGHT = 42

DEFAULT_SPLITTER_WIDTH = 4

DEFAULT_BORDER_WIDTH = 1

DEFAULT_OPACITY = 1.0

HOVER_OPACITY = 0.92

DISABLED_OPACITY = 0.45

# ============================================================================
# Public Exports
# ============================================================================

__all__ = [
    "APP_NAME",
    "APP_FULL_NAME",
    "APP_VERSION",
    "WINDOW_TITLE",
    "ROOT_DIR",
    "APP_DIR",
    "UI_DIR",
    "ASSETS_DIR",
    "ICONS_DIR",
    "IMAGES_DIR",
    "SVG_DIR",
    "FONTS_DIR",
    "THEME_DIR",
    "CACHE_DIR",
    "DATA_DIR",
    "LOG_DIR",
    "CONFIG_DIR",
    "Colors",
    "ThemeMode",
    "NavigationID",
    "AssistantState",
    "WindowMode",
]