from __future__ import annotations

import abc
import dataclasses
from typing import Any, Callable, Generic, Optional, Self, TypeVar

from ipywidgets import widgets

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")


@dataclasses.dataclass(kw_only=True)
class ElementConfig:
    show_debug_frames: bool = False


@dataclasses.dataclass(kw_only=True)
class ElementBase(abc.ABC):
    config: ElementConfig

    @abc.abstractmethod
    def get_widget(self) -> widgets.Widget:
        pass

    def _wrap_element(self, widget: widgets.Widget) -> widgets.Widget:
        if self.config.show_debug_frames:
            self.__feature_add_border(widget)

        return widget

    def __get_layout(self, widget: widgets.Widget) -> Optional[widgets.Layout]:
        if hasattr(widget, "layout"):
            layout = widget.layout  # type: ignore
            assert isinstance(layout, widgets.Layout)
            return layout

        return None

    def __feature_add_border(self, widget: widgets.Widget) -> None:
        if layout := self.__get_layout(widget):
            if layout.border is None:
                layout.border = "1px solid black"


@dataclasses.dataclass(kw_only=True)
class ValueChangeInfo:
    new_value: Any
    old_value: Any
    widget: widgets.Widget


@dataclasses.dataclass(kw_only=True)
class ChangableWidget(ElementBase):
    widget: widgets.Widget

    def __post_init__(self) -> None:
        self._wrap_element(self.widget)
        self.__manual_value: Any = None
        self.__couser: Optional[ElementBase] = None

    def get_widget(self) -> widgets.Widget:
        return self.widget

    def add_callback(self: Self, callback: Callable[[ValueChangeInfo, Optional[ElementBase]], None]) -> Self:
        def inner(value: dict[str, Any]) -> None:
            assert value["owner"] == self.widget

            # ignore the case when we have just updated the widget manually
            couser: Optional[ElementBase] = None
            if value["new"] == self.__manual_value:
                couser = self.__couser
                self.__manual_value = None
                self.__couser = None

            info = ValueChangeInfo(
                new_value=value["new"],
                old_value=value["old"],
                widget=self.widget,
            )
            callback(info, couser)

        self.widget.observe(inner, "value")  # type: ignore
        return self

    @property
    def value(self) -> Any:
        if hasattr(self.widget, "value"):
            return self.widget.value  # type: ignore
        assert hasattr(self.widget, "value")  # crutch

    def set_value(self, new_value: Any, couser: ElementBase) -> None:
        assert hasattr(self.widget, "value")
        self.__manual_value = new_value
        self.__couser = couser
        self.widget.value = new_value  # type: ignore


@dataclasses.dataclass(kw_only=False)
class ElementProperty(Generic[_T1]):
    Getter = Callable[[Any], _T2]
    Setter = Callable[[Any, _T2, ElementBase], None]
    Observer = Callable[[_T2, Optional[ElementBase]], None]

    fget: Getter[_T1]
    fset: Setter[_T1] | None = None

    class Wrapper(Generic[_T2]):
        def __init__(
            self, *,
            fget: ElementProperty[_T1].Getter[_T2],
            fset: ElementProperty[_T1].Setter[_T2] | None,
            clbs: list[ElementProperty[_T1].Observer[_T2]],
            obj: Any,
        ) -> None:
            self.__fget = fget
            self.__fset = fset
            self.__clbs = clbs
            self.__obj = obj

        @property
        def value(self) -> _T2:
            return self.__fget(self.__obj)

        def set_value(self, new_value: _T2, couser: ElementBase) -> None:
            if self.__fset is None:
                raise AttributeError("setter is none")

            self.__fset(self.__obj, new_value, couser)

        def observe(self, clb: ElementProperty[_T1].Observer[_T2]) -> None:
            self.__clbs.append(clb)

        def unobserve(self, clb: ElementProperty[_T1].Observer[_T2]) -> None:
            self.__clbs = [x for x in self.__clbs if x != clb]

        def broadcast(self, couser: Optional[ElementBase]) -> None:
            if len(self.__clbs) > 0:
                value = self.value
                for clb in self.__clbs:
                    clb(value, couser)

    def __post_init__(self):
        self.__doc__ = self.fget.__doc__
        self.__subscribers: list[ElementProperty[_T1].Observer[_T1]] = []

    def __get__(self, obj: Any, _: Any) -> Wrapper[_T1]:
        if obj is None:
            raise AttributeError("object cannot be nullptr")

        return ElementProperty[_T1].Wrapper[_T1](
            fget=self.fget,
            fset=self.fset,
            clbs=self.__subscribers,
            obj=obj,
        )

    def getter(self, fget: Getter[_T1]) -> None:
        self.fget = fget

    def setter(self, fset: Setter[_T1]) -> None:
        self.fset = fset


def element_property(fget: Callable[[Any], _T1]) -> ElementProperty[_T1]:
    return ElementProperty[_T1](fget)
