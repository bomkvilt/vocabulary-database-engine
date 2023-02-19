import abc

import pandas as pd
import pydantic


@pydantic.dataclasses.dataclass(kw_only=True)
class StorageBase(abc.ABC):
    @abc.abstractmethod
    def read_dump(self) -> pd.DataFrame | None:
        pass

    @abc.abstractmethod
    def save_dump(self, dump: pd.DataFrame) -> None:
        pass
