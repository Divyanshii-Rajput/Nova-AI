from dataclasses import dataclass

from app.models.intent import Intent


@dataclass(slots=True)
class Command:
    """
    Represents a parsed user command.
    """

    intent: Intent

    entity: str = ""

    original_text: str = ""