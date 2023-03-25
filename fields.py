from field import Field

import constants

class ASCII(Field):
    """
    Provides transcoding between binary data and ASCII-encoded text.
    """
    def __init__(self, name, length, optional=False):
        super().__init__(name, length, optional)

    def decode(self, data):
        return data.replace(b'\x00', b'').decode('ascii')
    
    def encode(self, value):
        if self.contains(value):
            encoded_data = value.encode('ascii')
            return (encoded_data, self.length)

    def contains(self, value):
        if type(value) != str:
            raise ValueError(f"Value '{value}' is not a string.")
        if not value.isascii():
            raise ValueError(f"String '{value}' contains non-ascii character(s).")
        if self.length < 8*len(value.encode('ascii')):
            raise ValueError(f"String '{value}' is too large for {self.length//8} character(s).")
        return True
    
class Enum(Field):
    """
    Provides bijective mapping between (key, value) pairs.
    """
    def __init__(self, name, length, map_key_val):
        super().__init__(name, length)

        self.map_key_val = map_key_val
        self.map_val_key = {v: k for k, v in self.map_key_val.items()}

        # ensure map is bijective
        value_size = len(self.map_key_val.values())
        unique_value_size = len(set(self.map_key_val.values()))
        if value_size != unique_value_size:
            raise ValueError(f"Mapping {self.name} is not injective: has {value_size} values but only {unique_value_size} are unique.")

        for k, v in map_key_val.items():
            if v < 0:
                raise ValueError(f"Mapping value {v} for key {k} must be non-negative.")
            if v >= 1 << self.length:
                raise ValueError(f"Mapping value {v} for key {k} is too large to fit in {self.length} bits.")

    def decode(self, data):
        value = int.from_bytes(data, byteorder=constants.BYTE_ORDER, signed=False)
        if self.containsValue(value):
            return self.map_val_key[value]

    def encode(self, key):
        if self.contains(key):
            encoded_data = self.map_key_val[key].to_bytes((self.length + 7) // 8, byteorder=constants.BYTE_ORDER)
            return (encoded_data, self.length)
    
    def contains(self, key):
        if key not in self.map_key_val:
            raise ValueError(f"Key '{key}' not found in mapping {self.name}.")
        return True
    
    def containsValue(self, value):
        if value not in self.map_val_key:
            raise ValueError(f"Value '{value}' not found in mapping {self.name}.")
        return True
    
class Numeric(Field):
    """
    Provides transcoding between binary data and (un)signed integers.
    Offers value scaling during transcoding but note that there may be imprecision during conversion.
    """
    def __init__(self, name, length, scale = 1, signed = False):
        super().__init__(name, length)
        self.scale = scale
        self.signed = signed

    def decode(self, data):
        value = int.from_bytes(data, byteorder=constants.BYTE_ORDER, signed = self.signed)
        return value * self.scale

    def encode(self, value):
        if self.contains(value):
            value = int(value // self.scale)
            encoded_data = value.to_bytes((self.length + 7) // 8, byteorder=constants.BYTE_ORDER, signed=self.signed)
            return (encoded_data, self.length)

    def contains(self, value):
        if type(value) != int and type(value) != float:
            raise ValueError(f"Value '{value}' is not a number.")
        value = int(value // self.scale)
        hex_value = hex(value)
        if not self.signed:
            if value >= 1 << self.length:
                raise ValueError(f"Value {value} ({hex_value}) is too large for {self.length} unsigned bits.")
            if value < 0:
                raise ValueError(f"Cannot encode negative value {value} in an unsigned field.")
        else:
            if value >= 1 << (self.length - 1):
                raise ValueError(f"Value {value} ({hex_value}) is too large for {self.length} signed bits.")
            if value < -1 << (self.length - 1):
                raise ValueError(f"Value {value} ({hex_value}) is too small for {self.length} signed bits.")
        return True

class Switch(Field):
    """
    Provides surjective mapping for enum keys and an another dictionary.
    """
    def __init__(self, enum, map_key_enum):
        super().__init__(enum.name, enum.length)
        self.enum = enum
        self.map_key_enum = map_key_enum
        self.name = enum.name
        self.length = enum.length

    def decode(self, data):
        return self.enum.decode(data)

    def encode(self, value):
        return self.enum.encode(value)
    
    def contains(self, value):
        return self.enum.contains(value)

    def get_fields(self, data):
        return self.map_key_enum[self.enum.decode(data)]
