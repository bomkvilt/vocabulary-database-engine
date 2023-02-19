import IPython.display
import pydantic

from engine.core.protocols import words_databse_protocol

from . import notebook_io_impl
from .notebook_io_impl import ElementConfig, WordInputFormOptions

__all__ = [
    "ElementConfig",
    "NotebookIO",
    "WordInputFormOptions",
]


@pydantic.dataclasses.dataclass(kw_only=True)
class NotebookIO:
    view_config: ElementConfig

    def open_word_input_form(
        self, *,
        database: words_databse_protocol.WordDatabaseProtocol,
        options: WordInputFormOptions,
    ) -> None:
        form = notebook_io_impl.WordInputForm(
            word_input_options=options,
            database=database,
            config=self.view_config,
        )

        IPython.display.display(form.get_widget())
