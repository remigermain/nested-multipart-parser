class NestedDeclare:
    """Create ditc/list wihout order"""

    def __init__(self, _type=None, options=None):
        self._elements = {}
        self._options = options or {}
        self.set_type(_type)

    def __repr__(self):
        return f"{type(self).__name__}({self._type.__name__})"

    def set_type(self, _type):
        self._type = _type
        self._is_dict = _type is dict
        self._is_list = _type is list
        self._is_none = _type is None

    def get_type(self):
        return self._type

    def set_type_from_key(self, key):
        self.set_type(list if isinstance(key, int) else dict)

    def conv_value(self, value):
        if isinstance(value, type(self)):
            value = value.convert()
        return value

    def __setitem__(self, key, value):
        if self._is_none:
            self.set_type_from_key(key)
        if isinstance(key, int) and not self._is_list:
            raise ValueError("int key cant be integer for dict object")
        if not isinstance(key, int) and self._is_list:
            raise ValueError("need integer key for list elements")

        if key in self._elements:
            if (
                isinstance(value, type(self))
                and isinstance(self._elements[key], type(self))
                and self._elements[key].get_type() == value.get_type()
            ):
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

    def _convert_list(self):
        keys = sorted(self._elements.keys())
        if keys != list(range(len(keys))):
            raise ValueError("invalid format list keys")

        return [self.conv_value(self._elements[key]) for key in keys]

    def _convert_dict(self):
        return {key: self.conv_value(value) for key, value in self._elements.items()}

    def convert(self):
        if self._is_none:
            return None
        if self._is_list:
            return self._convert_list()
        return self._convert_dict()
