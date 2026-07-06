from __future__ import annotations

import logging
import webbrowser
from urllib.parse import quote_plus
from typing import Any

from app.models.response import Response

logger = logging.getLogger(__name__)


class BrowserManager:
    """
    High-level browser manager.

    Responsibilities
    ----------------
    • Open known websites
    • Open arbitrary URLs
    • Perform Google searches
    • Return Response objects

    Business logic belongs here.
    Browser implementation is delegated
    to Python's default browser.
    """

    KNOWN_WEBSITES = {

        # -----------------------------
        # AI
        # -----------------------------

        "chatgpt": "https://chat.openai.com",
        "claude": "https://claude.ai",
        "gemini": "https://gemini.google.com",

        # -----------------------------
        # Coding
        # -----------------------------

        "leetcode": "https://leetcode.com",
        "geeksforgeeks": "https://www.geeksforgeeks.org",
        "github": "https://github.com",
        "codeforces": "https://codeforces.com",
        "codechef": "https://www.codechef.com",
        "hackerrank": "https://www.hackerrank.com",

        # -----------------------------
        # Google
        # -----------------------------

        "gmail": "https://mail.google.com",
        "drive": "https://drive.google.com",
        "docs": "https://docs.google.com",
        "maps": "https://maps.google.com",

        # -----------------------------
        # Entertainment
        # -----------------------------

        "youtube": "https://youtube.com",
        "spotify": "https://spotify.com",
        "netflix": "https://netflix.com",

        # -----------------------------
        # Social
        # -----------------------------

        "linkedin": "https://linkedin.com",
        "twitter": "https://x.com",
        "instagram": "https://instagram.com",
        "facebook": "https://facebook.com",

        # -----------------------------
        # Shopping
        # -----------------------------

        "amazon": "https://amazon.in",
        "flipkart": "https://flipkart.com",

    }

    GOOGLE = "https://www.google.com/search?q={}"

    def __init__(self) -> None:

        logger.info(
            "Initializing BrowserManager..."
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

    def _open_url(
        self,
        url: str,
        display_name: str,
    ) -> Response:

        try:

            webbrowser.open(url)

            logger.info(
                "Opened URL: %s",
                url,
            )

            return self._success(
                f"Opened {display_name}.",
                url,
            )

        except Exception:

            logger.exception(
                "Failed to open browser URL."
            )

            return self._failure(
                "Unable to open browser."
            )

    # =====================================================
    # Website
    # =====================================================

    def open_website(
        self,
        website: str,
    ) -> Response:

        if website is None:

            return self._failure(
                "No website specified."
            )

        website = website.strip().lower()

        if not website:

            return self._failure(
                "No website specified."
            )

        logger.info(
            "Opening website: %s",
            website,
        )

        # ---------------------------------
        # Known website
        # ---------------------------------

        if website in self.KNOWN_WEBSITES:

            return self._open_url(
                self.KNOWN_WEBSITES[website],
                website,
            )

        # ---------------------------------
        # Already URL
        # ---------------------------------

        if website.startswith(
            (
                "http://",
                "https://",
            )
        ):

            return self._open_url(
                website,
                website,
            )

        # ---------------------------------
        # Looks like domain
        # ---------------------------------

        if "." in website and " " not in website:

            return self._open_url(
                f"https://{website}",
                website,
            )

        logger.warning(
            "Unknown website: %s",
            website,
        )

        return self._failure(
            f"Website '{website}' not found."
        )

    # =====================================================
    # Google Search
    # =====================================================

    def search_google(
        self,
        query: str,
    ) -> Response:

        if query is None:

            return self._failure(
                "Empty search query."
            )

        query = query.strip()

        if not query:

            return self._failure(
                "Empty search query."
            )

        logger.info(
            "Google search: %s",
            query,
        )

        url = self.GOOGLE.format(
            quote_plus(query)
        )

        return self._open_url(
            url,
            f"Google search for '{query}'",
        )
    
        # =====================================================
    # Register Website
    # =====================================================

    def register(
        self,
        name: str,
        url: str,
    ) -> None:
        """
        Register a website at runtime.
        """

        if not name or not url:
            return

        name = name.strip().lower()
        url = url.strip()

        self.KNOWN_WEBSITES[name] = url

        logger.info(
            "Registered website '%s' -> %s",
            name,
            url,
        )

    # =====================================================
    # Remove Website
    # =====================================================

    def unregister(
        self,
        name: str,
    ) -> bool:
        """
        Remove a registered website.
        """

        if not name:
            return False

        name = name.strip().lower()

        if name not in self.KNOWN_WEBSITES:
            return False

        del self.KNOWN_WEBSITES[name]

        logger.info(
            "Removed website: %s",
            name,
        )

        return True

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        website: str,
    ) -> bool:

        if not website:
            return False

        return (
            website.strip().lower()
            in self.KNOWN_WEBSITES
        )

    # =====================================================
    # Resolve
    # =====================================================

    def resolve(
        self,
        website: str,
    ) -> str | None:
        """
        Return the URL of a known website.
        """

        if not website:
            return None

        return self.KNOWN_WEBSITES.get(
            website.strip().lower()
        )

    # =====================================================
    # Website List
    # =====================================================

    def websites(
        self,
    ) -> list[str]:

        return sorted(
            self.KNOWN_WEBSITES.keys()
        )

    # =====================================================
    # Statistics
    # =====================================================

    def stats(
        self,
    ) -> dict:

        return {

            "known_sites":
                len(self.KNOWN_WEBSITES),

            "google_search":
                self.GOOGLE,

        }

    # =====================================================
    # Refresh
    # =====================================================

    def refresh(
        self,
    ) -> Response:

        logger.info(
            "Refreshing BrowserManager..."
        )

        return self._success(
            "Browser manager refreshed."
        )

    # =====================================================
    # Cleanup
    # =====================================================

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "BrowserManager shutdown."
        )