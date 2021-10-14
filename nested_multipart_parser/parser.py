import re


class NestedParser:
    _valid = None
    errors = None
    _reg = re.compile(r"\[|\]")

    def __init__(self, data):
        self.data = data

    def split_key(self, key):
        # remove space
        k = key.replace(" ", "")
        # remove empty string and count key length for check is a good format
        # reduce + filter are a hight cost so do manualy with for loop
        results = []
        check = -2

        for select in self._reg.split(k):
            if select:
                results.append(select)
                check += len(select) + 2

        if len(k) != check:
            raise Exception(f"invalid format from key {key}")
        return results

    def set_type(self, dtc, key, value, full_keys):
        if isinstance(dtc, list):
            key = int(key)
            if len(dtc) < key:
                raise ValueError(
                    f"key \"{full_keys}\" is upper than actual list")
            if len(dtc) == key:
                dtc.append(value)
                return key
        elif isinstance(dtc, dict):
            if key not in dtc:
                dtc[key] = value
        else:
            raise ValueError(
                f"invalid rewrite key from \"{full_keys}\" to \"{dtc}\"")
        return key

    def construct(self, data):
        dictionary = {}

        for key in data:
            keys = self.split_key(key)
            tmp = dictionary

            # optimize with while loop instend of for in with zip function
            i = 0
            lenght = len(keys) - 1
            while i < lenght:
                set_type = [] if keys[i+1].isdigit() else {}
                tmp = tmp[self.set_type(tmp, keys[i], set_type, key)]
                i += 1

            self.set_type(tmp, keys[-1], data[key], key)
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
