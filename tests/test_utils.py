import pytest

from parsley_definitions import MESSAGE_TYPE, BOARD_ID

FLOAT_TOLERANCE = 0.01

def approx(value):
    return pytest.approx(value, FLOAT_TOLERANCE)

def create_msg_sid_from_strings(msg_type_str, board_id_str):
    (msg_type_bits, _) = MESSAGE_TYPE.encode(msg_type_str)
    (board_id_bits, _) = BOARD_ID.encode(board_id_str)
    msg_type_int = int.from_bytes(msg_type_bits, byteorder='big', signed=False)
    board_id_int = int.from_bytes(board_id_bits, byteorder='big', signed=False)
    msg_sid_int = msg_type_int | board_id_int
    msg_sid = msg_sid_int.to_bytes(2, byteorder='big')
    return msg_sid
