from field import Field

class Ascii(Field):
    def __init__(self, name, length):
        super().__init__(name, length)

    def decode(self, data):
        return data.decode('ascii')
    
    def encode(self, value):
        if self.contains(value):
            return value.encode('ascii')

    def contains(self, value):
        if not type(value) == str:
            raise ValueError(f"'{value}' is not a valid string")
        if self.length < len(value):
            raise ValueError(f"String '{value}' is too large for {self.length} characters")
        if not value.isascii():
            raise ValueError(f"String '{value}' contains non-ascii characters")
        return True