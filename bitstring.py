import constants

class BitString:
    """
    Stores the message data bits that we have yet to parse and lets us read
    arbitrary-length bits from the front. We need to operate at the bit level since some fields
    are non-byte-aligned (eg. DEBUG_MSG's 4-bit DEBUG_LEVEL and DEBUG_MSG's 12-bit LINE_NUM)
    """
    def __init__(self, data=b''):
        self.length = len(data) * 8 # length in bits
        # store the data as an int which is unbounded and lets us do bitwise manipulations
        self.data = int.from_bytes(data, byteorder=constants.BYTE_ORDER)

    def pop(self, field_length) -> bytes:
        """
        Returns the next field_length bits of data as a bytes object.

        The data returned will be LSB-aligned, so for example, asking for 12 bits will return:
        0000BBBB BBBBBBBB
        where B represents a data bit.
        """
        if self.length < field_length:
            raise IndexError
        self.length -= field_length
        res = self.data >> (self.length) # extract the field_length most significant bits
        self.data = self.data & ((1 << self.length) - 1) # and then mask them out
        return res.to_bytes((field_length + 7) // 8, byteorder=constants.BYTE_ORDER) # and convert to a bytes object

    def push(self, value, field_length):
        """
        Appends the next field_length bits of data from value.

        The data appended will be LSB-aligned, so for example, appending 6 bits from:
        10110000
        will append only 110000
        """
        self.length += field_length
        value = int.from_bytes(value, byteorder=constants.BYTE_ORDER)
        value = value & ((1 << field_length) -1) # extract the field_length least significant bits
        self.data = (self.data << field_length) | value # and then append to data
