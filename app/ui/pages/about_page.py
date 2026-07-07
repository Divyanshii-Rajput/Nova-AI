"""
Nova AI Desktop Assistant
-------------------------

About Page

Displays application information.

Responsibilities
----------------
- Application information
- Version details
- Developer information
- Technology stack
- Useful links
- License information
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    APP_NAME,
    APP_VERSION,
    PAGE_SPACING,
    SPACE_16,
    SPACE_24,
)
from app.ui.resources import resources


class AboutPage(QWidget):
    """
    About Nova AI Desktop Assistant.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("AboutPage")

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

        layout.setSpacing(PAGE_SPACING)

        # ==================================================
        # Header
        # ==================================================

        header = QHBoxLayout()

        self.logo = QLabel()

        self.logo.setPixmap(
            resources.icon(
                "fa6s.robot"
            ).pixmap(
                72,
                72,
            )
        )

        header.addWidget(self.logo)

        details = QVBoxLayout()

        self.titleLabel = QLabel(APP_NAME)

        self.titleLabel.setObjectName(
            "PageTitle"
        )

        details.addWidget(
            self.titleLabel
        )

        self.versionLabel = QLabel(
            f"Version {APP_VERSION}"
        )

        self.versionLabel.setObjectName(
            "PageSubtitle"
        )

        details.addWidget(
            self.versionLabel
        )

        details.addStretch()

        header.addLayout(details)

        header.addStretch()

        layout.addLayout(header)

        # ==================================================
        # Description
        # ==================================================

        self.description = QTextBrowser()

        self.description.setOpenExternalLinks(
            True
        )

        self.description.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.description.setMarkdown(
            """
# Nova AI Desktop Assistant

Nova is a modern desktop AI assistant built with **Python** and **PySide6**.

## Features

- AI Chat
- Voice Assistant
- Browser Integration
- File Management
- Music Control
- Desktop Automation

Designed with a modern desktop experience inspired by ChatGPT Desktop, Cursor IDE and Windows Copilot.
"""
        )

        layout.addWidget(
            self.description
        )

        # ==================================================
        # Technology
        # ==================================================

        techFrame = QFrame()

        techLayout = QVBoxLayout(
            techFrame
        )

        techTitle = QLabel(
            "Technology Stack"
        )

        techTitle.setObjectName(
            "SectionTitle"
        )

        techLayout.addWidget(
            techTitle
        )

        self.techLabel = QLabel(
            "Python 3.13\n"
            "PySide6\n"
            "QtAwesome\n"
            "QSS\n"
            "SVG Icons\n"
            "PyInstaller"
        )

        self.techLabel.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        techLayout.addWidget(
            self.techLabel
        )

        layout.addWidget(
            techFrame
        )
    
            # ==================================================
        # Footer
        # ==================================================

        footer = QHBoxLayout()

        self.websiteButton = QPushButton(
            "Website"
        )

        self.githubButton = QPushButton(
            "GitHub"
        )

        self.documentationButton = QPushButton(
            "Documentation"
        )

        footer.addStretch()

        footer.addWidget(
            self.websiteButton
        )

        footer.addWidget(
            self.githubButton
        )

        footer.addWidget(
            self.documentationButton
        )

        layout.addStretch()

        layout.addLayout(
            footer
        )

    # ======================================================
    # Public API
    # ======================================================

    def set_version(
        self,
        version: str,
    ) -> None:
        """
        Update the displayed application version.
        """

        self.versionLabel.setText(
            f"Version {version}"
        )

    def set_description(
        self,
        markdown: str,
    ) -> None:
        """
        Update the about description.
        """

        self.description.setMarkdown(markdown)

    def set_technology_stack(
        self,
        technologies: list[str],
    ) -> None:
        """
        Update the displayed technology stack.
        """

        self.techLabel.setText(
            "\n".join(technologies)
        )

    def version(self) -> str:
        """
        Return the displayed version text.
        """

        return self.versionLabel.text()

    def description_text(self) -> str:
        """
        Return the current markdown/plain text.
        """

        return self.description.toPlainText()

    def technology_stack(self) -> list[str]:
        """
        Return the displayed technologies.
        """

        return [
            line
            for line in self.techLabel.text().splitlines()
            if line.strip()
        ]

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
    "AboutPage",
]