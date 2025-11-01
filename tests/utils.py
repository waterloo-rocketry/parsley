import pytest

from parsley.bitstring import BitString
from parsley.message_definitions import MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID, MESSAGE_PRIO

FLOAT_TOLERANCE = 0.01

def approx(value):
    """
    Create a pytest.approx comparator configured with the module float tolerance.
    
    Parameters:
        value: The reference numeric value to compare against.
    
    Returns:
        A `pytest.approx` object that compares values to `value` within `FLOAT_TOLERANCE`.
    """
    return pytest.approx(value, FLOAT_TOLERANCE)

def create_msg_sid_from_strings(priority_str: str, msg_type_str: str, reserved_str: str, board_type_str: str, board_inst_str: str):
    """
    Constructs a message SID by encoding and packing the provided component fields into a bit-level identifier.
    
    Each input string is encoded to its field bit representation and concatenated in order: priority, message type, reserved (two zero bytes), board type, and board instance.
    
    Parameters:
        priority_str (str): Priority field value as a string.
        msg_type_str (str): Message type field value as a string.
        reserved_str (str): Reserved field value (ignored; reserved bits are set to zero).
        board_type_str (str): Board type identifier as a string.
        board_inst_str (str): Board instance identifier as a string.
    
    Returns:
        bytes: The assembled message SID as a byte sequence representing MESSAGE_SID.length bits.
    """
    (msg_prio_bits, _) = MESSAGE_PRIO.encode(priority_str)
    (msg_type_bits, _) = MESSAGE_TYPE.encode(msg_type_str)
    (reserved_bits, _) = bytes([0, 0]), 2 # reserved bits are always 0
    (board_type_bits, _) = BOARD_TYPE_ID.encode(board_type_str)
    (board_inst_bits, _) = BOARD_INST_ID.encode(board_inst_str)
    
    bit_msg_sid = BitString(msg_prio_bits, MESSAGE_PRIO.length)
    bit_msg_sid.push(msg_type_bits, MESSAGE_TYPE.length)
    bit_msg_sid.push(reserved_bits, 2)
    bit_msg_sid.push(board_type_bits, BOARD_TYPE_ID.length)
    bit_msg_sid.push(board_inst_bits, BOARD_INST_ID.length)
    msg_sid = bit_msg_sid.pop(MESSAGE_SID.length)
    return msg_sid