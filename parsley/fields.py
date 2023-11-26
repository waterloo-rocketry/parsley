from typing import Any, Tuple, Union

Number = Union[int, float]

class Field:
    """
    Abstract base class for all fields that can be transcoded.

    Note: data is assumed to be LSB-aligned to match the implementation of BitString.
    """
    def __init__(self, name: str, length: int, unit=""):
        self.name = name
        self.length = length # length in bits
        self.unit = unit # optional unit description

    def decode(self, data: bytes) -> Any:
        """
        Converts `self.length` bits of `data` to the field's corresponding python value.
        This value could be an integer, string, etc. depending on the specific field type.
        """
        raise NotImplementedError

    def encode(self, value: Any) -> Tuple[bytes, int]:
        """
        Converts value to `self.length` bits of data and returns a tuple of (encoded_value, self.length)
        or raises a ValueError with an appropiate message if this is not possible.
        
        self.length is returned in order to properly parse leading zeros. For example,
        the following cases are bit-level identical, but are not equilvalent for our purposes:
        2-bit: ______10
        4-bit: ____0010
        8-bit: 00000010 (<= they all look like this)
        """
        raise NotImplementedError

class ASCII(Field):
    """
    Transcodes binary data and ASCII text.

    For example:
    b'\x48\x65\x79' <=> 'Hey'
    """
    def decode(self, data: bytes) -> str:
        return data.replace(b'\x00', b'').decode('ascii') # remove null bytes to return original data 
    
    def encode(self, value: str) -> Tuple[bytes, int]:
        if type(value) != str:
            raise ValueError(f'{value} is not a string')
        if not value.isascii():
            raise ValueError(f'{value} contains non-ascii character(s)')
        if self.length < 8*len(value.encode('ascii')):
            raise ValueError(f'{value} is too large for {self.length//8} character(s)')

        # we want strings to be left aligned after they're encoded so pad with trailing null bytes
        encoded_data = value.encode('ascii').ljust(self.length // 8, b'\x00')
        return (encoded_data, self.length)

class Enum(Field):
    """
    Transcodes binary data using a user-defined dictionary.

    This allows for customizable byte interpretations:
    dictionary: {'GENERAL_CMD': 0x060, 'RESET_CMD': 0x160}
    b'\x01\x60' <=> 'RESET_CMD'
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
            raise ValueError(f'Mapping "{self.name}" is not bijective: has {value_size} values but only {unique_value_size} are unique')

        for k, v in map_key_val.items():
            if v < 0:
                raise ValueError(f'Mapping value {v} for key {k} must be non-negative')
            if v >= 1 << self.length:
                raise ValueError(f'Mapping value {v} for key {k} is too large to fit in {self.length} bits')

    def decode(self, data: bytes):
        value = int.from_bytes(data, byteorder='big', signed=False)
        if value not in self.map_val_key:
            raise ValueError(f'Value "{value}" not found in map "{self.name}"')

        return self.map_val_key[value]

    def encode(self, key) -> Tuple[bytes, int]:
        if key not in self.map_key_val:
            raise ValueError(f'Key "{key}" not found in map "{self.name}"')

        encoded_data = self.map_key_val[key].to_bytes((self.length + 7) // 8, byteorder='big')
        return (encoded_data, self.length)
    
    def get_keys(self):
        return self.map_key_val.keys()
    
    def render_enum(self):
        nl = '\n'
        output = f'enum {self.name} {{{nl}'
        
        for idx, (k,v) in enumerate(self.map_key_val.items()):
            output += f'    {k}{"" if idx else f" = {v}"}{nl}'

        output += '}\n'

        return output
    
    
class Numeric(Field):
    """
    Transcodes binary data and numbers (ie. (un)signed and/or floating point)
    with an optional scaling factor during transcoding.

    For example:
    b'\xFC' <=> -4 (two's complement)
    """
    def __init__(self, name: str, length: int, scale=1, signed=False, unit=""):
        super().__init__(name, length, unit)
        self.scale = scale
        self.signed = signed

    def decode(self, data: bytes) -> Number:
        value = int.from_bytes(data, byteorder='big', signed = self.signed)
        return value * self.scale

    def encode(self, value: Number) -> Tuple[bytes, int]:
        if not isinstance(value, Number):
            raise ValueError(f'Value "{value}" is not a valid number')

        value = int(value // self.scale)
        hex_value = hex(value)
        if not self.signed:
            if value >= 1 << self.length:
                raise ValueError(f'Value "{value}" ({hex_value}) is too large for {self.length} unsigned bits')
            if value < 0:
                raise ValueError(f'Cannot encode negative value "{value}" in an unsigned field')
        else:
            if value >= 1 << (self.length - 1):
                raise ValueError(f'Value "{value}" ({hex_value}) is too large for {self.length} signed bits')
            if value < -1 << (self.length - 1):
                raise ValueError(f'Value "{value}" ({hex_value}) is too small for {self.length} signed bits')
        
        encoded_data = value.to_bytes((self.length + 7) // 8, byteorder='big', signed=self.signed)
        return (encoded_data, self.length)

class Switch(Enum):
    """
    An Enum wrapper to map binary data -> list of Fields using a user-defined dictionary.

    For perspective, our CAN messages are defined as a Switch that maps:
    binary data <=> string (message type) and then
    string -> list of Fields (the specific fields that are defined in the message type)
    """
    def __init__(self, name: str, length: int, map_key_val: dict, map_key_enum: dict):
        super().__init__(name, length, map_key_val)
        self.map_key_enum = map_key_enum

    def get_fields(self, key):
        return self.map_key_enum[key]
    
    def get_keys(self):
        return self.map_key_val.keys()
