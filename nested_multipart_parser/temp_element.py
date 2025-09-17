import abc
from typing import Any


class TempElement(abc.ABC):
    @abc.abstractclassmethod
    def __setitem__(self, key, val):
        """method to set element"""

    def check(self, key, value):
        if key in self._elements:
            # same instance like templist to templist, we ignore it
            if isinstance(self._elements[key], type(value)):
                return

            if self._options.get("raise_duplicate"):
                raise ValueError("key is already set")

            if not self._options.get("assign_duplicate"):
                return

        self._elements[key] = value

    def __getitem__(self, key):
        if key not in self._elements:
            self[key] = type(self)(options=self._options)
        return self._elements[key]

    def conv_value(self, value: Any) -> Any:
        if isinstance(value, TempElement):
            value = value.convert()
        return value

    @abc.abstractmethod
    def convert(self):
        """method to convert tempoary element to real python element"""


class TempList(TempElement):
    def __init__(self, options=None):
        self._options = options or {}
        self._elements = {}

    def __setitem__(self, key: int, value: Any):
        assert isinstance(key, int), (
            f"Invalid key for list, need to be int, type={type(key)}"
        )
        self.check(key, value)

    def convert(self) -> list:
        keys = sorted(self._elements.keys())
        # check if index start to 0 and end to number of elements
        if any((keys[0] != 0, keys[-1] != (len(self._elements) - 1))):
            raise ValueError("invalid format list keys")

        return [self.conv_value(self._elements[key]) for key in keys]


class TempDict(TempElement):
    def __init__(self, options=None):
        self._options = options or {}
        self._elements = {}

    def __setitem__(self, key: str, value: Any):
        assert isinstance(key, str), (
            f"Invalid key for dict, need to be str, type={type(key)}"
        )
        self.check(key, value)

    def convert(self) -> dict:
        return {
            key: self.conv_value(value) for key, value in self._elements.items()
        }
