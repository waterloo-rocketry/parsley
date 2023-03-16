from field import Field

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
        pass
    
    def contains(self, value):
        pass

    def get_fields(self, data):
        return self.map_str_enum[self.enum.decode(data)]
