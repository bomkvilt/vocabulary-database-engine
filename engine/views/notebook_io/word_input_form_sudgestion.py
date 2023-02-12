import dataclasses

from ipywidgets import widgets

from .element_base import ElementBase


@dataclasses.dataclass(kw_only=True)
class WordInputSudgestion(ElementBase):
    def __post_init__(self):
        DEFAULT_TEXT_WIDTH = "99%"

        self.__sudgestions_title = self._wrap_element(
            widgets.Label("List of already known words:")
        )
        self.__sudgestions_list = self._wrap_element(
            widgets.Select(
                options=[],
                layout={
                    "height": "99%",
                    "width": DEFAULT_TEXT_WIDTH,
                },
            )
        )
        self.__sudgestions_layout = self._wrap_element(
            widgets.VBox([
                self.__sudgestions_title,
                self.__sudgestions_list,
            ])
        )

    def get_widget(self) -> widgets.Widget:
        return self.__sudgestions_layout
