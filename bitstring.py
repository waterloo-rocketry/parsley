class BitString:
    """
    Store the bits of the message data that we have yet to parse and let us chop off
    arbitrary-length sections from the front. We need to operate at the bit level since some
    fields don't take up a whole byte (eg. DEBUG_MSG's DEBUG_LEVEL) and some fields are split
    weirdly across bytes (eg. DEBUG_MSG's LINUM, a 12-bit value).
    """
    def __init__(self, data=b''):
        self.length = len(data) * 8 # length in bits
        # store the data as an int (in python ints are unbounded and this lets us do bitwise manipulations)
        self.data = int.from_bytes(data, 'big')

    def pop(self, field_length) -> bytes:
        """
        Returns the next field_length bits of data as a bytes object.

        The data will be LSB-aligned, so for example asking for 12 bits will return:
        0000BBBB BBBBBBBB
        where B represents a data bit.
        """
        if self.length < field_length:
            raise IndexError
        self.length -= field_length
        res = self.data >> (self.length) # extract the field_length most significant bits
        self.data = self.data & ((1 << self.length) - 1) # and then mask them out
        return res.to_bytes((field_length + 7) // 8, 'big') # and convert to a bytes object

    def push(self, data):
        (value, field_length) = data
        """
        Appends arbitrary sized bits.
        """
        self.length += field_length
        value = int.from_bytes(value, 'big')
        self.data = (self.data << field_length) | (value & ((1 << field_length) - 1))

    def __str__(self):
        return hex(self.data)
