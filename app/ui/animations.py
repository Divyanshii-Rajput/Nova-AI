"""
Nova AI Desktop Assistant
-------------------------

Animations

Centralized reusable Qt animations used throughout the UI.

Provides:
- Fade animations
- Slide animations
- Scale animations
- Opacity animations
- Button press effects
- Hover effects
- Window transitions

Widget-specific animation logic should not be implemented here.
"""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QWidget,
)

from app.ui.constants import (
    BUTTON_ANIMATION,
    FAST_ANIMATION,
    NORMAL_ANIMATION,
    PAGE_FADE_DURATION,
    SLOW_ANIMATION,
)


class UIAnimations:
    """
    Collection of reusable UI animations.
    """

    # ==========================================================
    # Fade
    # ==========================================================

    @staticmethod
    def fade_in(
        widget: QWidget,
        duration: int = PAGE_FADE_DURATION,
        finished: Callable | None = None,
    ) -> QPropertyAnimation:

        effect = widget.graphicsEffect()

        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        effect.setOpacity(0.0)

        animation = QPropertyAnimation(effect, b"opacity")

        animation.setDuration(duration)

        animation.setStartValue(0.0)

        animation.setEndValue(1.0)

        animation.setEasingCurve(QEasingCurve.OutCubic)

        if finished:
            animation.finished.connect(finished)

        animation.start()

        return animation

    @staticmethod
    def fade_out(
        widget: QWidget,
        duration: int = PAGE_FADE_DURATION,
        finished: Callable | None = None,
    ) -> QPropertyAnimation:

        effect = widget.graphicsEffect()

        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        effect.setOpacity(1.0)

        animation = QPropertyAnimation(effect, b"opacity")

        animation.setDuration(duration)

        animation.setStartValue(1.0)

        animation.setEndValue(0.0)

        animation.setEasingCurve(QEasingCurve.InCubic)

        if finished:
            animation.finished.connect(finished)

        animation.start()

        return animation

    # ==========================================================
    # Slide
    # ==========================================================

    @staticmethod
    def slide_in_left(
        widget: QWidget,
        distance: int = 40,
        duration: int = NORMAL_ANIMATION,
    ) -> QPropertyAnimation:

        end = widget.pos()

        start = QPoint(
            end.x() - distance,
            end.y(),
        )

        widget.move(start)

        animation = QPropertyAnimation(
            widget,
            b"pos",
        )

        animation.setDuration(duration)

        animation.setStartValue(start)

        animation.setEndValue(end)

        animation.setEasingCurve(
            QEasingCurve.OutCubic,
        )

        animation.start()

        return animation

    @staticmethod
    def slide_in_right(
        widget: QWidget,
        distance: int = 40,
        duration: int = NORMAL_ANIMATION,
    ) -> QPropertyAnimation:

        end = widget.pos()

        start = QPoint(
            end.x() + distance,
            end.y(),
        )

        widget.move(start)

        animation = QPropertyAnimation(
            widget,
            b"pos",
        )

        animation.setDuration(duration)

        animation.setStartValue(start)

        animation.setEndValue(end)

        animation.setEasingCurve(
            QEasingCurve.OutCubic,
        )

        animation.start()

        return animation

    @staticmethod
    def slide_vertical(
        widget: QWidget,
        start_y: int,
        end_y: int,
        duration: int = NORMAL_ANIMATION,
    ) -> QPropertyAnimation:

        animation = QPropertyAnimation(
            widget,
            b"pos",
        )

        animation.setDuration(duration)

        animation.setStartValue(
            QPoint(widget.x(), start_y)
        )

        animation.setEndValue(
            QPoint(widget.x(), end_y)
        )

        animation.setEasingCurve(
            QEasingCurve.OutQuart,
        )

        animation.start()

        return animation
    
        # ==========================================================
    # Geometry
    # ==========================================================

    @staticmethod
    def resize(
        widget: QWidget,
        start: QSize,
        end: QSize,
        duration: int = NORMAL_ANIMATION,
    ) -> QPropertyAnimation:
        """
        Animate widget size.
        """

        animation = QPropertyAnimation(widget, b"size")

        animation.setDuration(duration)

        animation.setStartValue(start)

        animation.setEndValue(end)

        animation.setEasingCurve(QEasingCurve.OutCubic)

        animation.start()

        return animation

    @staticmethod
    def geometry(
        widget: QWidget,
        start: QRect,
        end: QRect,
        duration: int = NORMAL_ANIMATION,
    ) -> QPropertyAnimation:
        """
        Animate widget geometry.
        """

        animation = QPropertyAnimation(widget, b"geometry")

        animation.setDuration(duration)

        animation.setStartValue(start)

        animation.setEndValue(end)

        animation.setEasingCurve(QEasingCurve.OutCubic)

        animation.start()

        return animation

    # ==========================================================
    # Button Effects
    # ==========================================================

    @staticmethod
    def press(
        widget: QWidget,
        duration: int = BUTTON_ANIMATION,
    ) -> QPropertyAnimation:
        """
        Small button press animation.
        """

        geometry = widget.geometry()

        inset = 2

        pressed = QRect(
            geometry.x() + inset,
            geometry.y() + inset,
            geometry.width() - (inset * 2),
            geometry.height() - (inset * 2),
        )

        animation = QPropertyAnimation(widget, b"geometry")

        animation.setDuration(duration)

        animation.setKeyValueAt(0.0, geometry)

        animation.setKeyValueAt(0.5, pressed)

        animation.setKeyValueAt(1.0, geometry)

        animation.setEasingCurve(QEasingCurve.OutQuad)

        animation.start()

        return animation

    # ==========================================================
    # Opacity
    # ==========================================================

    @staticmethod
    def opacity(
        widget: QWidget,
        start: float,
        end: float,
        duration: int = FAST_ANIMATION,
    ) -> QPropertyAnimation:
        """
        Animate widget opacity.
        """

        effect = widget.graphicsEffect()

        if not isinstance(effect, QGraphicsOpacityEffect):
            effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(effect)

        effect.setOpacity(start)

        animation = QPropertyAnimation(effect, b"opacity")

        animation.setDuration(duration)

        animation.setStartValue(start)

        animation.setEndValue(end)

        animation.setEasingCurve(QEasingCurve.OutCubic)

        animation.start()

        return animation

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def stop(animation: QPropertyAnimation | None) -> None:
        """
        Stop an animation safely.
        """

        if animation is None:
            return

        if animation.state():
            animation.stop()

    @staticmethod
    def set_default_curve(
        animation: QPropertyAnimation,
    ) -> None:
        """
        Apply the application's default easing curve.
        """

        animation.setEasingCurve(QEasingCurve.OutCubic)

    @staticmethod
    def set_fast(animation: QPropertyAnimation) -> None:
        animation.setDuration(FAST_ANIMATION)

    @staticmethod
    def set_normal(animation: QPropertyAnimation) -> None:
        animation.setDuration(NORMAL_ANIMATION)

    @staticmethod
    def set_slow(animation: QPropertyAnimation) -> None:
        animation.setDuration(SLOW_ANIMATION)


# ==========================================================
# Singleton
# ==========================================================

animations = UIAnimations()


__all__ = [
    "UIAnimations",
    "animations",
]