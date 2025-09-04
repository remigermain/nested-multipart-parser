from nested_multipart_parser.lazy import lazy_regex_compile


class InvalidFormat(Exception):
    """key is invalid formated"""

    def __init__(self, key):
        super().__init__(f"invaid key format: {key}")


class NestedParserOptionsType(type):
    def __new__(cls, cls_name, ns, childs):
        if cls_name != "NestedParserOptionsAbstract" and cls_name:
            if "sanitize" not in childs:
                raise ValueError("you need to define sanitize methods")
        return super().__new__(cls, cls_name, ns, childs)


INVALID_TOKEN_PARSER = ("[", "]", ".")


class NestedParserOptionsAbstract(metaclass=NestedParserOptionsType):
    def check(self, key, keys):
        if len(keys) == 0:
            raise InvalidFormat(key)

        first = keys[0]
        for token in INVALID_TOKEN_PARSER:
            if token in first:
                raise InvalidFormat(key)

        for key in keys:
            if not isinstance(key, str):
                continue
            for c in key:
                if c.isspace():
                    raise InvalidFormat(key)

    def split(self, key):
        contents = list(filter(None, self._reg_spliter.split(key)))
        if not contents:
            raise ValueError(f"invalid form key: {key}")

        lst = [contents[0]]
        if len(contents) >= 2:
            lst.extend(self._reg_options.split(contents[1]))
        if len(contents) == 3:
            lst.append(contents[2])

        return list(filter(None, lst))


class NestedParserOptionsDot(NestedParserOptionsAbstract):
    def __init__(self):
        self._reg_spliter = lazy_regex_compile(r"^([^\.]+)(.*?)(\.)?$")
        self._reg_options = lazy_regex_compile(r"(\.[^\.]+)")

    def sanitize(self, key, value):
        contents = self.split(key)
        lst = contents[1:]
        keys = [contents[0]]
        for idx, k in enumerate(lst):
            if k.startswith("."):
                k = k[1:]
                if not k:
                    if len(lst) != idx + 1:
                        raise InvalidFormat(key)
                    value = {}
                    break
                try:
                    k = int(k)
                except Exception:
                    pass
            else:
                raise InvalidFormat(key)
            keys.append(k)

        return keys, value


class NestedParserOptionsBracket(NestedParserOptionsAbstract):
    def __init__(self):
        self._reg_spliter = lazy_regex_compile(r"^([^\[\]]+)(.*?)(\[\])?$")
        self._reg_options = lazy_regex_compile(r"(\[[^\[\]]+\])")

    def sanitize(self, key, value):
        first, *lst = self.split(key)
        keys = [first]

        for idx, k in enumerate(lst):
            if k.startswith("[") or k.endswith("]"):
                if not k.startswith("[") or not k.endswith("]"):
                    raise InvalidFormat(key)
                k = k[1:-1]
                if not k:
                    if len(lst) != idx + 1:
                        raise InvalidFormat(key)
                    value = []
                    break
                try:
                    k = int(k)
                except Exception:
                    pass
            else:
                raise InvalidFormat(key)
            keys.append(k)
        return keys, value


class NestedParserOptionsMixedDot(NestedParserOptionsAbstract):
    def __init__(self):
        self._reg_spliter = lazy_regex_compile(
            r"^([^\[\]\.]+)(.*?)((?:\.)|(?:\[\]))?$"
        )
        self._reg_options = lazy_regex_compile(r"(\[\d+\])|(\.[^\[\]\.]+)")

    def sanitize(self, key, value):
        first, *lst = self.split(key)
        keys = [first]

        for idx, k in enumerate(lst):
            if k.startswith("."):
                k = k[1:]
                # empty dict
                if not k:
                    if len(lst) != idx + 1:
                        raise InvalidFormat(key)
                    value = {}
                    break
            elif k.startswith("[") or k.endswith("]"):
                if not k.startswith("[") or not k.endswith("]"):
                    raise InvalidFormat(key)
                k = k[1:-1]
                if not k:
                    if len(lst) != idx + 1:
                        raise InvalidFormat(key)
                    value = []
                    break
                k = int(k)
            else:
                raise InvalidFormat(key)
            keys.append(k)

        return keys, value


class NestedParserOptionsMixed(NestedParserOptionsMixedDot):
    def __init__(self):
        self._reg_spliter = lazy_regex_compile(
            r"^([^\[\]\.]+)(.*?)((?:\.)|(?:\[\]))?$"
        )
        self._reg_options = lazy_regex_compile(r"(\[\d+\])|(\.?[^\[\]\.]+)")

    def sanitize(self, key, value):
        first, *lst = self.split(key)
        keys = [first]

        for idx, k in enumerate(lst):
            if k.startswith("."):
                k = k[1:]
                # empty dict
                if not k:
                    if len(lst) != idx + 1:
                        raise InvalidFormat(key)
                    value = {}
                    break
            elif k.startswith("[") or k.endswith("]"):
                if not k.startswith("[") or not k.endswith("]"):
                    raise InvalidFormat(key)
                k = k[1:-1]
                if not k:
                    if len(lst) != idx + 1:
                        raise InvalidFormat(key)
                    value = []
                    break
                k = int(k)
            keys.append(k)

        return keys, value
