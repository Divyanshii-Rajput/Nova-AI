"""
Nova AI Desktop Assistant
-------------------------

Central UI signal bus.

This module provides a thread-safe global signal manager used for
communication between independent UI components without creating
tight coupling.

Widgets should communicate through this bus instead of directly
referencing each other whenever possible.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject, Signal


class UISignals(QObject):
    """
    Global signal bus for the entire UI.
    """

    # ==========================================================
    # Navigation
    # ==========================================================

    page_requested = Signal(str)

    page_changed = Signal(str)

    back_requested = Signal()

    forward_requested = Signal()

    home_requested = Signal()

    # ==========================================================
    # Assistant State
    # ==========================================================

    assistant_started = Signal()

    assistant_stopped = Signal()

    assistant_state_changed = Signal(str)

    assistant_busy = Signal(bool)

    assistant_error = Signal(str)

    # ==========================================================
    # Voice
    # ==========================================================

    microphone_started = Signal()

    microphone_stopped = Signal()

    microphone_muted = Signal(bool)

    voice_level_changed = Signal(float)

    waveform_updated = Signal(list)

    transcript_received = Signal(str)

    partial_transcript = Signal(str)

    speech_started = Signal()

    speech_finished = Signal()

    # ==========================================================
    # Chat
    # ==========================================================

    message_sent = Signal(str)

    message_received = Signal(str)

    message_stream_started = Signal()

    message_stream_chunk = Signal(str)

    message_stream_finished = Signal()

    conversation_cleared = Signal()

    history_loaded = Signal()

    # ==========================================================
    # Browser
    # ==========================================================

    browser_open_requested = Signal(str)

    browser_closed = Signal()

    browser_loading = Signal(bool)

    browser_title_changed = Signal(str)

    browser_url_changed = Signal(str)

    # ==========================================================
    # Music
    # ==========================================================

    music_play = Signal()

    music_pause = Signal()

    music_stop = Signal()

    music_next = Signal()

    music_previous = Signal()

    music_position_changed = Signal(int)

    music_duration_changed = Signal(int)

    music_track_changed = Signal(dict)

    # ==========================================================
    # Files
    # ==========================================================

    file_open_requested = Signal(str)

    file_selected = Signal(str)

    file_deleted = Signal(str)

    file_renamed = Signal(str, str)

    file_search_started = Signal()

    file_search_finished = Signal()

    # ==========================================================
    # Theme
    # ==========================================================

    theme_changed = Signal(str)

    accent_changed = Signal(str)

    font_changed = Signal(str)

    scale_changed = Signal(float)

    # ==========================================================
    # Window
    # ==========================================================

    minimize_requested = Signal()

    maximize_requested = Signal()

    restore_requested = Signal()

    close_requested = Signal()

    window_state_changed = Signal(str)

    fullscreen_changed = Signal(bool)

    # ==========================================================
    # Status
    # ==========================================================

    status_changed = Signal(str)

    progress_changed = Signal(int)

    loading_started = Signal()

    loading_finished = Signal()

    busy_state_changed = Signal(bool)

    # ==========================================================
    # Notifications
    # ==========================================================

    show_toast = Signal(str)

    show_success = Signal(str)

    show_warning = Signal(str)

    show_error = Signal(str)

    show_info = Signal(str)

    # ==========================================================
    # Settings
    # ==========================================================

    settings_loaded = Signal()

    settings_saved = Signal()

    settings_reset = Signal()

    # ==========================================================
    # Generic
    # ==========================================================

    refresh_requested = Signal()

    refresh_completed = Signal()

    data_updated = Signal(str)

    object_selected = Signal(object)

    custom_event = Signal(str, object)
    
        # ==========================================================
    # Diagnostics
    # ==========================================================

    log_message = Signal(str)

    exception_raised = Signal(str)

    performance_warning = Signal(str)

    # ==========================================================
    # Lifecycle
    # ==========================================================

    application_started = Signal()

    application_ready = Signal()

    application_closing = Signal()

    application_closed = Signal()

    # ==========================================================
    # Helpers
    # ==========================================================

    def emit_toast(self, message: str) -> None:
        """Emit a generic toast notification."""
        self.show_toast.emit(message)

    def emit_success(self, message: str) -> None:
        """Emit a success notification."""
        self.show_success.emit(message)

    def emit_warning(self, message: str) -> None:
        """Emit a warning notification."""
        self.show_warning.emit(message)

    def emit_error(self, message: str) -> None:
        """Emit an error notification."""
        self.show_error.emit(message)

    def emit_info(self, message: str) -> None:
        """Emit an informational notification."""
        self.show_info.emit(message)

    def emit_status(self, message: str) -> None:
        """Emit a status bar update."""
        self.status_changed.emit(message)

    def emit_progress(self, value: int) -> None:
        """
        Emit progress value.

        Parameters
        ----------
        value:
            Progress percentage between 0 and 100.
        """
        value = max(0, min(100, value))
        self.progress_changed.emit(value)

    def emit_page_change(self, page: str) -> None:
        """Request navigation to a page."""
        self.page_requested.emit(page)

    def emit_theme_change(self, theme: str) -> None:
        """Notify UI about theme changes."""
        self.theme_changed.emit(theme)

    def emit_busy(self, busy: bool) -> None:
        """Broadcast busy state."""
        self.busy_state_changed.emit(busy)

    def emit_custom_event(
        self,
        event_name: str,
        payload: Any = None,
    ) -> None:
        """Emit a custom event with arbitrary payload."""
        self.custom_event.emit(event_name, payload)


# ==============================================================
# Singleton Signal Bus
# ==============================================================

ui_signals = UISignals()


def get_ui_signals() -> UISignals:
    """
    Return the global UI signal bus.

    Using a singleton avoids duplicate signal instances across modules.
    """
    return ui_signals


__all__ = [
    "UISignals",
    "ui_signals",
    "get_ui_signals",
]