import dataclasses
import enum
from typing import Optional

from engine.core import system

__all__ = [
    "WordInputMessage",
    "WordFormInputMessage",
]


class Events(str, enum.Enum):
    # new form was created
    NEW_FORM = "new_form"



@dataclasses.dataclass(kw_only=True)
class WordInputMessage(system.BusMessage):
    word: str


@dataclasses.dataclass(kw_only=True)
class WordFormInputMessage(system.BusMessage):
    description: Optional[str] = None
    word_form: str
