"""
Nova AI Desktop Assistant
-------------------------

Cards

Reusable modern card widgets used across the UI.

Supported
---------
- Base Card
- Icon Card
- Action Card
- Information Card

Inspired by ChatGPT Desktop, Arc Browser and Cursor.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    CARD_ICON_SIZE,
    CARD_MIN_HEIGHT,
    CARD_PADDING,
    CARD_SPACING,
)
from app.ui.resources import resources


@dataclass(slots=True)
class CardData:
    """
    Data model for reusable cards.
    """

    title: str

    description: str

    icon: str = ""

    action_text: str = ""


class BaseCard(QFrame):
    """
    Base card widget.
    """

    clicked = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("BaseCard")

        self.setMinimumHeight(
            CARD_MIN_HEIGHT
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

    def mousePressEvent(self, event) -> None:

        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

        super().mousePressEvent(event)


class InfoCard(BaseCard):
    """
    Information display card.
    """

    def __init__(
        self,
        data: CardData,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.data = data

        self._build_ui()

    def _build_ui(self) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(
            CARD_SPACING
        )

        self.iconLabel = QLabel()

        if self.data.icon:

            self.iconLabel.setPixmap(

                resources.icon(
                    self.data.icon
                ).pixmap(
                    CARD_ICON_SIZE,
                    CARD_ICON_SIZE,
                )

            )

        layout.addWidget(
            self.iconLabel
        )

        body = QVBoxLayout()

        self.titleLabel = QLabel(
            self.data.title
        )

        self.titleLabel.setObjectName(
            "CardTitle"
        )

        body.addWidget(
            self.titleLabel
        )

        self.descriptionLabel = QLabel(
            self.data.description
        )

        self.descriptionLabel.setWordWrap(
            True
        )

        self.descriptionLabel.setObjectName(
            "CardDescription"
        )

        body.addWidget(
            self.descriptionLabel
        )

        layout.addLayout(body)

        layout.addStretch()
    
class ActionCard(InfoCard):
    """
    Information card with a primary action button.
    """

    actionTriggered = Signal()

    def __init__(
        self,
        data: CardData,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(data, parent)

        self.actionButton = QPushButton(
            data.action_text or "Open"
        )

        self.actionButton.setObjectName(
            "CardActionButton"
        )

        self.layout().addWidget(
            self.actionButton,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.actionButton.clicked.connect(
            self.actionTriggered.emit
        )


class IconCard(BaseCard):
    """
    Large icon-centric card.
    """

    def __init__(
        self,
        data: CardData,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.data = data

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(CARD_SPACING)

        self.iconLabel = QLabel()

        self.iconLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        if data.icon:

            self.iconLabel.setPixmap(

                resources.icon(
                    data.icon
                ).pixmap(
                    CARD_ICON_SIZE * 2,
                    CARD_ICON_SIZE * 2,
                )

            )

        layout.addWidget(
            self.iconLabel
        )

        self.titleLabel = QLabel(
            data.title
        )

        self.titleLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.titleLabel.setObjectName(
            "CardTitle"
        )

        layout.addWidget(
            self.titleLabel
        )

        self.descriptionLabel = QLabel(
            data.description
        )

        self.descriptionLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.descriptionLabel.setWordWrap(True)

        layout.addWidget(
            self.descriptionLabel
        )

    def setIcon(
        self,
        icon: str,
    ) -> None:
        """
        Update the displayed icon.
        """

        self.iconLabel.setPixmap(
            resources.icon(icon).pixmap(
                CARD_ICON_SIZE * 2,
                CARD_ICON_SIZE * 2,
            )
        )

    def setTitle(
        self,
        title: str,
    ) -> None:
        self.titleLabel.setText(title)

    def setDescription(
        self,
        description: str,
    ) -> None:
        self.descriptionLabel.setText(description)


__all__ = [
    "CardData",
    "BaseCard",
    "InfoCard",
    "ActionCard",
    "IconCard",
]