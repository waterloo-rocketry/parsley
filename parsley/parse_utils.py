def hexify(data: bytes):
    value = int.from_bytes(data, byteorder='big')
    hex_str = f'0x{value:X}' # uppercase hexadecimal
    return hex_str

def hexify_msg_sid(data: bytes, is_msg_type=False):
    value = int.from_bytes(data, byteorder='big')
    if is_msg_type: # convert the 6-bit msg_type into its 12-bit form
        value = value << 5
    hex_str = f'0x{value:03X}' # front-padded uppercase hexadecimal
    return hex_str
