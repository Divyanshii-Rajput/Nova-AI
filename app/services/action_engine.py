## app/services/action_engine.py
import logging
from typing import Callable

from app.desktop.desktop_engine import DesktopEngine
from app.browser.browser_manager import BrowserManager
from app.desktop.app_launcher import AppLauncher
from app.files.file_engine import FileEngine
from app.music.music_engine import MusicEngine

from app.system.brightness import BrightnessController
from app.system.clipboard import ClipboardManager
from app.system.power import PowerController
from app.system.screenshot import Screenshot
from app.system.volume import VolumeController

from app.models.command import Command
from app.models.intent import Intent
from app.models.response import Response

logger = logging.getLogger(__name__)

class ActionEngine:
    """
    Central dispatcher for Nova.
    Routes intents to appropriate subsystem.
    """

    # Known Windows apps (aliases to launch commands)
    WINDOWS_APPS = {
        "calculator": "calc",
        "calc": "calc",
        "notepad": "notepad",
        "paint": "mspaint",
        "wordpad": "write",
        "cmd": "cmd",
        "command prompt": "cmd",
        "powershell": "powershell",
        "terminal": "wt",
        "windows terminal": "wt",
        "explorer": "explorer",
        "file explorer": "explorer",
        "settings": "ms-settings:",
        "control": "control",
        "control panel": "control",
        "device manager": "devmgmt.msc",
        "disk management": "diskmgmt.msc",
        "services": "services.msc",
        "event viewer": "eventvwr",
        "task scheduler": "taskschd.msc",
        "snipping tool": "snippingtool",
        "camera": "microsoft.windows.camera:",
        # Aliases for Control Panel (e.g. "CP", "CPC")
        "cp": "control",
        "cpc": "control",
        "vs code": "code",
        "vscode": "code",
        "visual studio code": "code",
    }

    def __init__(self) -> None:
        logger.info("Initializing ActionEngine...")
        self.desktop = DesktopEngine()
        self.browser = BrowserManager()
        self.files = FileEngine()
        self.music = MusicEngine()
        self.volume = VolumeController()
        self.brightness = BrightnessController()
        self.screenshot = Screenshot()
        self.clipboard = ClipboardManager()
        self.power = PowerController()
        self._ai = None  # Lazy-loaded Gemini engine

        self.handlers: dict[Intent, Callable[[Command], Response]] = {
            Intent.OPEN_APP:         self._handle_open_app,
            Intent.OPEN_FOLDER:      self._handle_open_folder,
            Intent.OPEN_FILE:        self._handle_open_file,
            Intent.OPEN_WEBSITE:     self._handle_open_website,
            Intent.SEARCH_WEB:       self._handle_search,
            Intent.PLAY_MUSIC:       self._handle_music,
            Intent.SYSTEM_CONTROL:   self._handle_system,
            Intent.TAKE_SCREENSHOT:  self._handle_screenshot,
            Intent.AI_CHAT:          self._handle_ai,
            Intent.EXIT:             self._handle_exit,
        }

    @property
    def ai(self):
        if self._ai is None:
            logger.info("Loading LLMRouter Engine...")
            from app.llm.llm_router import LLMRouter
            self._ai = LLMRouter()
        return self._ai

    # Helper to get entity string
    def _entity(self, command: Command) -> str:
        return (command.entity or "").strip().lower()

    def _builtin(self, entity: str) -> bool:
        return entity in self.WINDOWS_APPS

    def _builtin_name(self, entity: str) -> str:
        return self.WINDOWS_APPS[entity]

    # ---------------------
    # Execute
    # ---------------------
    def execute(self, command: Command) -> Response:
        handler = self.handlers.get(command.intent)
        if handler is None:
            return Response(success=False, message="Unsupported command.")
        try:
            logger.info("Executing %s", command.intent.name)
            return handler(command)
        except Exception:
            logger.exception("Action execution failed.")
            return Response(success=False, message="Action execution failed.")

    # ---------------------
    # Handlers
    # ---------------------

    def _handle_open_app(self, command: Command) -> Response:
        entity = self._entity(command)
        if not entity:
            return Response(success=False, message="Which application should I open?")

        # Fuzzy match websites first to make website opening highly tolerant
        import difflib
        web_matches = difflib.get_close_matches(entity, ["youtube", "leetcode", "whatsapp"], n=1, cutoff=0.75)
        if web_matches:
            matched_web = web_matches[0]
            logger.info("Fuzzy matched website entity from '%s' to '%s'", entity, matched_web)
            entity = matched_web

        # Handle common websites explicitly
        if "youtube" in entity:
            logger.info("Launching YouTube website")
            return self.browser.open_website("youtube.com")
        if "leetcode" in entity:
            logger.info("Launching LeetCode website")
            return self.browser.open_website("leetcode.com")
        if "whatsapp" in entity:
            logger.info("Launching WhatsApp app with protocol")
            try:
                import subprocess
                subprocess.Popen("start whatsapp:", shell=True)
                return Response(success=True, message="Opened WhatsApp.")
            except Exception:
                logger.warning("WhatsApp protocol failed, falling back to Web WhatsApp")
                return self.browser.open_website("web.whatsapp.com")

        # Fuzzy match built-in Windows apps to make app launching spelling-tolerant
        app_keys = list(self.WINDOWS_APPS.keys())
        app_matches = difflib.get_close_matches(entity, app_keys, n=1, cutoff=0.55)
        if app_matches:
            matched_app = app_matches[0]
            logger.info("Fuzzy matched app entity from '%s' to '%s'", entity, matched_app)
            entity = matched_app

        # 1. Built-in Windows Apps
        if self._builtin(entity):
            logger.info("Launching built-in app: %s", entity)
            return self.desktop.open_app(self._builtin_name(entity))

        # 2. Known Websites (via BrowserManager)
        logger.info("Checking known websites...")
        try:
            response = self.browser.open_website(entity)
            if response.success:
                return response
        except Exception:
            logger.exception("Website lookup failed.")

        # 3. Installed Applications (DesktopEngine search)
        logger.info("Searching installed applications...")
        try:
            response = self.desktop.open_app(entity)
            if response.success:
                return response
        except Exception:
            logger.exception("Application search failed.")

        # 4. Indexed Files (FileEngine search)
        logger.info("Searching indexed files...")
        try:
            response = self.files.open(entity)
            if response.success:
                return response
        except Exception:
            logger.exception("File search failed.")

        # 5. Google Search fallback
        logger.info("Performing Google search as fallback...")
        try:
            response = self.browser.search_google(entity)
            if response.success:
                return response
        except Exception:
            logger.exception("Google search failed.")

        # 6. AI Fallback: Let the LLM suggest best match
        logger.info("Falling back to AI for best match suggestion")
        ai_prompt = (
            f"The user asked to open:\n\n{entity}\n\n"
            "Explain briefly what it is and suggest the closest match.\n"
            "Maximum 60 words."
        )
        return self.ai.chat(ai_prompt)

    def _handle_open_folder(self, command: Command) -> Response:
        return self.desktop.open_folder(self._entity(command))

    def _handle_open_file(self, command: Command) -> Response:
        return self.files.open(self._entity(command))

    def _handle_open_website(self, command: Command) -> Response:
        return self.browser.open_website(self._entity(command))

    def _handle_search(self, command: Command) -> Response:
        return self.browser.search_google(self._entity(command))

    def _handle_music(self, command: Command) -> Response:
        entity = self._entity(command)
        platform = "youtube"
        if "on spotify" in entity:
            platform = "spotify"
            entity = entity.replace("on spotify", "").strip()
        elif "on youtube" in entity:
            platform = "youtube"
            entity = entity.replace("on youtube", "").strip()
        return self.music.play(entity, platform=platform)


    def _handle_screenshot(self, command: Command) -> Response:
        try:
            path = self.screenshot.capture()
            return Response(success=True, message="Screenshot captured successfully.", data=path)
        except Exception:
            logger.exception("Screenshot capture failed.")
            return Response(success=False, message="Unable to capture screenshot.")

    def _handle_system(self, command: Command) -> Response:
        entity = self._entity(command)
        try:
            # Volume controls
            if "volume" in entity:
                if any(word in entity for word in ("increase", "up", "raise", "higher")):
                    self.volume.increase()
                elif any(word in entity for word in ("decrease", "down", "lower")):
                    self.volume.decrease()
                elif "mute" in entity:
                    self.volume.mute()
                elif "unmute" in entity:
                    self.volume.unmute()
                return Response(success=True, message="Volume updated.")

            # Brightness controls
            if "brightness" in entity:
                if any(word in entity for word in ("increase", "up", "raise")):
                    self.brightness.increase()
                elif any(word in entity for word in ("decrease", "down", "lower")):
                    self.brightness.decrease()
                return Response(success=True, message="Brightness updated.")

            # Power management
            if "shutdown" in entity:
                self.power.shutdown()
            elif "restart" in entity:
                self.power.restart()
            elif "sleep" in entity:
                self.power.sleep()
            elif "lock" in entity:
                self.power.lock()
            elif "logout" in entity:
                self.power.logout()
            else:
                return Response(success=False, message="Unknown system command.")

            return Response(success=True, message="System command executed.")
        except Exception:
            logger.exception("System command failed.")
            return Response(success=False, message="Unable to execute system command.")

    def _handle_ai(self, command: Command) -> Response:
        # Chat with AI using the original user text (preserve user phrasing)
        return self.ai.chat(command.original_text)

    def _handle_exit(self, command: Command) -> Response:
        return Response(success=True, message="Goodbye!")

    # ---------------------
    # Utilities
    # ---------------------

    def stats(self) -> dict:
        return {
            "desktop": type(self.desktop).__name__,
            "browser": type(self.browser).__name__,
            "files": type(self.files).__name__,
            "music": type(self.music).__name__,
            "ai_loaded": self._ai is not None,
        }

    def refresh(self) -> Response:
        """
        Refresh caches or indices in subsystems (if supported).
        """
        logger.info("Refreshing ActionEngine subsystems...")
        errors: list[str] = []
        for name, engine in (("desktop", self.desktop),
                             ("browser", self.browser),
                             ("files", self.files),
                             ("music", self.music)):
            refresh_fn = getattr(engine, "refresh", None)
            if callable(refresh_fn):
                try:
                    refresh_fn()
                except Exception:
                    logger.exception("Failed to refresh %s.", name)
                    errors.append(name)
        if errors:
            return Response(
                success=False,
                message="Failed to refresh: " + ", ".join(errors),
                data=errors
            )
        return Response(success=True, message="Action Engine refreshed.")

    def shutdown(self) -> None:
        """
        Clean up or close any resources held by subsystems.
        """
        logger.info("Shutting down ActionEngine...")
        for name, engine in (("desktop", self.desktop),
                             ("browser", self.browser),
                             ("files", self.files),
                             ("music", self.music)):
            shutdown_fn = getattr(engine, "shutdown", None)
            if callable(shutdown_fn):
                try:
                    shutdown_fn()
                except Exception:
                    logger.exception("Failed to shutdown %s.", name)
        # Release AI engine if loaded
        if self._ai is not None:
            logger.info("Releasing Gemini engine.")
            self._ai = None
        logger.info("ActionEngine shutdown complete.")
