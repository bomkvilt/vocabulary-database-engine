from dataclasses import InitVar
from typing import Any, Callable, Iterable

import Levenshtein
import numpy as np
import pandas as pd
import pydantic

from engine.core.protocols.words_databse_protocol import (
    WordDatabaseProtocol,
    WordFormInfo,
)

from .storage_base import StorageBase


@pydantic.dataclasses.dataclass(kw_only=True, frozen=True)
class WordsDatabaseOptions:
    pass


@pydantic.dataclasses.dataclass(kw_only=True)
class WordsDatabase(WordDatabaseProtocol):
    class Fields:
        DESCRIPTION = "__desc__"
        FORM = "__form__"
        WORD = "__word__"

    storage: StorageBase

    options: InitVar[WordsDatabaseOptions]

    def __post_init__(self, options: WordsDatabaseOptions) -> None:
        self.__words = self.__load_words_dump().copy()  # avaid errors
        self.__options = options

    def get_similar_words(self, base: str, count: int) -> Iterable[str]:
        return self.__get_similar_variants_by_index(self.__words.index, base, count)

    def get_similar_forms(self, word: str, base: str, count: int) -> Iterable[str]:
        if word not in self.__words.index:
            return []

        slice = self.__words.loc[word]
        return self.__get_similar_variants_by_index(slice.index, base, count)

    def update_word_form(self, info: WordFormInfo) -> None:
        key = (info.word, info.form)
        row = pd.Series({
            self.Fields.FORM: info.form,
            self.Fields.WORD: info.word,
            self.Fields.DESCRIPTION: info.description,
        })

        if key in self.__words.index:
            self.__words.loc[key, :] = row
            print("word updated")  # TODO: use logger
        else:
            patch = pd.DataFrame([row])
            self.__add_index(patch)
            self.__words = pd.concat([self.__words, patch])
            print("word created")  # TODO: use logger

        self.storage.save_dump(self.__words)

    def delete_word_form(self, word: str, form: str) -> None:
        key = (word, form)

        if key in self.__words.index:
            self.__words.drop(index=key, inplace=True)

            self.storage.save_dump(self.__words)
            print("word deleted from database")  # TODO: use logger

    def __load_words_dump(self) -> pd.DataFrame:
        dump = self.storage.read_dump()
        if dump is None:
            dump = pd.DataFrame(columns=[
                self.Fields.WORD,
                self.Fields.FORM,
                self.Fields.DESCRIPTION,
            ])

        self.__add_index(dump)
        return dump

    def __add_index(self, df: pd.DataFrame) -> None:
        df.set_index(
            [self.Fields.WORD, self.Fields.FORM],
            verify_integrity=True,
            inplace=True,
            drop=False,
        )

    def __get_similar_variants_by_index(self, index: pd.Index, base: str, count: int) -> Iterable[str]:
        assert count > 0
        variants = index.get_level_values(0).to_series().drop_duplicates()
        distances: pd.Series = variants.apply(self.__make_distance_function(base))  # type: ignore
        distances = distances.astype(np.int32, copy=False)

        top = distances.nsmallest(count)
        return variants.loc[top.index]

    def __make_distance_function(self, base: str) -> Callable[[Any], np.int32]:
        FINES = (
            1,  # insert
            5,  # delete
            2,  # replace
        )

        def scorrer(word: Any) -> np.int32:
            assert isinstance(word, str)
            dist = Levenshtein.distance(base, word, weights=FINES)
            return np.int32(dist)

        return scorrer
