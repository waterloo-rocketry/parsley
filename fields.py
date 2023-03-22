from field import Field

class ASCII(Field):
    def __init__(self, name, length, optional=False):
        super().__init__(name, length, optional)

    def decode(self, data):
        return data.replace(b'\x00', b'').decode('ascii')
    
    def encode(self, value):
        if self.contains(value):
            data = value.encode('ascii')
            return (data, self.length)

    def contains(self, value):
        if not type(value) == str:
            raise ValueError(f"'{value}' is not a string object")
        if not value.isascii():
            raise ValueError(f"String '{value}' contains non-ascii character(s)")
        if self.length < 8*len(value.encode('ascii')):
            raise ValueError(f"String '{value}' is too large for {self.length//8} character(s)")
        return True
    
class Enum(Field):
    def __init__(self, name, length, map_val_num):
        super().__init__(name, length)

        for k, v in map_val_num.items():
            if v < 0:
                raise ValueError(f"Mapping for key {k} should not be negative.")
            if v >= 1 << self.length:
                raise ValueError(f"Mapping for key {k} is too large to fit in {self.length} bits.")

        self.map_val_num = map_val_num
        self.map_num_val = {v: k for k, v in self.map_val_num.items()}

    def decode(self, data):
        num = int.from_bytes(data, 'big', signed=False)
        return self.map_num_val[num]

    def encode(self, value):
        if self.contains(value):
            return (self.map_val_num[value].to_bytes((self.length + 7) // 8, 'big'), self.length)
    
    def contains(self, value):
        if value not in self.map_val_num:
            raise ValueError(f"Value '{value}' not in mapping.")
        return True
    
class Numeric(Field):
    def __init__(self, name, length, scale = 1, signed = False):
        super().__init__(name, length)
        self.scale = scale
        self.signed = signed

    def decode(self, data):
        val = int.from_bytes(data, 'big', signed = self.signed)
        return val * self.scale

    def encode(self, value):
        value = int(value // self.scale)
        if self.contains(value):
            return (value.to_bytes((self.length + 7) // 8, byteorder='big', signed=self.signed), self.length)

    def contains(self, value):
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
    def __init__(self, enum, map_str_enum):
        super().__init__(enum.name, enum.length)
        self.enum = enum
        self.map_str_enum = map_str_enum
        self.name = enum.name
        self.length = enum.length

    def decode(self, data):
        #TODO:  add an error checking thing here
        return self.enum.decode(data)

    def encode(self, field):
        # TODO: add a message saying this is not possible instead of just saying pass
        pass
    
    def contains(self, value):
        pass

    def get_fields(self, data):
        return self.map_str_enum[self.enum.decode(data)]
