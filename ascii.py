from field import Field

class Ascii(Field):
    def __init__(self, name, length):
        super().__init__(name, length)

    def decode(self, data):
        return data.decode('ascii')
    
    def encode(self, value):
        if self.length < len(value):
            raise ValueError(f"String '{value}' is too large for {self.length} characters")
        if not value.isascii():
            raise UnicodeEncodeError(f"String '{value}' contains non-ascii characters")
        return value.encode('ascii')
