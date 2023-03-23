from field import Field

class ASCII(Field):
    """
    Provides text-based data encoding / decoding
    """
    def __init__(self, name, length, optional=False):
        # the optional field serves no purpose in parsley but is required in omnibus
        super().__init__(name, length, optional)

    def decode(self, data):
        return data.replace(b'\x00', b'').decode('ascii')
    
    def encode(self, value):
        if self.contains(value):
            data = value.encode('ascii')
            return (data, self.length)

    def contains(self, value):
        if type(value) != str:
            raise ValueError(f"'{value}' is not a string")
        if not value.isascii():
            raise ValueError(f"String '{value}' contains non-ascii character(s)")
        if self.length < 8*len(value.encode('ascii')):
            raise ValueError(f"String '{value}' is too large for {self.length//8} character(s)")
        return True
    
class Enum(Field):
    """
    Provides bijective mapping between (key, value) pairs
    """
    def __init__(self, name, length, map_key_val):
        super().__init__(name, length)

        self.map_key_val = map_key_val
        self.map_val_key = {v: k for k, v in self.map_key_val.items()}

        # ensure map is bijective
        map_kv_size = len(self.map_key_val.values())
        set_kv_size = len(set(self.map_key_val.values()))
        if map_kv_size != set_kv_size:
            raise ValueError(f"Map {name} is not bijective: has {map_kv_size} rows but only {set_kv_size} are unique")
        map_vk_size = len(self.map_val_key.values())
        set_vk_size = len(set(self.map_val_key.values()))
        if map_vk_size != set_vk_size:
            raise ValueError(f"Map {name} is not bijective: has {map_vk_size} cols but only {set_vk_size} are unique")

        if map_kv_size != set_kv_size:
            raise ValueError(f"Map {name} is not injective ({map_kv_size} rows but only {set_kv_size} unique values)")
        for k, v in map_key_val.items():
            if v < 0:
                raise ValueError(f"Mapping for key {k} should not be negative.")
            if v >= 1 << self.length:
                raise ValueError(f"Mapping for key {k} is too large to fit in {self.length} bits.")

    def decode(self, data):
        value = int.from_bytes(data, 'big', signed=False)
        if self.containsValue(value):
            return self.map_val_key[value]

    def encode(self, key):
        if self.contains(key):
            return (self.map_key_val[key].to_bytes((self.length + 7) // 8, 'big'), self.length)
    
    def contains(self, key):
        if key not in self.map_key_val:
            raise ValueError(f"Key '{key}' not in mapping.")
        return True
    
    def containsValue(self, value):
        if value not in self.map_val_key:
            raise ValueError(f"Value '{value}' not in map")
        return True
    
class Numeric(Field):
    """
    Provides (un)signed interpretation of bytes and offers value scaling
    """
    def __init__(self, name, length, scale = 1, signed = False):
        super().__init__(name, length)
        self.scale = scale
        self.signed = signed

    def decode(self, data):
        value = int.from_bytes(data, 'big', signed = self.signed)
        return value * self.scale

    def encode(self, value):
        if self.contains(value):
            value = int(value // self.scale)
            return (value.to_bytes((self.length + 7) // 8, byteorder='big', signed=self.signed), self.length)

    def contains(self, value):
        if type(value) != int and type(value) != float:
            raise ValueError(f"'{value}' is not a number")
        value = int(value // self.scale)
        hex_value = hex(value)
        if not self.signed:
            if value >= 1 << self.length:
                raise ValueError(f"Value {value} ({hex_value}) is too large for {self.length} unsigned bits.")
            if value < 0:
                raise ValueError(f"Cannot encode negative value {value} in unsigned field.")
        else:
            if value >= 1 << (self.length - 1):
                raise ValueError(f"Value {value} ({hex_value}) is too large for {self.length} signed bits.")
            if value < -1 << (self.length - 1):
                raise ValueError(f"Value {value} ({hex_value}) is too small for {self.length} signed bits.")
        return True

class Switch(Field):
    """
    Wrapper for enums that maps enum keys to another dictionary (to avoid code redudancy)
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
        pass

    def get_fields(self, data):
        return self.map_key_enum[self.enum.decode(data)]
