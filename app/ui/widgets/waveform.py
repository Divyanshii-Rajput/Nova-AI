"""
Nova AI Desktop Assistant
-------------------------

Waveform Widget

Animated audio waveform used while listening,
processing speech and speaking responses.

The widget renders animated vertical bars whose
heights are driven by incoming audio levels.
"""

from __future__ import annotations

import random

from PySide6.QtCore import (
    QTimer,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
)
from PySide6.QtWidgets import QWidget

from app.ui.constants import (
    WAVEFORM_BAR_COUNT,
    WAVEFORM_BAR_GAP,
    WAVEFORM_BAR_WIDTH,
    WAVEFORM_MAX_HEIGHT,
)


class WaveformWidget(QWidget):
    """
    Animated audio waveform.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("WaveformWidget")

        self._levels = [
            0.15
        ] * WAVEFORM_BAR_COUNT

        self._active = False

        self._color = QColor("#5B8CFF")

        self._timer = QTimer(self)

        self._timer.setInterval(35)

        self._timer.timeout.connect(
            self._animate
        )

    # ==========================================================
    # State
    # ==========================================================

    def start(self) -> None:
        """
        Start waveform animation.
        """

        self._active = True

        self._timer.start()

    def stop(self) -> None:
        """
        Stop waveform animation.
        """

        self._active = False

        self._timer.stop()

        self._levels = [
            0.15
        ] * WAVEFORM_BAR_COUNT

        self.update()

    def isActive(self) -> bool:
        """
        Return whether the waveform is animating.
        """

        return self._active

    # ==========================================================
    # Data
    # ==========================================================

    def setLevels(
        self,
        levels: list[float],
    ) -> None:
        """
        Update waveform levels.
        """

        if not levels:
            return

        self._levels = levels[
            :WAVEFORM_BAR_COUNT
        ]

        while (
            len(self._levels)
            < WAVEFORM_BAR_COUNT
        ):
            self._levels.append(0.15)

        self.update()

    def setColor(
        self,
        color: str,
    ) -> None:
        """
        Change waveform color.
        """

        self._color = QColor(color)

        self.update()

    # ==========================================================
    # Animation
    # ==========================================================

    def _animate(self) -> None:

        if not self._active:
            return

        self._levels = [

            random.uniform(
                0.15,
                1.0,
            )

            for _ in range(
                WAVEFORM_BAR_COUNT
            )

        ]

        self.update()
    
        # ==========================================================
    # Painting
    # ==========================================================

    def paintEvent(self, event) -> None:
        """
        Paint the waveform bars.
        """

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(self._color)

        total_width = (
            WAVEFORM_BAR_COUNT * WAVEFORM_BAR_WIDTH
            + (WAVEFORM_BAR_COUNT - 1) * WAVEFORM_BAR_GAP
        )

        start_x = (self.width() - total_width) / 2

        center_y = self.height() / 2

        for index, level in enumerate(self._levels):

            height = max(
                4.0,
                level * WAVEFORM_MAX_HEIGHT,
            )

            x = start_x + index * (
                WAVEFORM_BAR_WIDTH + WAVEFORM_BAR_GAP
            )

            y = center_y - (height / 2)

            painter.drawRoundedRect(
                x,
                y,
                WAVEFORM_BAR_WIDTH,
                height,
                2,
                2,
            )

    # ==========================================================
    # Helpers
    # ==========================================================

    def clear(self) -> None:
        """
        Reset waveform values.
        """

        self.stop()

    def setLevel(
        self,
        value: float,
    ) -> None:
        """
        Set all bars to the same normalized level.
        """

        value = max(0.0, min(1.0, value))

        self._levels = [
            value
        ] * WAVEFORM_BAR_COUNT

        self.update()

    def levelCount(self) -> int:
        """
        Return the number of waveform bars.
        """

        return len(self._levels)

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(260, 80)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(180, 48)


__all__ = [
    "WaveformWidget",
]