from __future__ import annotations
import logging
import requests
from app.config.settings import Settings
from app.llm.base_provider import BaseProvider

logger = logging.getLogger(__name__)

class GroqProvider(BaseProvider):
    def __init__(self):
        self.api_key = Settings.GROQ_API_KEY
        self.model = Settings.GROQ_MODEL

    def generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None = None,
        system_instruction: str = '',
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        Settings.load()
        api_key = Settings.GROQ_API_KEY or self.api_key
        if not api_key:
            raise RuntimeError('Groq API key unconfigured.')

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        messages = []
        if system_instruction:
            messages.append({'role': 'system', 'content': system_instruction})
        
        if history:
            for msg in history:
                messages.append({
                    'role': msg.get('role', 'user'),
                    'content': msg.get('content', '')
                })

        messages.append({'role': 'user', 'content': prompt})

        data = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }

        try:
            logger.info('GroqProvider sending request to API...')
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10.0
            )
            if response.status_code != 200:
                raise RuntimeError(f'Groq API returned status {response.status_code}: {response.text}')
            
            res_json = response.json()
            text = res_json['choices'][0]['message']['content'].strip()
            if not text:
                raise RuntimeError('Groq returned empty response.')
            return text
        except Exception as e:
            logger.error('GroqProvider failed: %s', e)
            raise RuntimeError(f'Groq failure: {str(e)}')
