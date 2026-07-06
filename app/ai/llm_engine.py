## app/ai/llm_engine.py
from __future__ import annotations
import logging
import time
from dataclasses import dataclass
from typing import Any

from google import genai
from google.genai.errors import ClientError

from app.ai.prompt_manager import PromptManager
from app.config.settings import Settings
from app.models.response import Response

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ChatMessage:
    """
    Represents one conversation message.
    """
    role: str
    text: str


class LLMEngine:
    """
    Google Gemini LLM Engine (Nova AI).

    Responsibilities:
    - Build prompts (including system/user messages)
    - Maintain a chat history (up to MAX_HISTORY)
    - Call Gemini API (with retries)
    - Support synchronous and streaming output
    - Return only `Response` objects to callers
    """

    MAX_HISTORY = 20
    MAX_RETRIES = 3
    RETRY_DELAY = 1.5

    def __init__(self) -> None:
        api_key = Settings.GEMINI_API_KEY
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not configured.")
        logger.info("Initializing Gemini client...")
        self.client = genai.Client(api_key=api_key)
        self.model = Settings.GEMINI_MODEL
        self.prompt_manager = PromptManager()
        self.history: list[ChatMessage] = []

    # ---------------------------
    # Helpers
    # ---------------------------

    @staticmethod
    def _success(message: str, data: Any = None) -> Response:
        return Response(success=True, message=message, data=data)

    @staticmethod
    def _failure(message: str) -> Response:
        return Response(success=False, message=message)

    # ---------------------------
    # Conversation History
    # ---------------------------

    def clear(self) -> None:
        self.history.clear()

    def history_size(self) -> int:
        return len(self.history)

    def add_user_message(self, text: str) -> None:
        self.history.append(ChatMessage(role="user", text=text))
        self._trim_history()

    def add_ai_message(self, text: str) -> None:
        self.history.append(ChatMessage(role="model", text=text))
        self._trim_history()

    def _trim_history(self) -> None:
        if len(self.history) > self.MAX_HISTORY:
            self.history = self.history[-self.MAX_HISTORY:]

    # ---------------------------
    # Prompt Construction
    # ---------------------------

    def _history_as_contents(self) -> list[dict[str, Any]]:
        """Convert conversation history to Gemini API content format."""
        contents: list[dict[str, Any]] = []
        for message in self.history:
            contents.append({
                "role": message.role,
                "parts": [{"text": message.text}],
            })
        return contents

    def _build_contents(self, prompt: str) -> list[dict[str, Any]]:
        """
        Build the contents list for a request, including system prompt (if any), 
        chat history, and the user prompt.
        """
        contents: list[dict[str, Any]] = []
        system_prompt = self.prompt_manager.system_prompt()
        if system_prompt:
            # Note: Gemini SDK also supports `system_instruction` in config,
            # but here we include it as a content part for simplicity.
            contents.append({"role": "user", "parts": [{"text": system_prompt}]})
        # Include history
        contents.extend(self._history_as_contents())
        # Add current user query
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        return contents

    # ---------------------------
    # Response Extraction
    # ---------------------------

    def _extract_response(self, response: Any) -> str:
        """
        Extract text from GenerateContentResponse. 
        Preference to `response.text`; if not present, concatenate `response.candidates`.
        """
        if response is None:
            return ""
        text = getattr(response, "text", None)
        if text:
            return text.strip()

        # If no .text, try candidates (for e.g. JSON response candidates)
        candidates = getattr(response, "candidates", None)
        if not candidates:
            return ""
        try:
            content = getattr(candidates[0], "content", None)
            if content:
                parts = getattr(content, "parts", [])
                output_parts = []
                for part in parts:
                    value = getattr(part, "text", None)
                    if value:
                        output_parts.append(value)
                return "\n".join(output_parts).strip()
        except Exception:
            logger.exception("Failed to extract Gemini response.")
        return ""

    # ---------------------------
    # Generation
    # ---------------------------

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        top_p: float = 0.95,
        max_output_tokens: int = 2048,
    ) -> Response:
        """
        Synchronously generate a response for the given prompt using Gemini.
        Retries on transient errors, up to MAX_RETRIES.
        """
        prompt = prompt.strip()
        if not prompt:
            return self._failure("Prompt cannot be empty.")

        contents = self._build_contents(prompt)
        retries = 0
        last_error = "Unknown Gemini error."
        while retries < self.MAX_RETRIES:
            try:
                result = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config={
                        "temperature": temperature,
                        "top_p": top_p,
                        "max_output_tokens": max_output_tokens,
                    }
                )
                text = self._extract_response(result)
                # Update history
                self.add_user_message(prompt)
                if text:
                    self.add_ai_message(text)
                return self._success(text, text)
            except ClientError as exc:
                retries += 1
                last_error = str(exc)
                logger.warning(
                    "Gemini API error (%d/%d): %s",
                    retries, self.MAX_RETRIES, last_error
                )
                time.sleep(self.RETRY_DELAY * retries)
            except Exception as exc:
                logger.exception("Gemini generation failed.")
                return self._failure(str(exc))

        # If we exit loop, return last error
        return self._failure(last_error)

    # ---------------------------
    # Streaming
    # ---------------------------

    def stream(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
    ):
        """
        Generator for streaming generation. Yields text chunks.
        """
        prompt = prompt.strip()
        if not prompt:
            return
        contents = self._build_contents(prompt)
        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config={"temperature": temperature}
            ):
                text = getattr(chunk, "text", None)
                if text:
                    yield text
        except Exception:
            logger.exception("Gemini streaming failed.")
            raise

    # ---------------------------
    # Public Helpers
    # ---------------------------

    def ask(self, prompt: str) -> str:
        """Simple ask: return text or raise on error."""
        response = self.generate(prompt)
        if response.success:
            return response.message
        raise RuntimeError(response.message)

    def chat(self, prompt: str) -> Response:
        """Used by ActionEngine to get an AI chat response."""
        return self.generate(prompt)

    # ---------------------------
    # Utilities
    # ---------------------------

    def stats(self) -> dict:
        return {
            "model": self.model,
            "history": len(self.history),
            "max_history": self.MAX_HISTORY,
            "max_retries": self.MAX_RETRIES,
        }

    def __len__(self) -> int:
        return len(self.history)

    def __repr__(self) -> str:
        return f"LLMEngine(model={self.model}, history={len(self.history)})"
