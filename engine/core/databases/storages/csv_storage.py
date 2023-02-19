import pathlib
from dataclasses import InitVar

import pandas as pd
import pydantic

from .common import StorageBase


@pydantic.dataclasses.dataclass(kw_only=True)
class CSVStorageOptions:
    path: pathlib.Path


@pydantic.dataclasses.dataclass(kw_only=True)
class CSVStorage(StorageBase):
    options: InitVar[CSVStorageOptions]

    def __post_init__(self, options: CSVStorageOptions) -> None:
        self.__encoding = "utf-8"
        self.__options = options
        self.__sep = "\t"

    def read_dump(self) -> pd.DataFrame | None:
        if not self.__options.path.exists():
            return None

        with self.__options.path.open("r", encoding=self.__encoding) as file:
            return pd.read_csv(file, sep=self.__sep)

    def save_dump(self, dump: pd.DataFrame) -> None:
        dump.to_csv(self.__options.path, sep=self.__sep, encoding=self.__encoding, index=False)
