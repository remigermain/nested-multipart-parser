import re


class NestedParser:
    _valid = None
    errors = None

    def __init__(self, data, options={}):
        self.data = data
        self._merge_options(options)

    def _merge_options(self, options):
        DEFAULT_OPTIONS = {
            "separator": "bracket",
            "raise_duplicate": True,
            "assign_duplicate": False
        }

        options = {**DEFAULT_OPTIONS, **options}
        self._options = options

        assert self._options.get("separator", "dot") in [
            "dot", "bracket", "mixed", "mixed-dot"]
        assert isinstance(self._options.get("raise_duplicate", False), bool)
        assert isinstance(self._options.get("assign_duplicate", False), bool)

        self.__is_dot = False
        self.__is_mixed = False
        self.__is_bracket = False
        self.__is_mixed_dot = False
        if self._options["separator"] == "dot":
            self.__is_dot = True
        elif self._options["separator"] == "mixed":
            self.__is_mixed = True
        elif self._options["separator"] == "mixed-dot":
            self.__is_mixed_dot = True
        else:
            self.__is_bracket = True
            self._reg = re.compile(r"\[|\]")

    def mixed_split(self, key):
        def span(key, i):
            old = i
            while i != len(key):
                if key[i] in ".[]":
                    break
                i += 1
            if old == i:
                raise ValueError(
                    f"invalid format key '{full_keys}', empty key value at position {i + pos}")
            return i

        full_keys = key
        idx = span(key, 0)
        pos = idx
        keys = [key[:idx]]
        key = key[idx:]

        i = 0
        last_is_list = False
        while i < len(key):
            if key[i] == '[':
                i += 1
                idx = span(key, i)
                if key[idx] != ']':
                    raise ValueError(
                        f"invalid format key '{full_keys}', not end with bracket at position {i + pos}")
                sub = key[i: idx]
                if not sub.isdigit():
                    raise ValueError(
                        f"invalid format key '{full_keys}', list key is not a valid number at position {i + pos}")
                keys.append(int(key[i: idx]))
                i = idx + 1
                last_is_list = True
            elif key[i] == ']':
                raise ValueError(
                    f"invalid format key '{full_keys}', not start with bracket at position {i + pos}")
            elif (key[i] == '.' and self.__is_mixed_dot) or (
                not self.__is_mixed_dot and (
                    (key[i] != '.' and last_is_list) or
                    (key[i] == '.' and not last_is_list)
                )
            ):
                if self.__is_mixed_dot or not last_is_list:
                    i += 1
                idx = span(key, i)
                keys.append(key[i: idx])
                i = idx
                last_is_list = False
            else:
                raise ValueError(
                    f"invalid format key '{full_keys}', invalid char at position {i + pos}")
        return keys

    def split_key(self, key):
        # remove space
        k = key.replace(" ", "")
        if len(k) != len(key):
            raise Exception(f"invalid format from key {key}, no space allowed")

        # remove empty string and count key length for check is a good format
        # reduce + filter are a hight cost so do manualy with for loop

        # optimize by split with string func
        if self.__is_mixed or self.__is_mixed_dot:
            return self.mixed_split(key)
        if self.__is_dot:
            length = 1
            splitter = key.split(".")
        else:
            length = 2
            splitter = self._reg.split(key)

        check = -length

        results = []
        for select in splitter:
            if select:
                results.append(select)
                check += len(select) + length

        if len(key) != check:
            raise Exception(f"invalid format from key {key}")
        return results

    def set_type(self, dtc, key, value, full_keys, prev=None, last=False):
        if isinstance(dtc, list):
            key = int(key)
            if len(dtc) < key:
                raise ValueError(
                    f"key \"{full_keys}\" is upper than actual list")
            if len(dtc) == key:
                dtc.append(value)
        elif isinstance(dtc, dict):
            if key not in dtc or last and self._options["assign_duplicate"]:
                dtc[key] = value
        else:
            if self._options["raise_duplicate"]:
                raise ValueError(
                    f"invalid rewrite key from \"{full_keys}\" to \"{dtc}\"")
            elif self._options["assign_duplicate"]:
                dtc = prev['dtc']
                dtc[prev['key']] = prev['type']
                return self.set_type(dtc[prev['key']], key, value, full_keys, prev, last)
        return key

    def get_next_type(self, key):
        if self.__is_mixed or self.__is_mixed_dot:
            return [] if isinstance(key, int) else {}
        return [] if key.isdigit() else {}

    def convert_value(self, data, key):
        return data[key]

    def construct(self, data):
        dictionary = {}
        prev = {}

        for key in data:
            keys = self.split_key(key)
            tmp = dictionary

            # need it for duplicate assignement
            prev['key'] = keys[0]
            prev['dtc'] = tmp
            prev['type'] = None

            # optimize with while loop instend of for in with zip function
            i = 0
            lenght = len(keys) - 1
            while i < lenght:
                set_type = self.get_next_type(keys[i+1])
                index = self.set_type(tmp, keys[i], set_type, key, prev)

                prev['dtc'] = tmp
                prev['key'] = index
                prev['type'] = set_type

                tmp = tmp[index]
                i += 1

            value = self.convert_value(data, key)
            self.set_type(tmp, keys[-1], value, key, prev, True)
        return dictionary

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
                "You need to be call is_valid() before access validate_data")
        if self._valid is False:
            raise ValueError("You can't get validate data")
        return self.__validate_data
