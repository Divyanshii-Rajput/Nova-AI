"""
Nova AI Desktop Assistant
-------------------------

Loading Indicator

Reusable animated loading indicator used throughout
the application.

Features
--------
- Indeterminate loading spinner
- Start / Stop animation
- Optional status text
- Lightweight
"""

from __future__ import annotations

from PySide6.QtCore import (
    Property,
    QPropertyAnimation,
    QEasingCurve,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    LOADER_SIZE,
    LOADER_STROKE,
    NORMAL_ANIMATION,
    SPACE_12,
)


class LoadingIndicator(QFrame):
    """
    Circular loading indicator.
    """

    def __init__(
        self,
        text: str = "Loading...",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("LoadingIndicator")

        self._angle = 0.0

        self._running = False

        self.setMinimumSize(
            LOADER_SIZE + 24,
            LOADER_SIZE + 52,
        )

        self._animation = QPropertyAnimation(
            self,
            b"angle",
            self,
        )

        self._animation.setDuration(
            NORMAL_ANIMATION * 6
        )

        self._animation.setLoopCount(-1)

        self._animation.setStartValue(0)

        self._animation.setEndValue(360)

        self._animation.setEasingCurve(
            QEasingCurve.Linear
        )

        self._build_ui(text)

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(
        self,
        text: str,
    ) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            SPACE_12,
            SPACE_12,
            SPACE_12,
            SPACE_12,
        )

        layout.setSpacing(SPACE_12)

        layout.addSpacing(
            LOADER_SIZE
        )

        self.textLabel = QLabel(text)

        self.textLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.textLabel.setObjectName(
            "LoadingText"
        )

        layout.addWidget(
            self.textLabel
        )

    # ======================================================
    # Property
    # ======================================================

    def getAngle(self) -> float:
        return self._angle

    def setAngle(
        self,
        value: float,
    ) -> None:
        self._angle = value
        self.update()

    angle = Property(
        float,
        getAngle,
        setAngle,
    )

    # ======================================================
    # Control
    # ======================================================

    def start(self) -> None:

        if self._running:
            return

        self._running = True

        self._animation.start()

    def stop(self) -> None:

        self._running = False

        self._animation.stop()

        self.update()
    
    def isRunning(self) -> bool:
        """
        Return True if the loading animation is running.
        """

        return self._running

    # ======================================================
    # Text
    # ======================================================

    def setText(
        self,
        text: str,
    ) -> None:
        """
        Update the loading text.
        """

        self.textLabel.setText(text)

    def text(self) -> str:
        """
        Return the current loading text.
        """

        return self.textLabel.text()

    # ======================================================
    # Painting
    # ======================================================

    def paintEvent(self, event) -> None:
        """
        Paint the rotating loading spinner.
        """

        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        center = self.rect().center()

        radius = LOADER_SIZE / 2

        painter.translate(center)

        painter.rotate(self._angle)

        pen = QPen(
            QColor("#5B8CFF"),
            LOADER_STROKE,
        )

        pen.setCapStyle(
            Qt.PenCapStyle.RoundCap
        )

        painter.setPen(pen)

        rect = (
            -radius,
            -radius,
            radius * 2,
            radius * 2,
        )

        painter.drawArc(
            int(rect[0]),
            int(rect[1]),
            int(rect[2]),
            int(rect[3]),
            0,
            120 * 16,
        )

    # ======================================================
    # Utilities
    # ======================================================

    def reset(self) -> None:
        """
        Reset the loading indicator.
        """

        self.stop()

        self._angle = 0

        self.update()

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(
            LOADER_SIZE + 24,
            LOADER_SIZE + 52,
        )

    def minimumSizeHint(self):
        return self.sizeHint()


__all__ = [
    "LoadingIndicator",
]