import pytest

from parsley.bitstring import BitString
from parsley.parse_to_object import (
    _MESSAGE_PRIO,
    _MESSAGE_TYPE,
    _BOARD_TYPE_ID,
    _BOARD_INST_ID,
    _MESSAGE_METADATA,
    _MESSAGE_SID,
)

FLOAT_TOLERANCE = 0.01

def approx(value):
    return pytest.approx(value, FLOAT_TOLERANCE)

def create_msg_sid_from_strings(priority_str: str, msg_type_str: str, metadata_str: str, board_type_str: str, board_inst_str: str):
    (msg_prio_bits, _) = _MESSAGE_PRIO.encode(priority_str)
    (msg_type_bits, _) = _MESSAGE_TYPE.encode(msg_type_str)
    (board_type_bits, _) = _BOARD_TYPE_ID.encode(board_type_str)
    (board_inst_bits, _) = _BOARD_INST_ID.encode(board_inst_str)
    (metadata_bits, _) = _MESSAGE_METADATA.encode(int(metadata_str) if metadata_str.isdigit() else 0)

    bit_msg_sid = BitString(msg_prio_bits, _MESSAGE_PRIO.length)
    bit_msg_sid.push(msg_type_bits, _MESSAGE_TYPE.length)
    bit_msg_sid.push(board_type_bits, _BOARD_TYPE_ID.length)
    bit_msg_sid.push(board_inst_bits, _BOARD_INST_ID.length)
    bit_msg_sid.push(metadata_bits, _MESSAGE_METADATA.length)
    msg_sid = bit_msg_sid.pop(_MESSAGE_SID.length)
    return msg_sid
