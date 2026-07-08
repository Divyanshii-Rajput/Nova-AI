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
        self.prompt_manager = PromptManager()
        self.history: list[ChatMessage] = []
        self._cache: dict[str, str] = {}

        api_key = Settings.GEMINI_API_KEY
        if not api_key:
            logger.warning("GEMINI_API_KEY not configured. Gemini provider will be unavailable.")
            self.client = None
        else:
            logger.info("Initializing Gemini client...")
            self.client = genai.Client(api_key=api_key)
        self.model = Settings.GEMINI_MODEL

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
        Build the contents list for a request, including 
        chat history and the user prompt.
        """
        contents: list[dict[str, Any]] = []
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

    def _generate_gemini(
        self,
        prompt: str,
        temperature: float,
        top_p: float,
        max_output_tokens: int,
    ) -> Response:
        if not self.client:
            return self._failure("Gemini API key unconfigured.")
        contents = self._build_contents(prompt)

        # Try multiple Gemini models in case of free tier daily quota exhaustion (429)
        models_to_try = [self.model]
        for fallback in ["gemini-1.5-flash", "gemini-1.5-pro"]:
            if fallback not in models_to_try:
                models_to_try.append(fallback)

        errors = []
        for model_name in models_to_try:
            try:
                logger.info("Attempting Gemini model: %s", model_name)
                result = self.client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config={
                        "temperature": temperature,
                        "top_p": top_p,
                        "max_output_tokens": max_output_tokens,
                        "system_instruction": self.prompt_manager.system_prompt(),
                    }
                )
                text = self._extract_response(result)
                if not text:
                    errors.append(f"{model_name}: Empty response")
                    continue
                self.add_user_message(prompt)
                self.add_ai_message(text)
                return self._success(text, text)
            except Exception as exc:
                errors.append(f"{model_name}: {str(exc)}")
                logger.warning("Gemini model %s failed: %s", model_name, exc)

        return self._failure(f"Gemini API failure: {'; '.join(errors)}")

    def _generate_groq(
        self,
        prompt: str,
        temperature: float,
        max_output_tokens: int,
    ) -> Response:
        api_key = Settings.GROQ_API_KEY
        if not api_key:
            return self._failure("Groq API key unconfigured.")
        
        import requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        messages = [{"role": "system", "content": self.prompt_manager.system_prompt()}]
        for msg in self.history:
            role = "assistant" if msg.role == "model" else msg.role
            messages.append({"role": role, "content": msg.text})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": Settings.GROQ_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_output_tokens
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=8.0
            )
            if response.status_code != 200:
                return self._failure(f"Groq status {response.status_code}")
            
            res_json = response.json()
            text = res_json["choices"][0]["message"]["content"].strip()
            if not text:
                return self._failure("Groq returned empty response.")
            
            self.add_user_message(prompt)
            self.add_ai_message(text)
            return self._success(text, text)
        except Exception as exc:
            return self._failure(str(exc))

    def _generate_ollama(
        self,
        prompt: str,
        temperature: float,
    ) -> Response:
        import requests
        
        messages = [{"role": "system", "content": self.prompt_manager.system_prompt()}]
        for msg in self.history:
            role = "assistant" if msg.role == "model" else msg.role
            messages.append({"role": role, "content": msg.text})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": Settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        try:
            response = requests.post(
                f"{Settings.OLLAMA_HOST}/v1/chat/completions",
                json=data,
                timeout=8.0
            )
            if response.status_code != 200:
                return self._failure(f"Ollama status {response.status_code}")
            
            res_json = response.json()
            text = res_json["choices"][0]["message"]["content"].strip()
            if not text:
                return self._failure("Ollama returned empty response.")
            
            self.add_user_message(prompt)
            self.add_ai_message(text)
            return self._success(text, text)
        except Exception as exc:
            return self._failure(str(exc))

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        top_p: float = 0.95,
        max_output_tokens: int = 2048,
    ) -> Response:
        """
        Synchronously generate a response for the given prompt using the LLM Router.
        Falls back through Gemini, Groq, and Ollama sequentially.
        """
        prompt = prompt.strip()
        if not prompt:
            return self._failure("Prompt cannot be empty.")

        # Check in-memory response cache first
        cache_key = prompt.lower().strip()
        if cache_key in self._cache:
            cached_text = self._cache[cache_key]
            logger.info("Returning cached response for query: '%s'", prompt)
            self.add_user_message(prompt)
            self.add_ai_message(cached_text)
            return self._success(cached_text, cached_text)

        errors = []
        for provider in Settings.LLM_PROVIDERS:
            try:
                logger.info("LLM Router attempting provider: %s", provider)
                if provider == "gemini":
                    res = self._generate_gemini(prompt, temperature, top_p, max_output_tokens)
                elif provider == "groq":
                    res = self._generate_groq(prompt, temperature, max_output_tokens)
                elif provider == "ollama":
                    res = self._generate_ollama(prompt, temperature)
                else:
                    continue

                if res.success:
                    logger.info("LLM Router success with provider: %s", provider)
                    # Store in response cache
                    self._cache[cache_key] = res.message
                    return res
                else:
                    errors.append(f"{provider}: {res.message}")
            except Exception as e:
                logger.exception("LLM Router provider %s raised exception", provider)
                errors.append(f"{provider}: {str(e)}")

        # If all providers fail, return a clean friendly message instead of stack trace or technical error
        logger.error("All LLM providers failed: %s", errors)
        return self._failure("I am currently experiencing technical difficulties connecting to my brain. Please check your internet connection or try again in a moment.")

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
                config={
                    "temperature": temperature,
                    "system_instruction": self.prompt_manager.system_prompt(),
                }
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
