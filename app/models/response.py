from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Response:
    """
    Standard response object returned by all modules.
    """

    success: bool

    message: str = ""

    data: Any = None