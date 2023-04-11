from typing import Any, Tuple, Union

Number = Union[int, float]

class Field:
    """
    Abstract base class for all transcode-able fields.
    """
    def __init__(self, name: str, length: int, optional=False):
        self.name = name
        self.length = length # length in bits
        self.optional = optional # boolean flag for allowing falsy encoded data (ie. empty string)

    def decode(self, data: bytes) -> Any:
        """
        Converts self.length bits of 'data' to the corresponding python value of the field.
        This value could be an integer, string, etc. depending on the specific field type.

        Note: 'data' should be LSB-aligned which is how BitString.pop currently returns its data.
        """
        raise NotImplementedError

    def encode(self, value: Any) -> Tuple[bytes, int]:
        """
        Converts value to self.length bits of data where value is the specific field type.
        Returns a tuple of (encoded_value, self.length) or raises
        a ValueError with an appropiate message if this is not possible.

        Note: 'value' should be LSB-aligned which is how BitString.push currently expects its data.
        """
        raise NotImplementedError

class ASCII(Field):
    """
    Provides transcoding between binary data and ASCII-encoded text.
    """
    def decode(self, data: bytes) -> str:
        """
        ASCIIs are automatically padded with leading \x00 to ensure correct alignment.
        Therefore, when decoding, we must perform adjustments to return the original encoded data.
        """
        # we need to manually replace the null bytes to return the original data
        return data.replace(b'\x00', b'').decode('ascii')
    
    def encode(self, value: str) -> Tuple[bytes, int]:
        if type(value) != str:
            raise ValueError(f"{value} is not a string")
        if not value.isascii():
            raise ValueError(f"{value} contains non-ascii character(s)")
        if self.length < 8*len(value.encode('ascii')):
            raise ValueError(f"{value} is too large for {self.length//8} character(s)")
        if not self.optional and not value:
            raise ValueError(f"{self.name} cannot encode empty strings")

        # we want strings to be left aligned when they are encoded so pad with trailing \x00
        encoded_data = value.encode('ascii').ljust(self.length // 8, b'\x00')
        return (encoded_data, self.length)

class Enum(Field):
    """
    Provides bijective mapping between (key, value) pairs.
    """
    def __init__(self, name: str, length: int, map_key_val: dict):
        super().__init__(name, length)

        self.map_key_val = map_key_val
        self.map_val_key = {v: k for k, v in self.map_key_val.items()}

        # ensure map is bijective
        value_size = len(self.map_key_val.values())
        unique_value_size = len(set(self.map_key_val.values()))
        if value_size != unique_value_size:
            # weakening the proposition but this message should be clearer
            raise ValueError(f"Mapping '{self.name}' is not bijective: has {value_size} values but only {unique_value_size} are unique")

        for k, v in map_key_val.items():
            if v < 0:
                raise ValueError(f"Mapping value {v} for key {k} must be non-negative")
            if v >= 1 << self.length:
                raise ValueError(f"Mapping value {v} for key {k} is too large to fit in {self.length} bits")

    def decode(self, data: bytes):
        value = int.from_bytes(data, byteorder='big', signed=False)
        if value not in self.map_val_key:
            raise ValueError(f"Value '{value}' not found in map '{self.name}'")

        return self.map_val_key[value]

    def encode(self, key) -> Tuple[bytes, int]:
        if key not in self.map_key_val:
            raise ValueError(f"Key '{key}' not found in map '{self.name}'")

        encoded_data = self.map_key_val[key].to_bytes((self.length + 7) // 8, byteorder='big')
        return (encoded_data, self.length)
    
class Numeric(Field):
    """
    Provides transcoding between binary data and (un)signed numbers,
    where 'Number' is defined as either a floating or integer type.
    Offers value scaling between conversions (note: there may be imprecision).
    """
    def __init__(self, name: str, length: int, scale = 1, signed = False):
        super().__init__(name, length)
        self.scale = scale
        self.signed = signed

    def decode(self, data: bytes) -> Number:
        value = int.from_bytes(data, byteorder='big', signed = self.signed)
        return value * self.scale

    def encode(self, value: Number) -> Tuple[bytes, int]:
        if not isinstance(value, Number):
            raise ValueError(f"Value '{value}' is not a valid number")

        value = int(value // self.scale)
        hex_value = hex(value)
        if not self.signed:
            if value >= 1 << self.length:
                raise ValueError(f"Value '{value}' ({hex_value}) is too large for {self.length} unsigned bits")
            if value < 0:
                raise ValueError(f"Cannot encode negative value '{value}' in an unsigned field")
        else:
            if value >= 1 << (self.length - 1):
                raise ValueError(f"Value '{value}' ({hex_value}) is too large for {self.length} signed bits")
            if value < -1 << (self.length - 1):
                raise ValueError(f"Value '{value}' ({hex_value}) is too small for {self.length} signed bits")
        
        encoded_data = value.to_bytes((self.length + 7) // 8, byteorder='big', signed=self.signed)
        return (encoded_data, self.length)

class Switch(Field):
    """
    Wrapper for Enum and provides surjective mapping for enum keys and an another dictionary.
    """
    def __init__(self, enum: Enum, map_key_enum: dict):
        super().__init__(enum.name, enum.length)
        self.enum = enum
        self.map_key_enum = map_key_enum
        self.name = enum.name
        self.length = enum.length

    def decode(self, data: bytes):
        return self.enum.decode(data)

    def encode(self, value) -> Tuple[bytes, int]:
        return self.enum.encode(value)
    
    def get_fields(self, key):
        return self.map_key_enum[key]
