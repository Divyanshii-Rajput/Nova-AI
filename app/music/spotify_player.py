from __future__ import annotations

import logging
import urllib.parse
import webbrowser
from typing import Any

from app.models.response import Response

logger = logging.getLogger(__name__)


class SpotifyPlayer:
    """
    Spotify Player

    Opens Spotify search results in the user's
    default browser.
    """

    BASE_URL = "https://open.spotify.com/search/{}"

    def __init__(self) -> None:

        logger.info(
            "Initializing SpotifyPlayer..."
        )

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

    @staticmethod
    def _encode(
        text: str,
    ) -> str:

        return urllib.parse.quote_plus(
            text.strip(),
        )

    # =====================================================
    # Search URL
    # =====================================================

    def search(
        self,
        song: str,
    ) -> str:

        song = song.strip()

        return self.BASE_URL.format(
            self._encode(song)
        )

    # =====================================================
    # Play
    # =====================================================

    def play(
        self,
        song: str,
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

        try:

            url = self.search(song)

            logger.info(
                "Opening Spotify search: %s",
                song,
            )

            webbrowser.open(url)

            return self._success(
                f'Playing "{song}" on Spotify.',
                url,
            )

        except Exception:

            logger.exception(
                "Unable to open Spotify."
            )

            return self._failure(
                "Unable to open Spotify."
            )

    # =====================================================
    # Validation
    # =====================================================

    def exists(
        self,
        song: str,
    ) -> bool:

        return bool(
            song and song.strip()
        )

    # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:

        return {

            "platform": "Spotify",

            "base_url": self.BASE_URL,

        }

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> None:

        logger.info(
            "SpotifyPlayer refreshed."
        )

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "SpotifyPlayer shutdown."
        )