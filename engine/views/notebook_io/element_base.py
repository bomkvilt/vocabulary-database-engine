import abc
import dataclasses
from typing import Any, Callable, Optional

from ipywidgets import widgets


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
        assert hasattr(widgets, "value")

        self._wrap_element(self.widget)
        self.__manual_value: Any = None

    def get_widget(self) -> widgets.Widget:
        return self.widget

    def add_callback(self, callback: Callable[[ValueChangeInfo], None]) -> None:
        def inner(value: dict[str, Any]) -> None:
            assert value["owner"] == self.widget

            # ignore the case when we have just updated the widget manually
            if value["new"] == self.__manual_value:
                self.__manual_value = None
                return

            info = ValueChangeInfo(
                new_value=value["new"],
                old_value=value["old"],
                widget=self.widget,
            )
            callback(info)

        self.widget.observe(inner, "value")  # type: ignore

    def set_value(self, new_value: Any) -> None:
        self.__manual_value = new_value
        self.widget.value = new_value  # type: ignore
