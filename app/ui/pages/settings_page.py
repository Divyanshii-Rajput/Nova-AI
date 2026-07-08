"""
Nova AI Desktop Assistant
-------------------------

Settings Page

Application configuration interface.

Responsibilities
----------------
- Theme settings
- Startup options
- Voice settings
- AI settings
- General preferences

Backend integration is implemented in Sprint 5.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QApplication,
    QPushButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    PAGE_SPACING,
    SPACE_16,
)

from app.ui.constants import ThemeMode
from app.ui.theme import theme_manager

class SettingsPage(QWidget):
    """
    Application settings page.
    """

    settingsChanged = Signal()

    resetRequested = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName("SettingsPage")

        self._build_ui()
        self._load_settings_into_ui()


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
        # Appearance
        # ==================================================

        appearance = QFrame()

        appearance.setObjectName(
            "SettingsSection"
        )

        appearance_form = QFormLayout(
            appearance
        )

        appearance_form.setSpacing(12)

        self.themeCombo = QComboBox()

        self.themeCombo.addItems(
            [
                "System",
                "Dark",
                "Light",
            ]
        )

        appearance_form.addRow(
            "Theme",
            self.themeCombo,
        )

        self.startupCheck = QCheckBox(
            "Launch Nova on system startup"
        )

        appearance_form.addRow(
            "",
            self.startupCheck,
        )

        layout.addWidget(
            appearance
        )

        # ==================================================
        # Voice
        # ==================================================

        voice = QFrame()

        voice.setObjectName(
            "SettingsSection"
        )

        voice_form = QFormLayout(
            voice
        )

        self.voiceCombo = QComboBox()

        self.voiceCombo.addItems(
            [
                "Default",
                "Female",
                "Male",
            ]
        )

        voice_form.addRow(
            "Voice",
            self.voiceCombo,
        )

        self.volumeSlider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.volumeSlider.setRange(
            0,
            100,
        )

        self.volumeSlider.setValue(75)

        voice_form.addRow(
            "Volume",
            self.volumeSlider,
        )

        layout.addWidget(
            voice
        )

        # ==================================================
        # AI
        # ==================================================

        ai = QFrame()

        ai.setObjectName(
            "SettingsSection"
        )

        ai_form = QFormLayout(ai)

        self.modelCombo = QComboBox()

        self.modelCombo.addItems(
            [
                "Gemini",
                "OpenAI",
                "Custom",
            ]
        )

        ai_form.addRow(
            "AI Model",
            self.modelCombo,
        )

        self.temperature = QSpinBox()

        self.temperature.setRange(
            0,
            100,
        )

        self.temperature.setValue(50)

        ai_form.addRow(
            "Temperature",
            self.temperature,
        )

        layout.addWidget(ai)
    
            # ==================================================
        # Actions
        # ==================================================

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.resetButton = QPushButton(
            "Reset"
        )

        self.saveButton = QPushButton(
            "Save"
        )

        buttons.addWidget(
            self.resetButton
        )

        buttons.addWidget(
            self.saveButton
        )

        layout.addStretch()

        layout.addLayout(
            buttons
        )

        # ==================================================
        # Signals
        # ==================================================

        self.themeCombo.currentIndexChanged.connect(
            self._apply_theme
        )

        self.themeCombo.currentIndexChanged.connect(
            self.settingsChanged
        )

        self.startupCheck.toggled.connect(
            self.settingsChanged
        )

        self.voiceCombo.currentIndexChanged.connect(
            self.settingsChanged
        )

        self.volumeSlider.valueChanged.connect(
            self.settingsChanged
        )

        self.modelCombo.currentIndexChanged.connect(
            self.settingsChanged
        )

        self.temperature.valueChanged.connect(
            self.settingsChanged
        )

        self.resetButton.clicked.connect(
            self.reset
        )

        self.saveButton.clicked.connect(
            self.save_settings_from_ui
        )


    # ======================================================
    # Public API
    # ======================================================

    def values(self) -> dict:
        """
        Return all current settings.
        """

        return {
            "theme": self.themeCombo.currentText(),
            "startup": self.startupCheck.isChecked(),
            "voice": self.voiceCombo.currentText(),
            "volume": self.volumeSlider.value(),
            "model": self.modelCombo.currentText(),
            "temperature": self.temperature.value(),
        }

    def reset(self) -> None:
        """
        Restore default settings.
        """

        self.themeCombo.setCurrentIndex(0)

        self.startupCheck.setChecked(False)

        self.voiceCombo.setCurrentIndex(0)

        self.volumeSlider.setValue(75)

        self.modelCombo.setCurrentIndex(0)

        self.temperature.setValue(50)

        self.resetRequested.emit()
        self.save_settings_from_ui()

    def _load_settings_into_ui(self) -> None:
        from app.config.settings import Settings
        Settings.load()

        # Set Theme
        theme_idx = self.themeCombo.findText(Settings.THEME)
        if theme_idx >= 0:
            self.themeCombo.setCurrentIndex(theme_idx)

        # Set Startup
        self.startupCheck.setChecked(Settings.STARTUP)

        # Set Voice
        voice_idx = self.voiceCombo.findText(Settings.VOICE)
        if voice_idx >= 0:
            self.voiceCombo.setCurrentIndex(voice_idx)

        # Set Volume
        self.volumeSlider.setValue(Settings.VOLUME)

        # Set AI Model
        model_idx = self.modelCombo.findText(Settings.MODEL)
        if model_idx >= 0:
            self.modelCombo.setCurrentIndex(model_idx)

        # Set Temperature
        self.temperature.setValue(Settings.TEMPERATURE)

    def save_settings_from_ui(self) -> None:
        from app.config.settings import Settings
        
        # Get values from UI
        Settings.THEME = self.themeCombo.currentText()
        Settings.STARTUP = self.startupCheck.isChecked()
        Settings.VOICE = self.voiceCombo.currentText()
        Settings.VOLUME = self.volumeSlider.value()
        Settings.MODEL = self.modelCombo.currentText()
        Settings.TEMPERATURE = self.temperature.value()

        # Save to settings.json
        Settings.save()
        
        # Emit signal to notify other components
        self.settingsChanged.emit()


    # ======================================================
    # Utilities
    # ======================================================

    def sizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(1200, 800)

    def minimumSizeHint(self):
        from PySide6.QtCore import QSize

        return QSize(900, 600)

    def _apply_theme(self) -> None:
        """
        Apply selected theme.
        """

        selected = self.themeCombo.currentText()

        if selected == "Dark":

            theme_manager.apply_theme(
                QApplication.instance(),
                ThemeMode.DARK,
            )

        elif selected == "Light":

            theme_manager.apply_theme(
                QApplication.instance(),
                ThemeMode.LIGHT,
            )

        else:

            theme_manager.apply_theme(
                QApplication.instance(),
                ThemeMode.SYSTEM,
            )

__all__ = [
    "SettingsPage",
]