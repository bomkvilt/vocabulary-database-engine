import dataclasses

from ipywidgets import widgets

from .element_base import ChangableWidget, ElementBase, ValueChangeInfo


@dataclasses.dataclass(kw_only=True)
class WordInputCard(ElementBase):
    def __post_init__(self):
        DEFAULT_TEXT_WIDTH = "99%"

        self.__word_card_title = self._wrap_element(
            widgets.Label("Word form card:")
        )

        self.__word_card_word = ChangableWidget(
            config=self.config,
            widget=widgets.Text(
                value="",
                placeholder="Start to type a word here",
                description="Word:",
                disabled=False,
                layout={
                    "width": DEFAULT_TEXT_WIDTH,
                },
            )
        )
        self.__word_card_word.add_callback(self.__on_word_chaged)

        self.__word_card_form = ChangableWidget(
            config=self.config,
            widget=widgets.Text(
                value="",
                placeholder="Start to type a word form here",
                description="Form:",
                disabled=False,
                layout={
                    "width": DEFAULT_TEXT_WIDTH,
                },
            )
        )
        self.__word_card_form.add_callback(self.__on_form_chaged)

        self.__word_card_description = self._wrap_element(
            widgets.Text(
                value="",
                placeholder="Start to type a word description here",
                description="Description:",
                disabled=False,
                layout={
                    "width": DEFAULT_TEXT_WIDTH,
                },
            )
        )

        self.__word_card_submit_word = self._wrap_element(
            widgets.Button(
                button_style="",
                description="submit the word form",
                disabled=False,
                tooltip="",
                icon="check"
            )
        )
        self.__word_card_delete_word = self._wrap_element(
            widgets.Button(
                button_style="danger",
                description="delete the word form",
                disabled=False,
                tooltip="",
                icon="check"
            )
        )

        self.__word_card_layout = self._wrap_element(
            widgets.VBox([
                self.__word_card_title,
                self.__word_card_word,
                self.__word_card_form,
                self.__word_card_description,
                widgets.HBox([
                    self.__word_card_submit_word,
                    self.__word_card_delete_word,
                ]),
            ])
        )

    def get_widget(self) -> widgets.Widget:
        return self.__word_card_layout

    def __on_word_chaged(self, info: ValueChangeInfo) -> None:
        # TODO: choose a word sudgestion mode
        print(info)

    def __on_form_chaged(self, info: ValueChangeInfo) -> None:
        # TODO: choose a word form sudgestion mode
        print(info)
