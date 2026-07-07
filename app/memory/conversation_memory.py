from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Conversation:

    title: str

    user: str

    assistant: str

    timestamp: datetime


class ConversationMemory:
    """
    Stores conversation history for the desktop UI.
    """

    def __init__(self):

        self._history: list[Conversation] = []

    def add(
        self,
        user: str,
        assistant: str,
    ) -> None:

        self._history.append(

            Conversation(

                title=user[:40],

                user=user,

                assistant=assistant,

                timestamp=datetime.now(),

            )

        )

    def all(
        self,
    ) -> list[Conversation]:

        return list(reversed(self._history))

    def clear(
        self,
    ) -> None:

        self._history.clear()

    def search(
        self,
        query: str,
    ) -> list[Conversation]:

        query = query.lower()

        return [

            item

            for item in self._history

            if query in item.user.lower()

            or query in item.assistant.lower()

        ]

conversation_memory = ConversationMemory()