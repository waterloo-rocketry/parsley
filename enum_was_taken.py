from field import Field

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
    