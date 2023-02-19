import dataclasses
from typing import Iterable, Optional

from ipywidgets import widgets

from .element_base import (
    ChangableWidget,
    ElementBase,
    ValueChangeInfo,
    element_property,
)

_EMPTY_VALUE = ""


@dataclasses.dataclass(kw_only=True)
class WordInputSuggestion(ElementBase):
    def __post_init__(self):
        DEFAULT_TEXT_WIDTH = "99%"

        self.__sudgestions_title = self._wrap_element(
            widgets.Label("")
        )

        self.__sudgestions_list = ChangableWidget[widgets.Select](
            config=self.config,
            widget=widgets.Select(
                options=[],
                layout={
                    "height": "99%",
                    "width": DEFAULT_TEXT_WIDTH,
                },
            )
        ).add_callback(self.__on_value_selected)

        self.__sudgestions_layout = self._wrap_element(
            widgets.VBox([
                self.__sudgestions_title,
                self.__sudgestions_list.get_widget(),
            ])
        )

    def get_widget(self) -> widgets.Widget:
        return self.__sudgestions_layout

    def set_title(self, value: str) -> None:
        self.__sudgestions_title.value = value

    # ------------------| properties

    @element_property
    def selected(self) -> str:
        value = self.__sudgestions_list.value
        assert isinstance(value, str)
        return value

    @selected.setter
    def _(self, new_value: str, couser: ElementBase) -> None:
        self.__sudgestions_list.set_value(new_value, couser)

    @element_property
    def variants(self) -> list[str]:
        options = self.__sudgestions_list.widget.options
        assert isinstance(options, Iterable)
        return list(options)  # type: ignore

    @variants.setter
    def _(self, new_value: list[str], couser: ElementBase) -> None:
        self.__sudgestions_list.widget.options = [_EMPTY_VALUE] + new_value

    # ------------------| callbacks

    def __on_value_selected(self, info: ValueChangeInfo, couser: Optional[ElementBase]) -> None:
        if info.new_value != _EMPTY_VALUE:
            self.selected.broadcast(couser)
