import abc
import dataclasses
import pathlib
from typing import Type

Language = Type("Language")


@dataclasses.dataclass(kw_only=True, frozen=True)
class WordDescription:
    description: str
    language: Language
    word: str
    form: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class DatabaseOptions:
    path: pathlib.Path


class DatabaseBase(abc.ABC):
    """ Databse interface
    """
    options: DatabaseOptions

    @abc.abstractmethod
    def add_word(self):
        pass
