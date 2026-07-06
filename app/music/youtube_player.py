from __future__ import annotations

import logging
import webbrowser
from typing import Any

import yt_dlp

from app.models.response import Response

logger = logging.getLogger(__name__)


class YouTubePlayer:
    """
    Production YouTube Player.

    Features
    --------
    • Search first matching video
    • Play playlists
    • Browser playback
    • yt-dlp backend
    • Robust search
    """

    DEFAULT_OPTIONS = {

        "quiet": True,

        "no_warnings": True,

        "extract_flat": True,

        "skip_download": True,

        "noplaylist": True,

    }

    PLAYLIST_OPTIONS = {

        "quiet": True,

        "no_warnings": True,

        "extract_flat": True,

        "skip_download": True,

    }

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Initializing YouTubePlayer..."
        )

        self.ydl_options = dict(
            self.DEFAULT_OPTIONS
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

    def _browser(
        self,
        url: str,
        message: str,
    ) -> Response:

        try:

            opened = webbrowser.open(

                url,

                new=2,

            )

            if not opened:

                return self._failure(
                    "Unable to open browser."
                )

            logger.info(

                "Opened browser: %s",

                url,

            )

            return self._success(

                message,

                url,

            )

        except Exception:

            logger.exception(
                "Browser launch failed."
            )

            return self._failure(
                "Unable to open browser."
            )

    # =====================================================
    # Search
    # =====================================================

    def first_video(
        self,
        query: str,
    ) -> str | None:

        query = query.strip()

        if not query:

            return None

        try:

            with yt_dlp.YoutubeDL(
                self.ydl_options,
            ) as ydl:

                result = ydl.extract_info(

                    f"ytsearch5:{query}",

                    download=False,

                )

                if not result:

                    return None

                entries = result.get(
                    "entries",
                    [],
                )

                if not entries:

                    return None

                for item in entries:

                    video_id = item.get(
                        "id"
                    )

                    if not video_id:
                        continue

                    return (
                        "https://www.youtube.com/watch?v="
                        + video_id
                    )

                return None

        except Exception as exc:

            logger.exception(

                "YouTube search failed: %s",

                exc,

            )

            return None
    
        # =====================================================
    # Play
    # =====================================================

    def play(
        self,
        query: str,
    ) -> Response:

        if query is None:

            return self._failure(
                "No song specified."
            )

        query = query.strip()

        if not query:

            return self._failure(
                "No song specified."
            )

        logger.info(
            "Searching YouTube: %s",
            query,
        )

        url = self.first_video(
            query,
        )

        if url is None:

            return self._failure(
                "Unable to find the requested video."
            )

        return self._browser(

            url,

            f'Playing "{query}"',

        )

    # =====================================================
    # Search (without playing)
    # =====================================================

    def search(
        self,
        query: str,
    ) -> str | None:

        return self.first_video(
            query,
        )

    # =====================================================
    # Play URL
    # =====================================================

    def play_url(
        self,
        url: str,
    ) -> Response:

        if url is None:

            return self._failure(
                "No URL specified."
            )

        url = url.strip()

        if not url:

            return self._failure(
                "No URL specified."
            )

        logger.info(
            "Opening YouTube URL: %s",
            url,
        )

        return self._browser(

            url,

            "Opening YouTube...",

        )

    # =====================================================
    # Playlist
    # =====================================================

    def play_playlist(
        self,
        query: str,
    ) -> Response:

        if query is None:

            return self._failure(
                "No playlist specified."
            )

        query = query.strip()

        if not query:

            return self._failure(
                "No playlist specified."
            )

        logger.info(
            "Searching playlist: %s",
            query,
        )

        try:

            with yt_dlp.YoutubeDL(
                self.PLAYLIST_OPTIONS,
            ) as ydl:

                result = ydl.extract_info(

                    f"ytsearch5:{query}",

                    download=False,

                )

                if not result:

                    return self._failure(
                        "Playlist not found."
                    )

                entries = result.get(
                    "entries",
                    [],
                )

                if not entries:

                    return self._failure(
                        "Playlist not found."
                    )

                for item in entries:

                    video_id = item.get(
                        "id"
                    )

                    if not video_id:
                        continue

                    url = (
                        "https://www.youtube.com/watch?v="
                        + video_id
                    )

                    return self._browser(

                        url,

                        f'Playing "{query}"',

                    )

                return self._failure(
                    "Playlist not found."
                )

        except Exception as exc:

            logger.exception(

                "Playlist lookup failed: %s",

                exc,

            )

            return self._failure(
                "Unable to play playlist."
            )
    
        # =====================================================
    # Validation
    # =====================================================

    def exists(
        self,
        query: str,
    ) -> bool:

        return (
            self.first_video(
                query,
            )
            is not None
        )

    # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:

        return {

            "engine":
                "yt-dlp",

            "search":
                "ytsearch5",

            "playlist":
                "ytsearch5",

        }

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> None:

        logger.info(
            "Refreshing YouTubePlayer..."
        )

        self.ydl_options = dict(
            self.DEFAULT_OPTIONS
        )

    # =====================================================
    # Cleanup
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "YouTubePlayer shutdown."
        )

    # =====================================================
    # Compatibility
    # =====================================================

    def open(
        self,
        query: str,
    ) -> Response:
        """
        Backward compatibility.
        """

        return self.play(
            query,
        )

    def __repr__(
        self,
    ) -> str:

        return (

            "YouTubePlayer("

            f"engine='yt-dlp', "

            f"search='ytsearch5'"

            ")"

        )