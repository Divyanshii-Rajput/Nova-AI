from __future__ import annotations

import logging
from typing import Any

from app.models.response import Response
from app.music.youtube_player import YouTubePlayer
from app.music.spotify_player import SpotifyPlayer

logger = logging.getLogger(__name__)


class MusicEngine:
    """
    High-level music engine.

    Responsibilities
    ----------------
    • Play music
    • Delegate playback to YouTube or Spotify
    • Return Response objects
    • Provide platform statistics

    Default Platform
    ----------------
    YouTube
    """

    SUPPORTED_PLATFORMS = {

        "youtube",

        "spotify",

    }

    DEFAULT_PLATFORM = "youtube"

    def __init__(self) -> None:

        logger.info(
            "Initializing MusicEngine..."
        )

        self.youtube = YouTubePlayer()

        self.spotify = SpotifyPlayer()

    # =====================================================
    # Helpers
    # =====================================================

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

    @staticmethod
    def _failure(
        message: str,
    ) -> Response:

        return Response(
            success=False,
            message=message,
        )

    def _player(
        self,
        platform: str,
    ):

        if platform == "spotify":

            return self.spotify

        return self.youtube

    # =====================================================
    # Play
    # =====================================================

    def play(
        self,
        song: str,
        platform: str = DEFAULT_PLATFORM,
    ) -> Response:

        if song is None:

            return self._failure(
                "No song specified."
            )

        song = song.strip()

        if not song:

            return self._failure(
                "No song specified."
            )

        platform = (
            platform
            or self.DEFAULT_PLATFORM
        )

        platform = platform.lower().strip()

        if platform not in self.SUPPORTED_PLATFORMS:

            logger.warning(

                "Unsupported platform '%s'. "
                "Falling back to YouTube.",

                platform,

            )

            platform = self.DEFAULT_PLATFORM

        logger.info(

            "Playing '%s' using %s",

            song,

            platform,

        )

        try:

            player = self._player(platform)

            response = player.play(song)

            if not isinstance(
                response,
                Response,
            ):

                logger.error(

                    "%s returned invalid response.",

                    platform,

                )

                return self._failure(
                    "Music playback failed."
                )

            return response

        except Exception:

            logger.exception(

                "Music playback failed."

            )

            return self._failure(

                "Unable to play music."

            )

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        song: str,
    ):

        if not song:

            return []

        try:

            logger.info(

                "Searching song: %s",

                song,

            )

            return self.youtube.search(
                song,
            )

        except Exception:

            logger.exception(

                "Music search failed."

            )

            return []
    
        # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> Response:
        """
        Refresh all music providers.
        """

        logger.info(
            "Refreshing music providers..."
        )

        try:

            self.youtube.refresh()

            self.spotify.refresh()

            logger.info(
                "Music providers refreshed successfully."
            )

            return self._success(
                "Music providers refreshed."
            )

        except Exception:

            logger.exception(
                "Unable to refresh music providers."
            )

            return self._failure(
                "Unable to refresh music providers."
            )

    # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:
        """
        Return engine statistics.
        """

        try:

            youtube_stats = self.youtube.stats()

        except Exception:

            logger.exception(
                "Unable to retrieve YouTube statistics."
            )

            youtube_stats = {}

        try:

            spotify_stats = self.spotify.stats()

        except Exception:

            logger.exception(
                "Unable to retrieve Spotify statistics."
            )

            spotify_stats = {}

        return {

            "default_platform":
                self.DEFAULT_PLATFORM,

            "supported_platforms":
                sorted(
                    self.SUPPORTED_PLATFORMS
                ),

            "youtube":
                youtube_stats,

            "spotify":
                spotify_stats,

        }

    # =====================================================
    # Utilities
    # =====================================================

    def supported_platforms(
        self,
    ) -> list[str]:

        return sorted(
            self.SUPPORTED_PLATFORMS
        )

    def platform_exists(
        self,
        platform: str,
    ) -> bool:

        if not platform:

            return False

        return (

            platform
            .strip()
            .lower()

            in self.SUPPORTED_PLATFORMS

        )

    # =====================================================
    # Cleanup
    # =====================================================

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown all music providers.
        """

        logger.info(
            "Shutting down MusicEngine..."
        )

        try:

            self.youtube.shutdown()

        except Exception:

            logger.exception(
                "Failed to shutdown YouTube player."
            )

        try:

            self.spotify.shutdown()

        except Exception:

            logger.exception(
                "Failed to shutdown Spotify player."
            )

        logger.info(
            "MusicEngine shutdown complete."
        )