class NestedDeclare:
    def __init__(self, _type=None):
        self._elements = {}
        self.set_type(_type)
    
    def set_type(self, _type):
        self._is_dict = _type is dict
        self._is_list = _type is list
        self._is_none = _type is None
    
    def set_type_from_key(self, key):
        self.set_type(list if isinstance(key, int) else dict)
    
    def conv_value(self, key):
        value = self._elements[key]
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
            raise ValueError("key is already set")

        self._elements[key] = value
    
    def __getitem__(self, key):
        if key not in self._elements:
            self[key] = type(self)()
        return self._elements[key]
    
    def _convert_list(self):
        keys = sorted(self._elements.keys())
        if keys != list(range(len(keys))):
            raise ValueError("invalid format list keys")
        
        return [self.conv_value(key) for key in keys]
    
    def _convert_dict(self):
        return {
            key: self.conv_value(value)
            for key, value in self._elements.items()
        }

    def convert(self):
        if self._is_none:
            return None
        if self._is_list:
            return self._convert_list()
        return self._convert_dict()