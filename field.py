class Field:
    """
    Abstract base class for a field in a message.
    """
    def __init__(self, name, length, optional=False):
        self.name = name
        self.length = length # length in bits
        self.optional = optional

    def decode(self, data):
        """
        Convert self.length bits of data (returned in the format given by BitString.pop)
        to the corresponding python value of the field. This value could be a number, string,
        etc. depending on the specific field type.
        """
        raise NotImplementedError

    def encode(self, value):
        """
        Convert value to self.length bits of data (in an LSB-aligned bytes object) to
        build a message. Returns a tuple of (data, len_of_data_in_bits). Raise a ValueError with
        an appropiate message if this is not possible.
        """
        raise NotImplementedError

    def contains(self, value):
        """
        Used to check whether a certain value is contained within the range of the field.
        """
        raise NotImplementedError