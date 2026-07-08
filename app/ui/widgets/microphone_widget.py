"""
Nova AI Desktop Assistant
-------------------------

Animated Microphone Widget

Displays the assistant microphone state and provides
visual feedback while listening, thinking and speaking.
"""

from __future__ import annotations

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QWidget

from app.ui.constants import (
    MIC_ACTIVE_SCALE,
    MIC_ANIMATION_DURATION,
    MIC_IDLE_SCALE,
    MIC_MAX_SCALE,
    MIC_RING_SIZE,
    MIC_SIZE,
)
from app.ui.resources import resources


class MicrophoneWidget(QWidget):
    """
    Animated microphone widget.
    """

    clicked = Signal()

    listeningChanged = Signal(bool)

    speakingChanged = Signal(bool)

    thinkingChanged = Signal(bool)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("MicrophoneWidget")

        self.setFixedSize(
            MIC_RING_SIZE,
            MIC_RING_SIZE,
        )

        self._scale = MIC_IDLE_SCALE

        self._listening = False

        self._thinking = False

        self._speaking = False

        self._pulse = QPropertyAnimation(
            self,
            b"scale",
            self,
        )

        self._pulse.setDuration(
            MIC_ANIMATION_DURATION
        )

        self._pulse.setLoopCount(-1)

        self._pulse.setStartValue(
            MIC_IDLE_SCALE
        )

        self._pulse.setKeyValueAt(
            0.5,
            MIC_MAX_SCALE,
        )

        self._pulse.setEndValue(
            MIC_IDLE_SCALE
        )

        self._pulse.setEasingCurve(
            QEasingCurve.InOutQuad
        )

    # ======================================================
    # Property
    # ======================================================

    def getScale(self) -> float:
        return self._scale

    def setScale(
        self,
        value: float,
    ) -> None:
        self._scale = value
        self.update()

    scale = Property(
        float,
        getScale,
        setScale,
    )

    # ======================================================
    # States
    # ======================================================

    def setListening(
        self,
        value: bool,
    ) -> None:

        self._listening = value

        if value:
            self._pulse.start()
        else:
            self._pulse.stop()
            self.setScale(
                MIC_IDLE_SCALE
            )

        self.listeningChanged.emit(value)

        self.update()

    def setThinking(
        self,
        value: bool,
    ) -> None:

        self._thinking = value

        self.update()

        self.thinkingChanged.emit(value)

    def setSpeaking(
        self,
        value: bool,
    ) -> None:

        self._speaking = value

        self.update()

        self.speakingChanged.emit(value)
    
        # ======================================================
    # Queries
    # ======================================================

    def isListening(self) -> bool:
        return self._listening

    def isThinking(self) -> bool:
        return self._thinking

    def isSpeaking(self) -> bool:
        return self._speaking

    # ======================================================
    # Painting
    # ======================================================

    def paintEvent(self, event) -> None:
        """
        Paint the animated microphone.
        """

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        center = self.rect().center()

        radius = (
            MIC_SIZE / 2
        ) * self._scale

        if self._listening:
            ring_color = QColor("#2ECC71") # Green
        elif self._speaking:
            ring_color = QColor("#5B8CFF") # Blue
        elif self._thinking:
            ring_color = QColor("#F4B400") # Amber
        else:
            ring_color = QColor("#7B8494") # Gray

        pen = QPen(ring_color, 3)

        painter.setPen(pen)

        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            QRectF(
                center.x() - radius,
                center.y() - radius,
                radius * 2,
                radius * 2,
            )
        )

        icon = resources.icon(
            "fa6s.microphone",
            color=ring_color.name(),
        )

        pixmap = icon.pixmap(
            MIC_SIZE,
            MIC_SIZE,
        )

        painter.drawPixmap(
            int(center.x() - (MIC_SIZE / 2)),
            int(center.y() - (MIC_SIZE / 2)),
            pixmap,
        )

    # ======================================================
    # Events
    # ======================================================

    def mousePressEvent(self, event) -> None:
        """
        Emit click signal when the widget is pressed.
        """

        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)

    # ======================================================
    # Utilities
    # ======================================================

    def reset(self) -> None:
        """
        Reset the microphone widget to the idle state.
        """

        self._pulse.stop()

        self._listening = False
        self._thinking = False
        self._speaking = False

        self.setScale(MIC_IDLE_SCALE)

        self.update()

    def startPulse(self) -> None:
        """
        Start the pulse animation.
        """

        if self._pulse.state() != QPropertyAnimation.State.Running:
            self._pulse.start()

    def stopPulse(self) -> None:
        """
        Stop the pulse animation.
        """

        self._pulse.stop()

        self.setScale(MIC_IDLE_SCALE)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(
            MIC_RING_SIZE,
            MIC_RING_SIZE,
        )


__all__ = [
    "MicrophoneWidget",
]