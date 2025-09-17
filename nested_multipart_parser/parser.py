from nested_multipart_parser.options import (
    NestedParserOptionsBracket,
    NestedParserOptionsDot,
    NestedParserOptionsMixed,
    NestedParserOptionsMixedDot,
)
from nested_multipart_parser.temp_element import TempDict, TempList

DEFAULT_OPTIONS = {
    "separator": "mixed-dot",
    "raise_duplicate": True,
    "assign_duplicate": False,
}

REGEX_SEPARATOR = {
    "bracket": NestedParserOptionsBracket,
    "dot": NestedParserOptionsDot,
    "mixed": NestedParserOptionsMixed,
    "mixed-dot": NestedParserOptionsMixedDot,
}


class NestedParser:
    _valid = None
    errors = None

    def __init__(self, data, options=None):
        self.data = data
        self._options = {**DEFAULT_OPTIONS, **(options or {})}

        assert self._options["separator"] in [
            "dot",
            "bracket",
            "mixed",
            "mixed-dot",
        ]
        assert isinstance(self._options["raise_duplicate"], bool)
        assert isinstance(self._options["assign_duplicate"], bool)

        self._cls_options = REGEX_SEPARATOR[self._options["separator"]]

    def _split_keys(self, data):
        checker = self._cls_options()
        for key, value in data.items():
            keys, value = checker.sanitize(key, value)
            checker.check(key, keys)

            yield keys, value

    def convert_value(self, value):
        return value

    def construct(self, data):
        dictionary = TempDict(self._options)

        for keys, value in self._split_keys(data):
            tmp = dictionary

            for actual_key, next_key in zip(keys, keys[1:]):
                if isinstance(next_key, int):
                    tmp[actual_key] = TempList(self._options)
                else:
                    tmp[actual_key] = TempDict(self._options)
                tmp = tmp[actual_key]

            tmp[keys[-1]] = self.convert_value(value)
        return dictionary.convert()

    def is_valid(self):
        self._valid = False
        try:
            self.__validate_data = self.construct(self.data)
            self._valid = True
        except Exception as err:
            self.errors = err
        return self._valid

    @property
    def validate_data(self):
        if self._valid is None:
            raise ValueError(
                "You need to be call is_valid() before access validate_data"
            )
        if self._valid is False:
            raise ValueError("You can't get validate data")
        return self.__validate_data
