"""
Nova AI Desktop Assistant
-------------------------

UI Configuration

Contains runtime configuration for the UI layer.

Unlike constants.py, values here may be loaded from user settings,
modified during execution, and persisted between sessions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.ui.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    MINIMUM_WINDOW_HEIGHT,
    MINIMUM_WINDOW_WIDTH,
    ThemeMode,
)


# ============================================================================
# Paths
# ============================================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = ROOT_DIR / "config"

SETTINGS_FILE = CONFIG_DIR / "settings.json"


# ============================================================================
# Window Configuration
# ============================================================================

@dataclass(slots=True)
class WindowConfig:
    """Main application window configuration."""

    title: str = APP_NAME

    width: int = DEFAULT_WINDOW_WIDTH

    height: int = DEFAULT_WINDOW_HEIGHT

    minimum_width: int = MINIMUM_WINDOW_WIDTH

    minimum_height: int = MINIMUM_WINDOW_HEIGHT

    maximized: bool = False

    frameless: bool = True

    translucent_background: bool = False

    remember_geometry: bool = True


# ============================================================================
# Theme Configuration
# ============================================================================

@dataclass(slots=True)
class ThemeConfig:
    """Appearance configuration."""

    mode: ThemeMode = ThemeMode.DARK

    follow_system: bool = False

    enable_animations: bool = True

    enable_blur: bool = True

    enable_shadows: bool = True

    enable_acrylic: bool = False

    accent_color: str = "#5B8CFF"

    font_family: str = "Segoe UI"

    font_size: int = 13

    border_radius: int = 12


# ============================================================================
# Chat Configuration
# ============================================================================

@dataclass(slots=True)
class ChatConfig:
    """Chat interface configuration."""

    auto_scroll: bool = True

    show_timestamps: bool = True

    show_avatar: bool = True

    bubble_animation: bool = True

    typing_indicator: bool = True

    history_limit: int = 500

    markdown_enabled: bool = True

    code_highlighting: bool = True


# ============================================================================
# Voice Configuration
# ============================================================================

@dataclass(slots=True)
class VoiceConfig:
    """Voice UI configuration."""

    show_waveform: bool = True

    animate_microphone: bool = True

    auto_start_animation: bool = True

    waveform_bars: int = 42

    microphone_size: int = 76


# ============================================================================
# Notification Configuration
# ============================================================================

@dataclass(slots=True)
class NotificationConfig:
    """Toast notification settings."""

    enabled: bool = True

    timeout_ms: int = 3000

    maximum_visible: int = 3

    play_sound: bool = False

    # ============================================================================
# Developer Configuration
# ============================================================================

@dataclass(slots=True)
class DeveloperConfig:
    """Developer and debugging configuration."""

    debug: bool = False

    show_fps: bool = False

    show_layout_bounds: bool = False

    enable_logging: bool = True

    log_level: str = "INFO"

    enable_qt_messages: bool = False

    performance_overlay: bool = False


# ============================================================================
# Application Configuration
# ============================================================================

@dataclass(slots=True)
class UIConfig:
    """
    Root UI configuration.

    This object is intended to be shared throughout the UI layer and can
    be serialized/deserialized from the settings file.
    """

    application_name: str = APP_NAME

    application_version: str = APP_VERSION

    window: WindowConfig = field(default_factory=WindowConfig)

    theme: ThemeConfig = field(default_factory=ThemeConfig)

    chat: ChatConfig = field(default_factory=ChatConfig)

    voice: VoiceConfig = field(default_factory=VoiceConfig)

    notifications: NotificationConfig = field(default_factory=NotificationConfig)

    developer: DeveloperConfig = field(default_factory=DeveloperConfig)

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration into a serializable dictionary."""

        return {
            "application_name": self.application_name,
            "application_version": self.application_version,
            "window": vars(self.window),
            "theme": {
                **vars(self.theme),
                "mode": self.theme.mode.value,
            },
            "chat": vars(self.chat),
            "voice": vars(self.voice),
            "notifications": vars(self.notifications),
            "developer": vars(self.developer),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UIConfig":
        """Create configuration from dictionary."""

        window = WindowConfig(**data.get("window", {}))

        theme_data = dict(data.get("theme", {}))
        mode = theme_data.get("mode", ThemeMode.DARK.value)
        theme_data["mode"] = ThemeMode(mode)

        theme = ThemeConfig(**theme_data)

        chat = ChatConfig(**data.get("chat", {}))

        voice = VoiceConfig(**data.get("voice", {}))

        notifications = NotificationConfig(
            **data.get("notifications", {})
        )

        developer = DeveloperConfig(
            **data.get("developer", {})
        )

        return cls(
            application_name=data.get(
                "application_name",
                APP_NAME,
            ),
            application_version=data.get(
                "application_version",
                APP_VERSION,
            ),
            window=window,
            theme=theme,
            chat=chat,
            voice=voice,
            notifications=notifications,
            developer=developer,
        )


# ============================================================================
# Default Instance
# ============================================================================

DEFAULT_UI_CONFIG = UIConfig()


# ============================================================================
# Public Exports
# ============================================================================

__all__ = [
    "SETTINGS_FILE",
    "WindowConfig",
    "ThemeConfig",
    "ChatConfig",
    "VoiceConfig",
    "NotificationConfig",
    "DeveloperConfig",
    "UIConfig",
    "DEFAULT_UI_CONFIG",
]