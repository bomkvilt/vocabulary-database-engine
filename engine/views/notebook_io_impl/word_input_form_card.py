import dataclasses
from typing import Optional

from ipywidgets import widgets

from engine.core.protocols import words_databse_protocol

from .element_base import (
    ChangableWidget,
    ElementBase,
    ValueChangeInfo,
    element_property,
)


@dataclasses.dataclass(kw_only=True)
class WordInputCard(ElementBase):
    def __post_init__(self):
        DEFAULT_TEXT_WIDTH = "99%"

        self.__title = self._wrap_element(
            widgets.Label("Word form card:")
        )

        self.__word = ChangableWidget[widgets.Text](
            config=self.config,
            widget=widgets.Text(
                value="",
                placeholder="Start to type a word here",
                description="Word:",
                disabled=False,
                layout={
                    "width": DEFAULT_TEXT_WIDTH,
                },
            ),
        ).add_callback(self.__on_word_chaged)

        self.__form = ChangableWidget[widgets.Text](
            config=self.config,
            widget=widgets.Text(
                value="",
                placeholder="Start to type a word form here",
                description="Form:",
                disabled=False,
                layout={
                    "width": DEFAULT_TEXT_WIDTH,
                },
            ),
        ).add_callback(self.__on_form_chaged)

        self.__description = ChangableWidget[widgets.Text](
            config=self.config,
            widget=widgets.Text(
                value="",
                placeholder="Start to type a word description here",
                description="Description:",
                disabled=False,
                layout={
                    "width": DEFAULT_TEXT_WIDTH,
                },
            )
        )

        self.__submit_word = self._wrap_element(
            widgets.Button(
                button_style="",
                description="submit the word form",
                disabled=False,
                tooltip="",
                icon="check"
            )
        )
        self.__submit_word.on_click(self.__on_word_submit)

        self.__delete_word = self._wrap_element(
            widgets.Button(
                button_style="danger",
                description="delete the word form",
                disabled=False,
                tooltip="",
                icon="check"
            )
        )
        self.__delete_word.on_click(self.__on_word_delete)

        self.__layout = self._wrap_element(
            widgets.VBox([
                self.__title,
                self.__word.get_widget(),
                self.__form.get_widget(),
                self.__description.get_widget(),
                widgets.HBox([
                    self.__submit_word,
                    self.__delete_word,
                ]),
            ])
        )

    def get_widget(self) -> widgets.Widget:
        return self.__layout

    # ------------------| interface

    @element_property
    def word(self) -> str:
        value = self.__word.value
        assert isinstance(value, str)
        return value

    @word.setter
    def _(self, new_value: str, couser: ElementBase) -> None:
        self.__word.set_value(new_value, couser)

    @element_property
    def form(self) -> str:
        value = self.__form.value
        assert isinstance(value, str)
        return value

    @form.setter
    def _(self, new_value: str, couser: ElementBase) -> None:
        self.__form.set_value(new_value, couser)

    @element_property
    def on_word_submit(self) -> words_databse_protocol.WordFormInfo:
        return words_databse_protocol.WordFormInfo(
            description=self.__description.value,
            form=self.__form.value,
            word=self.__word.value,
        )

    @element_property
    def on_word_delete(self) -> words_databse_protocol.WordFormInfo:
        return words_databse_protocol.WordFormInfo(
            description=self.__description.value,
            form=self.__form.value,
            word=self.__word.value,
        )

    # ------------------| callbacks

    def __on_word_chaged(self, info: ValueChangeInfo, couser: Optional[ElementBase]) -> None:
        self.word.broadcast(couser)

    def __on_form_chaged(self, info: ValueChangeInfo, couser: Optional[ElementBase]) -> None:
        self.form.broadcast(couser)

    def __on_word_submit(self, button: widgets.Widget) -> None:
        self.on_word_submit.broadcast(self)

    def __on_word_delete(self, button: widgets.Widget) -> None:
        self.on_word_delete.broadcast(self)
