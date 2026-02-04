import crc8
from typing import Any
import struct
from parsley.bitstring import BitString
from parsley.fields import Field, Switch, Bitfield
from parsley.message_definitions import CAN_MESSAGE, MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import parsley.message_types as mt
import parsley.parse_utils as pu
from deprecated import deprecated
from parsley.parse_to_object import _ParsleyParseInternal 
from parsley.parsley_message import ParsleyError

@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.parse_fields in parsley.parse_to_object (or whichever object the data is supposed to become)")
def parse_fields(bit_str: BitString, fields: list[Field]) -> dict[str, Any]:
    """
    Parses binary data stored in a BitString and decodes the data
    based on each field's decode() implementation. Returns a dictionary
    of each field's name to its decoded python value.
    """
    return _ParsleyParseInternal.parse_fields(bit_str, fields)

@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.parse_to_object in parsley.parse_to_object (or whichever object the data is supposed to become)")
def parse(msg_sid: bytes, msg_data: bytes) -> dict:
    """
    Extracts the message_type and board_id from msg_sid to construct a CAN message along with message_data.
    Upon reading poorly formatted data, the error is caught and returned in the dictionary.
    """

    result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
    
    if isinstance(result, ParsleyError):
        return {
            'board_type_id': result.board_type_id,
            'board_inst_id': result.board_inst_id,
            'msg_type': result.msg_type,
            'data': {
                'msg_data': result.msg_data,
                'error': result.error
            }
        }
    else:
        return result.model_dump(mode='json')

@deprecated(version='2026.2', reason="Deprecated; use BitstringParser.parse in the new BitstringParser object")
def parse_bitstring(bit_str: BitString) -> tuple[bytes, bytes]:
    msg_sid = int.from_bytes(bit_str.pop(MESSAGE_SID.length), byteorder='big')
    msg_data = [byte for byte in bit_str.pop(bit_str.length)]
    return format_can_message(msg_sid, list(msg_data))

@deprecated(version='2026.2', reason="Deprecated; use LiveTelemetryParser.parse in the new LiveTelemetryParser object")
def parse_live_telemetry(frame: bytes) -> tuple[bytes, bytes] | None:
    if len(frame) < 7:   raise ValueError("Incorrect frame length")
    if frame[0] != 0x02: raise ValueError("Incorrect frame header")

    frame_len = frame[1]
    msg_sid = int.from_bytes(bytes([frame[2] & 0x1F]) + frame[3:6], byteorder='big')
    msg_data = frame[6:frame_len-1]
    exp_crc = frame[frame_len-1]
    msg_crc = crc8.crc8(frame[:frame_len-1]).digest()[0]

    if msg_crc != exp_crc:
        raise ValueError(f'Bad checksum, expected {exp_crc:02X} but got {msg_crc:02X}')

    return format_can_message(msg_sid, list(msg_data))

@deprecated(version='2026.2', reason="Deprecated; use USBDebugParser.parse in the new USBDebugParser object")
def parse_usb_debug(line: str) -> tuple[bytes, bytes] | None:
    line = line.strip(' \0\r\n')
    if len(line) == 0 or line[0] != '$':
        raise ValueError("Incorrect line format")
    line = line[1:]

    if ':' in line:
        msg_sid, msg_data = line.split(':')
        msg_sid = int(msg_sid, 16)
        msg_data = [int(byte, 16) for byte in msg_data.split(',')]
    else:
        msg_sid = int(line, 16)
        msg_data = []

    return format_can_message(msg_sid, msg_data)

@deprecated(version='2026.2', reason="Deprecated; use LoggerParser.parse in the new LoggerParser object")
def parse_logger(buf: bytes, page_number: int) -> tuple[bytes, bytes] | None:
    """
    Parse one logger record.

    Layout  (little-endian unless stated):
        0  - 2  : ASCII 'L','O','G'
        3       : page number (uint8)
        4  - 12 : SID (uint32 LE) | timestamp (uint32 LE) | DLC (uint8)
        13 - .. : up to 8 bytes CAN payload
        -- ff-padding may follow, removed before parsing --

    Returns whatever `format_can_message()` returns.
    Raises ValueError on any structural problem.
    """

    LOG_MAGIC = b"LOG"          # ASCII “LOG” = 0x4c4f47
    HEADER_FMT = "<IIB"         # SID(uint32 LE), timestamp(uint32 LE), DLC(uint8)
    HEADER_LEN = struct.calcsize(HEADER_FMT)   # == 9

    # Strip the buffer to 4096 bytes, as required by the logger.
    if len(buf) != 4096:
        raise ValueError("Logger message must be exactly 4096 bytes")

    if not buf.startswith(LOG_MAGIC):
        raise ValueError("Missing 'LOG' signature")

    if buf[3] != page_number % 256:
        raise ValueError(f"Page number mismatch: expected {page_number % 256}, got {buf[3]}")
    
    offset = 4 # start of the header

    while (4096 - offset > HEADER_LEN): # at least one message
        sid, _, dlc = struct.unpack_from(HEADER_FMT, buf, offset)

        if sid & 0xE000_0000:
            break

        if not 0 <= dlc <= 8:
            raise ValueError(f"DLC out of range (0-8), got {dlc}")

        offset += HEADER_LEN

        data: list[int] = list(buf[offset: offset + dlc])

        offset += dlc

        yield format_can_message(sid, data)

# our three parsing functions create ints, but after the rewrite, they should return bytes
@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.format_can_message in parsley.parse_to_object (or whichever object the data is supposed to become)")
def format_can_message(msg_sid: int, msg_data: list[int]) -> tuple[bytes, bytes]:
    return _ParsleyParseInternal.format_can_message(msg_sid, msg_data)

# given a dictionary of CAN message data, return the CAN message bits
@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.encode_data in parsley.parse_to_object (or whichever object the data is supposed to become)")
def encode_data(parsed_data: dict) -> tuple[int, list[int]]:
    return _ParsleyParseInternal.encode_data(parsed_data)

MSG_PRIO_LEN = max([len(msg_prio) for msg_prio in mt.msg_prio])
MSG_TYPE_LEN = max([len(msg_type) for msg_type in mt.msg_type])
BOARD_TYPE_ID_LEN = max([len(board_type_id) for board_type_id in mt.board_type_id])
BOARD_INST_ID_LEN = max([len(board_inst_id) for board_inst_id in mt.board_inst_id])

# formats a parsed CAN message (dictionary) into a singular line
@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.format_line in parsley.parse_to_object (or whichever object the data is supposed to become)")
def format_line(parsed_data: dict) -> str:
    return _ParsleyParseInternal.format_line(parsed_data)

# can_message is an array of parsley fields
@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.calculate_msg_bit_len in parsley.parse_to_object (or whichever object the data is supposed to become)")
def calculate_msg_bit_len(can_message):
    return _ParsleyParseInternal.calculate_msg_bit_len(can_message)
