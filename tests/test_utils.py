import pytest

# changing the import structure in this file because I want people to be able
# to run the README snippet (our test suite appends to pythonpath)
from parsley import (
    BitString,
    MESSAGE_TYPE, BOARD_ID, MSG_SID
)

FLOAT_TOLERANCE = 0.01

def approx(value):
    return pytest.approx(value, FLOAT_TOLERANCE)

def create_msg_sid_from_strings(msg_type_str, board_id_str):
    (msg_type_bits, _) = MESSAGE_TYPE.encode(msg_type_str)
    (board_id_bits, _) = BOARD_ID.encode(board_id_str)
    bit_msg_sid = BitString(msg_type_bits, MESSAGE_TYPE.length)
    bit_msg_sid.push(board_id_bits, BOARD_ID.length)
    msg_sid = bit_msg_sid.pop(MSG_SID.length)
    return msg_sid
