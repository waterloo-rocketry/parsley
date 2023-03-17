from field import Field

class ASCII(Field):
    def __init__(self, name, length, optional=False):
        super().__init__(name, length, optional)

    def decode(self, data):
        return data.replace(b'\x00', b'').decode('ascii')
    
    def encode(self, value):
        if self.contains(value):
            data = value.encode('ascii')
            filler_data = b'\x00' * (self.length - len(data))
            if self.optional:
                data = filler_data + data
            return (data, self.length)

    def contains(self, value):
        if not type(value) == str:
            raise ValueError(f"'{value}' is not a valid string")
        if self.length < len(value):
            raise ValueError(f"String '{value}' is too large for {self.length} characters")
        if not value.isascii():
            raise ValueError(f"String '{value}' contains non-ascii characters")
        return True