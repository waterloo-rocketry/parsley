import pytest

import constants

FLOAT_TOLERANCE = 0.01

def approx(value):
    return pytest.approx(value, FLOAT_TOLERANCE)

def create_msg_sid_from_bytes(msg_type, board_id):
    msg_type_int = int.from_bytes(msg_type, byteorder=constants.BYTE_ORDER)
    board_id_int = int.from_bytes(board_id, byteorder=constants.BYTE_ORDER)
    msg_sid_int = msg_type_int | board_id_int
    msg_sid = msg_sid_int.to_bytes(2, byteorder=constants.BYTE_ORDER)
    return msg_sid
