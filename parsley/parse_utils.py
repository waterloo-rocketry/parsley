def hexify(data: bytes):
    """
    Formats byte strings into hexadecimal strings.

    For perspective, printing the byte string b'\x12\x34\x42' is b'\x124B' since
    \x34 and \x42 represent the ASCII character '4' and 'B' respectively, which can be misleading.
    hexify() will instead return '0x123442' which visually is much more intuitive.
    """
    value = int.from_bytes(data, byteorder='big')
    hex_str = f'0x{value:X}' # uppercase hexadecimal
    return hex_str

def hexify_msg_sid(data: bytes, is_msg_type=False):
    value = int.from_bytes(data, byteorder='big')
    if is_msg_type: # convert the 6-bit msg_type into its 12-bit canlib form
        value = value << 5
    hex_str = f'0x{value:03X}' # front-padded uppercase hexadecimal
    return hex_str
