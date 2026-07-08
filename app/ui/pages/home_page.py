"""
Nova AI Desktop Assistant
-------------------------

Home Page

Modern, elegant, and minimal assistant dashboard experience.
"""

from __future__ import annotations

import re
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.ui.constants import (
    PAGE_SPACING,
    SPACE_24,
)
from app.ui.widgets.microphone_widget import (
    MicrophoneWidget,
)

class HomePage(QWidget):
    """
    Assistant dashboard page.
    """

    start_voice_requested = Signal()
    stop_voice_requested = Signal()
    browserRequested = Signal()
    filesRequested = Signal()
    musicRequested = Signal()
    commandTriggered = Signal(str)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("HomePage")
        self._voice_running = False
        
        # Backwards compatibility dummy status widget
        self.statusWidget = QWidget()

        self._build_ui()
        self.update_interaction_history()

    # ======================================================
    # UI
    # ======================================================

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE_24, SPACE_24, SPACE_24, SPACE_24)
        root.setSpacing(PAGE_SPACING)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        root.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(28)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # --------------------------------------------------
        # 1. Branding Header
        # --------------------------------------------------
        self.brand_title = QLabel("NOVA AI")
        self.brand_title.setObjectName("PageTitle")
        self.brand_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.brand_title)

        self.brand_subtitle = QLabel("Your Intelligent Desktop Assistant")
        self.brand_subtitle.setObjectName("PageSubtitle")
        self.brand_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.brand_subtitle)

        layout.addSpacing(5)

        # --------------------------------------------------
        # 2. Assistant Core (Status, Mic, Prompt)
        # --------------------------------------------------
        self.statusLabel = QLabel("⚪ Standby")
        self.statusLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #7B8494;")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.statusLabel)

        self.microphone = MicrophoneWidget()
        self.microphone.clicked.connect(self._toggle_voice)
        layout.addWidget(self.microphone, alignment=Qt.AlignmentFlag.AlignCenter)

        self.promptLabel = QLabel("How can I help today?")
        self.promptLabel.setStyleSheet("font-size: 16px; font-weight: 500; color: #E8EAED;")
        self.promptLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.promptLabel)

        layout.addSpacing(10)

        # --------------------------------------------------
        # 3. Last Command & Response Container
        # --------------------------------------------------
        self.lastInteractionFrame = QFrame()
        self.lastInteractionFrame.setObjectName("ActivityFrame")
        self.lastInteractionFrame.setMinimumWidth(520)
        self.lastInteractionFrame.setMaximumWidth(520)
        self.lastInteractionFrame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.lastInteractionFrame.setStyleSheet("""
            #ActivityFrame {
                background-color: #151820;
                border: 1px solid #242936;
                border-radius: 12px;
            }
        """)
        interaction_layout = QVBoxLayout(self.lastInteractionFrame)
        interaction_layout.setContentsMargins(18, 18, 18, 18)
        interaction_layout.setSpacing(10)

        self.lastCommandTitle = QLabel("LAST COMMAND")
        self.lastCommandTitle.setStyleSheet("font-size: 11px; font-weight: bold; color: #5B8CFF; letter-spacing: 1px;")
        self.lastCommandText = QLabel("None")
        self.lastCommandText.setWordWrap(True)
        self.lastCommandText.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        self.lastCommandText.setStyleSheet("font-size: 14px; color: #E8EAED;")

        self.lastResponseTitle = QLabel("NOVA RESPONSE")
        self.lastResponseTitle.setStyleSheet("font-size: 11px; font-weight: bold; color: #2ECC71; letter-spacing: 1px;")
        self.lastResponseText = QLabel("None")
        self.lastResponseText.setWordWrap(True)
        self.lastResponseText.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        self.lastResponseText.setStyleSheet("font-size: 14px; color: #A8AFBC;")

        interaction_layout.addWidget(self.lastCommandTitle)
        interaction_layout.addWidget(self.lastCommandText)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("background-color: #242936; max-height: 1px; border: none;")
        interaction_layout.addWidget(divider)

        interaction_layout.addWidget(self.lastResponseTitle)
        interaction_layout.addWidget(self.lastResponseText)

        layout.addWidget(self.lastInteractionFrame, alignment=Qt.AlignmentFlag.AlignCenter)

        # --------------------------------------------------
        # 4. Recent Commands Section
        # --------------------------------------------------
        self.recentFrame = QFrame()
        self.recentFrame.setFixedWidth(520)
        recent_layout = QVBoxLayout(self.recentFrame)
        recent_layout.setContentsMargins(0, 0, 0, 0)
        recent_layout.setSpacing(8)

        recent_title = QLabel("Recent Commands")
        recent_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E8EAED;")
        recent_layout.addWidget(recent_title)

        self.recentButtonsList: list[QPushButton] = []
        for _ in range(4):
            btn = QPushButton("• None")
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    background: transparent;
                    border: none;
                    color: #A8AFBC;
                    padding: 4px 0px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    color: #5B8CFF;
                }
            """)
            btn.setVisible(False)
            btn.clicked.connect(self._on_recent_clicked)
            recent_layout.addWidget(btn)
            self.recentButtonsList.append(btn)

        layout.addWidget(self.recentFrame, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(5)

        # --------------------------------------------------
        # 5. Quick Actions Section
        # --------------------------------------------------
        self.quickFrame = QFrame()
        self.quickFrame.setFixedWidth(520)
        quick_layout = QVBoxLayout(self.quickFrame)
        quick_layout.setContentsMargins(0, 0, 0, 0)
        quick_layout.setSpacing(10)

        quick_actions_title = QLabel("Quick Actions")
        quick_actions_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E8EAED;")
        quick_layout.addWidget(quick_actions_title)

        pills_layout = QHBoxLayout()
        pills_layout.setSpacing(12)

        calc_btn = QPushButton("Calculator")
        browser_btn = QPushButton("Browser")
        files_btn = QPushButton("Files")
        music_btn = QPushButton("Music")

        pill_style = """
            QPushButton {
                background-color: #151820;
                color: #A8AFBC;
                border: 1px solid #242936;
                border-radius: 16px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #242936;
                color: #FFFFFF;
                border-color: #5B8CFF;
            }
            QPushButton:pressed {
                background-color: #111318;
            }
        """
        for btn in [calc_btn, browser_btn, files_btn, music_btn]:
            btn.setStyleSheet(pill_style)
            pills_layout.addWidget(btn)

        quick_layout.addLayout(pills_layout)
        layout.addWidget(self.quickFrame, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        # Wire up pills
        calc_btn.clicked.connect(lambda: self.commandTriggered.emit("open calculator"))
        browser_btn.clicked.connect(self.browserRequested)
        files_btn.clicked.connect(self.filesRequested)
        music_btn.clicked.connect(self.musicRequested)

    # ======================================================
    # Public API
    # ======================================================

    def setStatus(self, text: str) -> None:
        """
        Update assistant status.
        """
        self.statusLabel.setText(text)

    def setRecentActivity(self, text: str) -> None:
        """
        Fallback implementation for updates.
        """
        self.update_interaction_history()

    def microphoneWidget(self) -> MicrophoneWidget:
        """
        Return the microphone widget.
        """
        return self.microphone

    def _toggle_voice(self) -> None:
        if self._voice_running:
            self.stop_voice_requested.emit()
        else:
            self.start_voice_requested.emit()

    def on_voice_state_changed(self, state: str) -> None:
        """
        Update HomePage status, prompt text and microphone animation based on controller state.
        """
        if state == "Listening...":
            self.statusLabel.setText("🟢 Listening...")
            self.statusLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #2ECC71;")
            self.promptLabel.setText("How can I help today?")
            self.microphone.setListening(True)
            self.microphone.setThinking(False)
            self.microphone.setSpeaking(False)
            self._voice_running = True
        elif state == "Thinking...":
            self.statusLabel.setText("🟡 Thinking...")
            self.statusLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #F4B400;")
            self.promptLabel.setText("Thinking...")
            self.microphone.setListening(False)
            self.microphone.setThinking(True)
            self.microphone.setSpeaking(False)
            self._voice_running = True
        elif state == "Speaking...":
            self.statusLabel.setText("🔵 Speaking...")
            self.statusLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #5B8CFF;")
            self.promptLabel.setText("Speaking...")
            self.microphone.setListening(False)
            self.microphone.setThinking(False)
            self.microphone.setSpeaking(True)
            self._voice_running = True
        elif state.startswith("Standby"):
            self.statusLabel.setText(f"⚪ {state}")
            self.statusLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #7B8494;")
            self.promptLabel.setText("Say 'Hey Nova' to wake me up")
            self.microphone.reset()
            self._voice_running = True
        else:
            self.statusLabel.setText("⚪ Standby")
            self.statusLabel.setStyleSheet("font-size: 15px; font-weight: bold; color: #7B8494;")
            self.promptLabel.setText("How can I help today?")
            self.microphone.reset()
            self._voice_running = False

    def _on_recent_clicked(self) -> None:
        btn = self.sender()
        if isinstance(btn, QPushButton):
            cmd = btn.property("command")
            if cmd:
                self.commandTriggered.emit(cmd)

    def update_interaction_history(self) -> None:
        """
        Loads from global conversation memory and refreshes Home UI.
        """
        from app.memory.conversation_memory import conversation_memory
        history = conversation_memory.all()

        # 1. Update Last Command / Response
        if history:
            last = history[0]
            user_clean = re.sub(r"\*\*|`", "", last.user)
            assistant_clean = re.sub(r"\*\*|`", "", last.assistant)

            self.lastCommandText.setText(user_clean)
            self.lastResponseText.setText(assistant_clean)
            self.lastInteractionFrame.setVisible(True)
        else:
            self.lastCommandText.setText("None")
            self.lastResponseText.setText("None")
            self.lastInteractionFrame.setVisible(False)

        # 2. Update Recent Commands list (unique list to avoid duplicates)
        unique_commands = []
        for item in history:
            cmd = item.user.strip()
            # Strip phonetic wake word variants cleanly
            cmd_clean = re.sub(r"^(hey\s+)?(nova|noha|noah|nowa|lova|ova|noba|no\s+va)\b", "", cmd, flags=re.IGNORECASE).strip()
            cmd_clean = re.sub(r"^[^\w]+|[^\w]+$", "", cmd_clean).strip()
            if not cmd_clean:
                cmd_clean = cmd
            if cmd_clean and cmd_clean not in unique_commands:
                unique_commands.append(cmd_clean)
            if len(unique_commands) >= 4:
                break

        for idx, btn in enumerate(self.recentButtonsList):
            if idx < len(unique_commands):
                cmd_val = unique_commands[idx]
                btn.setText(f"• {cmd_val}")
                btn.setProperty("command", cmd_val)
                btn.setVisible(True)
            else:
                btn.setVisible(False)

        if not unique_commands:
            self.recentFrame.setVisible(False)
        else:
            self.recentFrame.setVisible(True)

    def status(self) -> QWidget:
        """
        Return backwards compatible dummy status widget.
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