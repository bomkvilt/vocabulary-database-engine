import abc
import collections
import dataclasses
import logging
from typing import Awaitable, Callable, Iterable, Optional

import aiorwlock

from .loggers import KVLoggerAdapter


class BusMessage(abc.ABC):
    """ An abstract for bus messages.
    """


BusEventType = str
BusDeviceId = str

BusListener = Callable[[BusEventType, BusMessage], Awaitable[None]]


@dataclasses.dataclass(kw_only=True)
class _BusListenerDispatcher:
    event_type: Optional[BusEventType]
    listener: BusListener

    def dispatch(self, event_type: BusEventType, message: BusMessage) -> bool:
        if self.event_type is None or self.event_type == event_type:
            self.listener(event_type, message)
            return True

        return False


@dataclasses.dataclass(kw_only=True)
class AsyncIOMessageBusController:
    """ Class that provides a simple message bus interface.

    NOTE: The bus is expected to be used in a async io singlethreaded context.
    """

    dispatchers = collections.defaultdict[BusDeviceId, list[_BusListenerDispatcher]](list)
    logger = logging.getLogger()

    def __post_init__(self) -> None:
        self.__mutex = aiorwlock.RWLock()

    async def register(
        self, device_id: BusDeviceId, listener: BusListener, *,
        event_types: Optional[Iterable[BusEventType]] = None,
    ) -> None:
        with self.__mutex.writer_lock:
            logger = KVLoggerAdapter(self.logger, device_id=device_id)

            all_event_types = list(event_types or [None])
            new_event_types = set(event_types or [None])

            dispatchers = self.dispatchers[device_id]
            for dispatcher in dispatchers:
                if dispatcher.listener == listener:
                    if dispatcher.event_type in all_event_types:
                        logger.info(f"event type '{dispatcher.event_type}' is already registred")
                        new_event_types.remove(dispatcher.event_type)

            for event_type in new_event_types:
                logger.info("registing a listener for event type '%s'", event_type)
                dispatchers.append(_BusListenerDispatcher(
                    event_type=event_type,
                    listener=listener,
                ))

    async def unregister(
        self, device_id: BusDeviceId, listener: BusListener, *,
        event_types: Optional[Iterable[BusEventType]] = None,
        remove_all: bool = False,
    ) -> None:
        with self.__mutex.writer_lock:
            logger = KVLoggerAdapter(self.logger, device_id=device_id)

            if remove_all and event_types is not None:
                self.logger.warning(
                    "'remove_all' have been used with a specified list of 'event_types'; "
                    "all events for the device will be removed"
                )

            all_event_types = list(event_types or [None])

            def must_be_removed(dispatcher: _BusListenerDispatcher) -> bool:
                if dispatcher.listener != listener:
                    return False

                on_remove = remove_all or dispatcher.event_type in all_event_types
                if on_remove:
                    logger.info("registing a listener for event type '%s'", dispatcher.event_type)

                return on_remove

            dispatchers = self.dispatchers[device_id]
            dispatchers = [clb for clb in dispatchers if not must_be_removed(clb)]

            if len(dispatchers) > 0:
                self.dispatchers[device_id] = dispatchers
                return

            logger.info("divice has no listeners and will be removed from bus")
            del self.dispatchers[device_id]

    async def send_message(self, device_id: BusDeviceId, event_type: str, message: BusMessage) -> None:
        with self.__mutex.reader_lock:
            logger = KVLoggerAdapter(self.logger, device_id=device_id)

            if device_id not in self.dispatchers:
                logger.warning("device_id was not found")
                return

            for dispatcher in self.dispatchers[device_id]:
                if dispatcher.event_type == event_type:
                    dispatcher.listener(event_type, message)


BUS = AsyncIOMessageBusController()
