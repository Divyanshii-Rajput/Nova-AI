from __future__ import annotations

class BaseProvider:
    def generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None = None,
        system_instruction: str = '',
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        raise NotImplementedError('Providers must implement the generate method.')
