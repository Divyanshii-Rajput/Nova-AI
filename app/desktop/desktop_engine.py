from __future__ import annotations

import logging
from typing import Any

from app.desktop.app_launcher import AppLauncher
from app.desktop.folder_launcher import FolderLauncher
from app.models.response import Response

logger = logging.getLogger(__name__)


class DesktopEngine:
    """
    High-level desktop operations.

    Responsibilities
    ----------------
    • Launch desktop applications
    • Open folders
    • Delegate platform-specific work
      to launcher classes

    This class intentionally contains no
    Windows-specific implementation.
    """

    def __init__(self) -> None:

        logger.info("Initializing DesktopEngine...")

        self.app_launcher = AppLauncher()
        self.folder_launcher = FolderLauncher()

    # =====================================================
    # Helpers
    # =====================================================

    @staticmethod
    def _failure(message: str) -> Response:

        return Response(
            success=False,
            message=message,
        )

    @staticmethod
    def _success(
        message: str,
        data: Any = None,
    ) -> Response:

        return Response(
            success=True,
            message=message,
            data=data,
        )

    # =====================================================
    # Applications
    # =====================================================

    def open_app(
        self,
        app_name: str,
    ) -> Response:

        if app_name is None:

            return self._failure(
                "No application specified."
            )

        app_name = app_name.strip().lower()

        if not app_name:

            return self._failure(
                "No application specified."
            )

        logger.info(
            "Opening application: %s",
            app_name,
        )

        try:

            response = self.app_launcher.open(app_name)

            if response.success:
                logger.info(
                    "Application launched: %s",
                    app_name,
                )
                return response

            logger.warning(
                "Unable to launch application: %s",
                app_name,
            )

            return response

        except Exception:

            logger.exception(
                "Application launch failed."
            )

            return self._failure(
                "Failed to launch application."
            )

    # =====================================================
    # Folders
    # =====================================================

    def open_folder(
        self,
        folder_name: str,
    ) -> Response:

        if folder_name is None:

            return self._failure(
                "No folder specified."
            )

        folder_name = folder_name.strip().lower()

        if not folder_name:

            return self._failure(
                "No folder specified."
            )

        logger.info(
            "Opening folder: %s",
            folder_name,
        )

        try:

            success = self.folder_launcher.open(
                folder_name,
            )

            if success:

                logger.info(
                    "Folder opened: %s",
                    folder_name,
                )

                return self._success(
                    f"Opened folder: {folder_name}",
                    folder_name,
                )

            logger.warning(
                "Unable to open folder: %s",
                folder_name,
            )

            return self._failure(
                f"Unable to open folder: {folder_name}"
            )

        except Exception:

            logger.exception(
                "Folder open failed."
            )

            return self._failure(
                "Failed to open folder."
            )
        # =====================================================
    # Utilities
    # =====================================================

    def installed_apps(
        self,
    ):

        """
        Return all indexed applications.
        """

        try:

            return self.app_launcher.all()

        except Exception:

            logger.exception(
                "Failed to retrieve installed applications."
            )

            return []

    def app_exists(
        self,
        app_name: str,
    ) -> bool:

        if not app_name:
            return False

        try:

            return self.app_launcher.exists(
                app_name.strip().lower()
            )

        except Exception:

            logger.exception(
                "Application existence check failed."
            )

            return False

    def app_count(
        self,
    ) -> int:

        try:

            return len(self.app_launcher)

        except Exception:

            logger.exception(
                "Unable to count installed applications."
            )

            return 0

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> Response:

        logger.info(
            "Refreshing desktop application index..."
        )

        try:

            self.app_launcher.refresh()

            logger.info(
                "Desktop application index refreshed."
            )

            return self._success(
                "Desktop applications refreshed."
            )

        except Exception:

            logger.exception(
                "Desktop refresh failed."
            )

            return self._failure(
                "Unable to refresh desktop applications."
            )

    # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:

        return {

            "installed_apps":
                self.app_count(),

            "launcher":
                type(self.app_launcher).__name__,

            "folder_launcher":
                type(self.folder_launcher).__name__,

        }

    # =====================================================
    # Cleanup
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "DesktopEngine shutdown."
        )