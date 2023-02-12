import dataclasses
from typing import Any

from ipywidgets import widgets

from .element_base import ElementBase
from .word_input_form_card import WordInputCard
from .word_input_form_sudgestion import WordInputSudgestion


@dataclasses.dataclass(kw_only=True)
class WordInputForm(ElementBase):
    def __post_init__(self):
        self.__form_title = self._wrap_element(
            widgets.Label("Word input and update form")
        )

        self.__sudgestions_layout = WordInputSudgestion(
            config=self.config,
        )

        def tmp(value: str, couser: Any) -> None:
            print((value, couser))

        self.__word_card_layout = WordInputCard(
            config=self.config,
        )
        self.__word_card_layout.word.observe(tmp)
        self.__word_card_layout.form.observe(tmp)

        def tmp_mirror(value: str, couser: Any) -> None:
            self.__word_card_layout.form.set_value(value, self)

        self.__word_card_layout.word.observe(tmp_mirror)

        self.__form_layout = widgets.AppLayout(
            right_sidebar=self.__sudgestions_layout.get_widget(),
            left_sidebar=None,
            center=self.__word_card_layout.get_widget(),
            header=self.__form_title,

            pane_heights=["30px", 4, 1],
            pane_widths=["80px", 2, 1],
            grid_gap="30px",
            height="100%",
            width="100%",
        )

    def get_widget(self) -> widgets.Widget:
        return self.__form_layout
