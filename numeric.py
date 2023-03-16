from field import Field

class Numeric(Field):
    def __init__(self, name, length, scale = 1, signed = False):
        super().__init__(name, length)
        self.scale = scale
        self.signed = signed

    def decode(self, data):
        val = int.from_bytes(data, 'big', signed = self.signed)
        return int(val * self.scale)

    def encode(self, value):
        value *= 1/self.scale # doing //= self.scale sometimes fogs up the data after decode
        value = int(value)
        if self.contains(value):
            return value.to_bytes((self.length + 7) // 8, byteorder='big', signed=self.signed)

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

