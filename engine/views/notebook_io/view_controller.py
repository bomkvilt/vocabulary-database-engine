from engine.core.protocols.new_word_protocol import (
    WordFormInputMessage,
    WordInputMessage,
)
from engine.views.view_controller import WordInputView


class NotebookWordInputView(WordInputView):
    def set_sudgestions(self, variants: list[str]) -> None:
        pass

    def set_word_text(self, text: WordInputMessage) -> None:
        pass

    def set_word_form(self, text: WordFormInputMessage) -> None:
        pass
