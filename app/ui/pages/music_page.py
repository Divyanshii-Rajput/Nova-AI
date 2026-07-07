"""
Nova AI Desktop Assistant
-------------------------

Music Page

Music control interface.

Responsibilities
----------------
- Display current track
- Playback controls
- Progress display
- Volume control
- Playlist placeholder

Backend integration will be completed in Sprint 5.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    PAGE_SPACING,
    SPACE_12,
    SPACE_16,
)
from app.ui.resources import resources


class MusicPage(QWidget):
    """
    Music player page.
    """

    playRequested = Signal()

    pauseRequested = Signal()

    stopRequested = Signal()

    nextRequested = Signal()

    previousRequested = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("MusicPage")

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:

        root = QVBoxLayout(self)

        root.setContentsMargins(
            SPACE_16,
            SPACE_16,
            SPACE_16,
            SPACE_16,
        )

        root.setSpacing(PAGE_SPACING)

        # ==================================================
        # Album
        # ==================================================

        self.albumArt = QLabel()

        self.albumArt.setFixedSize(
            180,
            180,
        )

        self.albumArt.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.albumArt.setPixmap(
            resources.icon(
                "fa6s.music"
            ).pixmap(
                96,
                96,
            )
        )

        root.addWidget(
            self.albumArt,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        self.trackTitle = QLabel(
            "No Track Playing"
        )

        self.trackTitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.trackTitle.setObjectName(
            "PageTitle"
        )

        root.addWidget(
            self.trackTitle
        )

        self.artistLabel = QLabel(
            "Unknown Artist"
        )

        self.artistLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        root.addWidget(
            self.artistLabel
        )

        # ==================================================
        # Progress
        # ==================================================

        self.progressSlider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.progressSlider.setRange(
            0,
            100,
        )

        root.addWidget(
            self.progressSlider
        )

        # ==================================================
        # Controls
        # ==================================================

        controls = QHBoxLayout()

        controls.setSpacing(
            SPACE_12
        )

        self.previousButton = QPushButton()

        self.previousButton.setIcon(
            resources.icon(
                "fa6s.backward-step"
            )
        )

        controls.addWidget(
            self.previousButton
        )

        self.playButton = QPushButton()

        self.playButton.setIcon(
            resources.icon(
                "fa6s.play"
            )
        )

        controls.addWidget(
            self.playButton
        )

        self.pauseButton = QPushButton()

        self.pauseButton.setIcon(
            resources.icon(
                "fa6s.pause"
            )
        )

        controls.addWidget(
            self.pauseButton
        )

        self.stopButton = QPushButton()

        self.stopButton.setIcon(
            resources.icon(
                "fa6s.stop"
            )
        )

        controls.addWidget(
            self.stopButton
        )

        self.nextButton = QPushButton()

        self.nextButton.setIcon(
            resources.icon(
                "fa6s.forward-step"
            )
        )

        controls.addWidget(
            self.nextButton
        )

        root.addLayout(
            controls
        )

        # ==================================================
        # Playlist
        # ==================================================

        self.playlist = QListWidget()

        root.addWidget(
            self.playlist
        )

        # ==================================================
        # Signals
        # ==================================================

        self.playButton.clicked.connect(
            self.playRequested
        )

        self.pauseButton.clicked.connect(
            self.pauseRequested
        )

        self.stopButton.clicked.connect(
            self.stopRequested
        )

        self.nextButton.clicked.connect(
            self.nextRequested
        )

        self.previousButton.clicked.connect(
            self.previousRequested
        )
    
        # ======================================================
    # Public API
    # ======================================================

    def set_track(
        self,
        title: str,
        artist: str,
    ) -> None:
        """
        Update the currently playing track information.
        """

        self.trackTitle.setText(title)

        self.artistLabel.setText(artist)

    def set_progress(
        self,
        value: int,
    ) -> None:
        """
        Update playback progress.
        """

        self.progressSlider.setValue(value)

    def progress(self) -> int:
        """
        Return the current playback progress.
        """

        return self.progressSlider.value()

    def add_track(
        self,
        title: str,
    ) -> None:
        """
        Add a track to the playlist.
        """

        self.playlist.addItem(title)

    def add_tracks(
        self,
        tracks: list[str],
    ) -> None:
        """
        Add multiple tracks to the playlist.
        """

        self.playlist.addItems(tracks)

    def clear_playlist(self) -> None:
        """
        Remove all playlist items.
        """

        self.playlist.clear()

    def playlist_count(self) -> int:
        """
        Return the number of playlist entries.
        """

        return self.playlist.count()

    def set_volume(
        self,
        value: int,
    ) -> None:
        """
        Placeholder for volume integration.
        """

        value = max(0, min(100, value))

    def reset(self) -> None:
        """
        Restore the page to its default state.
        """

        self.trackTitle.setText("No Track Playing")

        self.artistLabel.setText("Unknown Artist")

        self.progressSlider.setValue(0)

        self.playlist.clear()

    # ======================================================
    # Utilities
    # ======================================================

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(1200, 800)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(900, 600)


__all__ = [
    "MusicPage",
]