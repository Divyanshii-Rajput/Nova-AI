from app.models.command import Command

from app.nlp.intent_detector import IntentDetector
from app.nlp.entity_extractor import EntityExtractor


class CommandParser:
    """
    Creates a Command object from normalized text.
    """

    def __init__(self):

        self.intent_detector = IntentDetector()

        self.entity_extractor = EntityExtractor()

    def parse(self, text: str) -> Command:

        intent = self.intent_detector.detect(text)

        entity = self.entity_extractor.extract(text)

        return Command(
            intent=intent,
            entity=entity,
            original_text=text,
        )