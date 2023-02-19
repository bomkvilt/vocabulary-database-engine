import dataclasses
import enum
from typing import Any

from ipywidgets import widgets

from engine.core.protocols.words_databse_protocol import (
    WordDatabaseProtocol,
    WordFormInfo,
)

from .element_base import ElementBase
from .word_input_form_card import WordInputCard
from .word_input_form_suggestion import WordInputSuggestion


class _InputMode(str, enum.Enum):
    WORD = "word"
    FORM = "form"


@dataclasses.dataclass(kw_only=True)
class WordInputFormOptions:
    similar_words_count: int = 20
    similar_forms_count: int = 20


@dataclasses.dataclass(kw_only=True)
class WordInputForm(ElementBase):
    word_input_options: WordInputFormOptions
    database: WordDatabaseProtocol

    def __post_init__(self):
        self.__input_mode = _InputMode.WORD

        self.__form_title = self._wrap_element(
            widgets.Label("Word input and update form")
        )

        self.__word_card = WordInputCard(
            config=self.config,
        )

        self.__suggestions = WordInputSuggestion(
            config=self.config,
        )

        self.__form_layout = widgets.AppLayout(
            right_sidebar=self.__suggestions.get_widget(),
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
        self.__add_mode_detector_action()
        self.__add_similar_words_action()
        self.__add_similar_forms_action()

        self.__update_suggestion_form()

        # move a selected suggested variant to an input form
        self.__add_word_peeker_action()

        # add button actions
        self.__add_word_updation_action()
        self.__add_word_deletion_action()

    def get_widget(self) -> widgets.Widget:
        return self.__form_layout

    def __mode_updater(self, mode: _InputMode):
        def callback(value: str, couser: Any) -> None:
            if self.__input_mode != mode:
                self.__input_mode = mode
                self.__update_suggestion_form()

        return callback

    def __add_word_peeker_action(self) -> None:
        def callback(value: str, couser: Any) -> None:
            match self.__input_mode:
                case _InputMode.WORD:
                    self.__word_card.word.set_value(value, self)
                case _InputMode.FORM:
                    self.__word_card.form.set_value(value, self)
                case _:
                    raise NotImplementedError()

        self.__suggestions.selected.observe(callback)

    def __add_mode_detector_action(self):
        self.__word_card.word.observe(self.__mode_updater(_InputMode.WORD))
        self.__word_card.form.observe(self.__mode_updater(_InputMode.FORM))

    def __add_similar_words_action(self):
        self.__word_card.word.observe(self.__update_words_list)

    def __add_similar_forms_action(self):
        self.__word_card.form.observe(self.__update_forms_list)

    def __update_words_list(self, word: str, couser: Any) -> None:
        limit = self.word_input_options.similar_words_count
        words = self.database.get_similar_words(word, limit)
        self.__suggestions.variants.set_value(list(words), self)

    def __update_forms_list(self, form: str, couser: Any) -> None:
        word = self.__word_card.word.value
        limit = self.word_input_options.similar_words_count
        forms = self.database.get_similar_forms(word, form, limit)
        self.__suggestions.variants.set_value(list(forms), self)

    def __update_suggestion_form(self) -> None:
        match self.__input_mode:
            case _InputMode.WORD:
                self.__suggestions.set_title("list of similar words:")

                word = self.__word_card.word.value
                self.__update_words_list(word, self)
            case _InputMode.FORM:
                word = self.__word_card.word.value
                self.__suggestions.set_title(f"list of known forms for '{word}':")

                form = self.__word_card.form.value
                self.__update_forms_list(form, self)
            case _:
                raise NotImplementedError()

    def __add_word_updation_action(self) -> None:
        def callback(info: WordFormInfo, couser: Any) -> None:
            self.database.update_word_form(info)
            self.__update_suggestion_form()

        self.__word_card.on_word_submit.observe(callback)

    def __add_word_deletion_action(self) -> None:
        def callback(info: WordFormInfo, couser: Any) -> None:
            self.database.delete_word_form(info.word, info.form)
            self.__update_suggestion_form()

        self.__word_card.on_word_delete.observe(callback)
