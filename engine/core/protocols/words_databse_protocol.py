import abc
import dataclasses
from typing import Iterable

import pydantic

# , Optional

__all__ = [
    "WordDatabaseProtocol",
    "WordFormInfo",
]


@dataclasses.dataclass(kw_only=True, frozen=True)
class WordFormInfo:
    description: str
    form: str
    word: str


@pydantic.dataclasses.dataclass(kw_only=True)
class WordDatabaseProtocol(abc.ABC):
    @abc.abstractmethod
    def get_similar_words(self, base: str, count: int) -> Iterable[str]:
        return []

    @abc.abstractmethod
    def get_similar_forms(self, word: str, base: str, count: int) -> Iterable[str]:
        return []

    # @abc.abstractmethod
    # def get_word_form_info(self, word: str, form: str) -> Optional[WordFormInfo]:
    #     return WordFormInfo()

    @abc.abstractmethod
    def update_word_form(self, info: WordFormInfo) -> None:
        pass

    @abc.abstractmethod
    def delete_word_form(self, word: str, form: str) -> None:
        pass
