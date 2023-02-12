import logging
from typing import Any, MutableMapping

AnyLogger = logging.Logger | logging.LoggerAdapter[Any]


class KVLoggerAdapter(logging.LoggerAdapter[AnyLogger]):
    def __init__(self, logger: AnyLogger, **kwds: Any):
        super().__init__(logger, {})

        prefixes: list[str] = []
        for key, value in kwds.items():
            prefixes.append(f"'{key}'='{value}'")

        self.__prefix = ", ".join(prefixes)

    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> tuple[str, MutableMapping[str, Any]]:
        return self.__prefix + ", " + msg, kwargs
