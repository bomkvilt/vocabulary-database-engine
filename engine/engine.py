import pathlib

from engine.core import databases
from engine.core.databases import storages
from engine.core.protocols.words_databse_protocol import WordDatabaseProtocol
from engine.views import notebook_io


class Engine:
    def open_csv_database(self, path: pathlib.Path) -> WordDatabaseProtocol:
        storage = storages.CSVStorage(
            options=storages.CSVStorageOptions(
                path=path,
            ),
        )

        words_database = databases.WordsDatabase(
            storage=storage,
            options=databases.WordsDatabaseOptions(),
        )

        return words_database

    def open_words_input(self, words_database: WordDatabaseProtocol) -> None:
        controller = notebook_io.NotebookIO(
            view_config=notebook_io.ElementConfig(
                show_debug_frames=False,
            ),
        )

        controller.open_word_input_form(
            database=words_database,
            options=notebook_io.WordInputFormOptions(),
        )
