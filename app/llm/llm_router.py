from __future__ import annotations
import logging
import time
from app.config.settings import Settings
from app.models.response import Response
from app.llm.gemini_provider import GeminiProvider
from app.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self):
        self.gemini = GeminiProvider()
        self.groq = GroqProvider()
        self.history: list[dict[str, str]] = []
        self._cache: dict[str, str] = {}
        
        from app.ai.prompt_manager import PromptManager
        self.prompt_manager = PromptManager()

    def clear(self) -> None:
        self.history.clear()

    def chat(self, prompt: str) -> Response:
        return self.generate(prompt)

    def generate(self, prompt: str) -> Response:
        prompt = prompt.strip()
        if not prompt:
            return Response(success=False, message='Prompt cannot be empty.')

        # Check in-memory cache
        cache_key = prompt.lower().strip()
        if cache_key in self._cache:
            logger.info('Returning cached response for query: \'%s\'', prompt)
            self.history.append({'role': 'user', 'content': prompt})
            self.history.append({'role': 'assistant', 'content': self._cache[cache_key]})
            return Response(success=True, message=self._cache[cache_key])

        system_instruction = self.prompt_manager.system_prompt()
        errors = []
        providers = ['gemini', 'groq']

        for provider in providers:
            try:
                logger.info('Using %s', provider.capitalize())
                start_time = time.time()
                
                if provider == 'gemini':
                    text = self.gemini.generate(
                        prompt=prompt,
                        history=self.history,
                        system_instruction=system_instruction
                    )
                elif provider == 'groq':
                    text = self.groq.generate(
                        prompt=prompt,
                        history=self.history,
                        system_instruction=system_instruction
                    )
                else:
                    continue

                duration = time.time() - start_time
                logger.info('%s response generated in %.2f seconds', provider.capitalize(), duration)

                self.history.append({'role': 'user', 'content': prompt})
                self.history.append({'role': 'assistant', 'content': text})
                self._cache[cache_key] = text
                return Response(success=True, message=text)

            except Exception as e:
                logger.warning('%s failed: %s', provider.capitalize(), e)
                errors.append(f'{provider}: {str(e)}')
                if provider == 'gemini':
                    logger.info('Switching to Groq')

        logger.error('All LLM providers failed: %s', errors)
        fallback_msg = 'I am currently experiencing technical difficulties connecting to my brain. Please check your internet connection or try again in a moment.'
        return Response(success=False, message=fallback_msg)
