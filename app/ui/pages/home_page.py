"""
Nova AI Desktop Assistant
-------------------------

Home Page

Landing page displayed after the application starts.

Inspired by ChatGPT Desktop, Cursor IDE and Windows Copilot.

Responsibilities
----------------
- Welcome section
- Quick actions
- Assistant status
- Recent activity
- Suggested tasks
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    CARD_SPACING,
    PAGE_SPACING,
    SPACE_16,
    SPACE_24,
)
from app.ui.widgets.cards import (
    ActionCard,
    CardData,
)
from app.ui.widgets.microphone_widget import (
    MicrophoneWidget,
)
from app.ui.widgets.status_widget import (
    StatusWidget,
)


class HomePage(QWidget):
    """
    Main landing page.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("HomePage")

        self._build_ui()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:

        root = QVBoxLayout(self)

        root.setContentsMargins(
            SPACE_24,
            SPACE_24,
            SPACE_24,
            SPACE_24,
        )

        root.setSpacing(PAGE_SPACING)

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        root.addWidget(scroll)

        container = QWidget()

        scroll.setWidget(container)

        layout = QVBoxLayout(container)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(PAGE_SPACING)

        # ==================================================
        # Header
        # ==================================================

        title = QLabel(
            "Welcome to Nova AI"
        )

        title.setObjectName(
            "PageTitle"
        )

        layout.addWidget(title)

        subtitle = QLabel(
            "Your intelligent desktop assistant."
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        layout.addWidget(subtitle)

        # ==================================================
        # Assistant
        # ==================================================

        assistant_row = QHBoxLayout()

        assistant_row.setSpacing(
            SPACE_24
        )

        self.microphone = (
            MicrophoneWidget()
        )

        assistant_row.addWidget(
            self.microphone,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        self.statusWidget = (
            StatusWidget()
        )

        assistant_row.addWidget(
            self.statusWidget
        )

        assistant_row.addStretch()

        layout.addLayout(
            assistant_row
        )

        # ==================================================
        # Quick Actions
        # ==================================================

        quick_title = QLabel(
            "Quick Actions"
        )

        quick_title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(
            quick_title
        )

        self.cardsLayout = QGridLayout()

        self.cardsLayout.setSpacing(
            CARD_SPACING
        )

        layout.addLayout(
            self.cardsLayout
        )
    
        cards = [

            CardData(
                title="Start Voice Assistant",
                description="Begin a conversation with Nova using your microphone.",
                icon="fa6s.microphone",
                action_text="Start",
            ),

            CardData(
                title="Open Browser",
                description="Browse the web using Nova's integrated browser.",
                icon="fa6s.globe",
                action_text="Open",
            ),

            CardData(
                title="Search Files",
                description="Find files instantly using natural language.",
                icon="fa6s.folder-open",
                action_text="Search",
            ),

            CardData(
                title="Play Music",
                description="Control music playback with voice commands.",
                icon="fa6s.music",
                action_text="Launch",
            ),

        ]

        row = 0
        column = 0

        for card in cards:

            widget = ActionCard(card)

            self.cardsLayout.addWidget(
                widget,
                row,
                column,
            )

            column += 1

            if column == 2:
                column = 0
                row += 1

        # ==================================================
        # Recent Activity
        # ==================================================

        recent_title = QLabel("Recent Activity")

        recent_title.setObjectName(
            "SectionTitle"
        )

        layout.addWidget(recent_title)

        self.activityFrame = QFrame()

        self.activityFrame.setObjectName(
            "ActivityFrame"
        )

        activity_layout = QVBoxLayout(
            self.activityFrame
        )

        activity_layout.setContentsMargins(
            SPACE_16,
            SPACE_16,
            SPACE_16,
            SPACE_16,
        )

        activity_layout.setSpacing(10)

        self.activityLabel = QLabel(
            "No recent activity."
        )

        self.activityLabel.setWordWrap(True)

        activity_layout.addWidget(
            self.activityLabel
        )

        layout.addWidget(
            self.activityFrame
        )

        layout.addStretch()

    # ======================================================
    # Public API
    # ======================================================

    def setStatus(
        self,
        text: str,
    ) -> None:
        """
        Update assistant status.
        """

        self.statusWidget.setStatus(text)

    def setRecentActivity(
        self,
        text: str,
    ) -> None:
        """
        Update recent activity.
        """

        self.activityLabel.setText(text)

    def microphoneWidget(
        self,
    ) -> MicrophoneWidget:
        """
        Return the microphone widget.
        """

        return self.microphone

    def status(
        self,
    ) -> StatusWidget:
        """
        Return the status widget.
        """

        return self.statusWidget

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(1200, 800)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(900, 600)


__all__ = [
    "HomePage",
]