from dataclasses import dataclass

from app.models.intent import Intent


@dataclass(slots=True)
class Command:
    """
    Represents a parsed user command.
    """

    # Original spoken sentence
    original_text: str

    # After cleaning / alias replacement
    cleaned_text: str

    # Detected intent
    intent: Intent

    # Extracted entity
    entity: str = ""

    # Confidence (future NLP improvements)
    confidence: float = 1.0