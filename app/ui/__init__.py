"""
Nova AI Desktop UI

PySide6-based desktop interface for Nova AI.

Modules
-------
app.py
    Application entry point.

main_window.py
    Main application window.

theme.py
    Global colors and theme.

resources.py
    Icons, fonts and resource helpers.

animations.py
    Shared UI animations.
"""

from .app import NovaApplication

__all__ = [
    "NovaApplication",
]