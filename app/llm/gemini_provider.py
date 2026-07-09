from __future__ import annotations
import logging
from google import genai
from app.config.settings import Settings
from app.llm.base_provider import BaseProvider

logger = logging.getLogger(__name__)

class GeminiProvider(BaseProvider):
    def __init__(self):
        self.api_key = Settings.GEMINI_API_KEY
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        self.model = Settings.GEMINI_MODEL

    def generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None = None,
        system_instruction: str = '',
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self.client:
            raise RuntimeError('Gemini API key unconfigured.')

        # Convert simple history list into Gemini SDK format
        contents = []
        if history:
            for msg in history:
                role = msg.get('role', 'user')
                if role == 'assistant':
                    role = 'model'
                contents.append({
                    'role': role,
                    'parts': [{'text': msg.get('content', '')}]
                })
        
        contents.append({
            'role': 'user',
            'parts': [{'text': prompt}]
        })

        models_to_try = [self.model]
        for fallback in ['gemini-1.5-flash', 'gemini-1.5-pro']:
            if fallback not in models_to_try:
                models_to_try.append(fallback)

        errors = []
        for model_name in models_to_try:
            try:
                logger.info('GeminiProvider attempting model: %s', model_name)
                result = self.client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config={
                        'temperature': temperature,
                        'max_output_tokens': max_tokens,
                        'system_instruction': system_instruction,
                    }
                )
                text = getattr(result, 'text', None)
                if text:
                    return text.strip()
                
                # Fallback extraction from candidates
                candidates = getattr(result, 'candidates', None)
                if candidates:
                    content = getattr(candidates[0], 'content', None)
                    if content:
                        parts = getattr(content, 'parts', [])
                        text_parts = [getattr(p, 'text', '') for p in parts if getattr(p, 'text', None)]
                        if text_parts:
                            return '\n'.join(text_parts).strip()
                            
                errors.append(f'{model_name}: Empty response')
            except Exception as e:
                errors.append(f'{model_name}: {str(e)}')
                logger.warning('Gemini model %s failed: %s', model_name, e)

        raise RuntimeError(f'Gemini API failure: {'; '.join(errors)}')
