import dataclasses
import enum
from typing import Any

from ipywidgets import widgets

from .element_base import ElementBase
from .word_input_form_card import WordInputCard
from .word_input_form_sudgestion import WordInputSudgestion


class InputMode(str, enum.Enum):
    WORD = "word"
    FORM = "form"


@dataclasses.dataclass(kw_only=True)
class WordInputForm(ElementBase):
    def __post_init__(self):
        self.__input_mode = InputMode.WORD

        self.__form_title = self._wrap_element(
            widgets.Label("Word input and update form")
        )

        self.__word_card = WordInputCard(
            config=self.config,
        )

        self.__sudgestions = WordInputSudgestion(
            config=self.config,
        )

        self.__form_layout = widgets.AppLayout(
            right_sidebar=self.__sudgestions.get_widget(),
            left_sidebar=None,
            center=self.__word_card.get_widget(),
            header=self.__form_title,

            pane_heights=["30px", 4, 1],
            pane_widths=["80px", 2, 1],
            grid_gap="30px",
            height="100%",
            width="100%",
        )

        # add input mode detectors
        self.__word_card.word.observe(self.__mode_peeker(InputMode.WORD))
        self.__word_card.form.observe(self.__mode_peeker(InputMode.FORM))
        self.__update_sudestion_from()

        # move selected variant to an active input row
        self.__add_word_peeker()

        # TODO: drop "tmp__" logging
        def tmp__logger(value: Any, couser: Any) -> None:
            print((value, couser))

        self.__word_card.word.observe(tmp__logger)
        self.__word_card.form.observe(tmp__logger)
        self.__sudgestions.selected.observe(tmp__logger)
        self.__sudgestions.variants.observe(tmp__logger)

        # TODO: drop "tmp__" database emulation
        def tmp__word_to_variants(value: str, couser: Any) -> None:
            if couser == self:
                return

            new_variants = [
                value,
                value + " 1",
                value + " 2",
            ]
            self.__sudgestions.variants.set_value(new_variants, self)

        self.__word_card.word.observe(tmp__word_to_variants)
        self.__word_card.form.observe(tmp__word_to_variants)

    def get_widget(self) -> widgets.Widget:
        return self.__form_layout

    def __mode_peeker(self, mode: InputMode):
        def callback(value: str, couser: Any) -> None:
            if self.__input_mode != mode:
                self.__input_mode = mode
                self.__update_sudestion_from()

        return callback

    def __add_word_peeker(self) -> None:
        def callback(value: str, couser: Any) -> None:
            match self.__input_mode:
                case InputMode.WORD:
                    self.__word_card.word.set_value(value, self)
                case InputMode.FORM:
                    self.__word_card.form.set_value(value, self)
                case _:
                    raise NotImplementedError()

        self.__sudgestions.selected.observe(callback)

    def __update_sudestion_from(self) -> None:
        match self.__input_mode:
            case InputMode.WORD:
                self.__sudgestions.set_title("list of simular words:")
            case InputMode.FORM:
                word: str = self.__word_card.word.value
                self.__sudgestions.set_title(f"list of known forms for '{word}':")
            case _:
                raise NotImplementedError()
