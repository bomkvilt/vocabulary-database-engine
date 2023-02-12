import abc
import enum
from typing import Callable

from engine.core.protocols.new_word_protocol import (
    WordFormInputMessage,
    WordInputMessage,
)


class WordInputView(abc.ABC):
    class InputStage(enum.Enum):
        WORD_INPUT = "word_input"
        FORM_INPUT = "form_input"

    def __init__(self) -> None:
        self._stage = self.InputStage.WORD_INPUT

    @abc.abstractmethod
    def set_sudgestions(self, variants: list[str]) -> None:
        """ Set sudgestions list.
        """

    @abc.abstractmethod
    def set_word_text(self, text: WordInputMessage) -> None:
        """ Set specified word text to an input widget.
        """

    @abc.abstractmethod
    def set_on_word_enterd(self, clb: Callable[[WordInputMessage], None]) -> None:
        """ Set callback that will be called when a word will be inputted.

        NOTE: the method will override a previous callback.
        """

    @abc.abstractmethod
    def set_word_form(self, text: WordFormInputMessage) -> None:
        """ Set specified word form description.
        """
