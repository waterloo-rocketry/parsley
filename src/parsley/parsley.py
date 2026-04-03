from __future__ import annotations

import crc8
from typing import Any, Generator
import struct
from parsley.bitstring import BitString
from parsley.fields import Field
from deprecated import deprecated
from parsley.parse_to_object import _ParsleyParseInternal
from parsley.parsley_message import ParsleyError


@deprecated(version='2026.2', reason="Deprecated; use a ParsleyParser subclass (USBDebugParser, LiveTelemetryParser, LoggerParser, BitstringParser) from parsley.parse_to_object")
def parse_fields(bit_str: BitString, fields: list[Field]) -> dict[str, Any]:
    """Parse binary data stored in a BitString."""
    return _ParsleyParseInternal.parse_fields(bit_str, fields)


@deprecated(version='2026.2', reason="Deprecated; use a ParsleyParser subclass from parsley.parse_to_object")
def parse(msg_sid: bytes, msg_data: bytes) -> dict[str, Any]:
    """Parse msg_sid and msg_data into a CAN message dict."""
    result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)

    if isinstance(result, ParsleyError):
        return {
            'board_type_id': result.board_type_id,
            'board_inst_id': result.board_inst_id,
            'msg_type': result.msg_type,
            'data': {
                'msg_data': result.msg_data,
                'error': result.error,
            },
        }
    else:
        return result.model_dump(mode='json')


@deprecated(version='2026.2', reason="Deprecated; use BitstringParser.parse")
def parse_bitstring(bit_str: BitString) -> tuple[bytes, bytes]:
    from parsley.parse_to_object import _MESSAGE_SID
    msg_sid = int.from_bytes(bit_str.pop(_MESSAGE_SID.length), byteorder='big')
    msg_data = list(bit_str.pop(bit_str.length))
    return format_can_message(msg_sid, msg_data)


@deprecated(version='2026.2', reason="Deprecated; use LiveTelemetryParser.parse")
def parse_live_telemetry(frame: bytes) -> tuple[bytes, bytes] | None:
    if len(frame) < 7:
        raise ValueError("Incorrect frame length")
    if frame[0] != 0x02:
        raise ValueError("Incorrect frame header")

    frame_len = frame[1]
    msg_sid = int.from_bytes(bytes([frame[2] & 0x1F]) + frame[3:6], byteorder='big')
    msg_data = frame[6:frame_len - 1]
    exp_crc = frame[frame_len - 1]
    msg_crc = crc8.crc8(frame[:frame_len - 1]).digest()[0]

    if msg_crc != exp_crc:
        raise ValueError(f'Bad checksum, expected {exp_crc:02X} but got {msg_crc:02X}')

    return format_can_message(msg_sid, list(msg_data))


@deprecated(version='2026.2', reason="Deprecated; use USBDebugParser.parse")
def parse_usb_debug(line: str) -> tuple[bytes, bytes] | None:
    line = line.strip(' \0\r\n')
    if len(line) == 0 or line[0] != '$':
        raise ValueError("Incorrect line format")
    line = line[1:]

    if ':' in line:
        msg_sid_str, msg_data_str = line.split(':')
        msg_sid_int = int(msg_sid_str, 16)
        msg_data_list = [int(byte, 16) for byte in msg_data_str.split(',')]
    else:
        msg_sid_int = int(line, 16)
        msg_data_list: list[int] = []

    return format_can_message(msg_sid_int, msg_data_list)


@deprecated(version='2026.2', reason="Deprecated; use LoggerParser.parse")
def parse_logger(buf: bytes, page_number: int) -> Generator[tuple[bytes, bytes], None, None]:
    """Parse one logger page."""
    LOG_MAGIC = b"LOG"
    HEADER_FMT = "<IIB"
    HEADER_LEN = struct.calcsize(HEADER_FMT)

    if len(buf) != 4096:
        raise ValueError("Logger message must be exactly 4096 bytes")
    if not buf.startswith(LOG_MAGIC):
        raise ValueError("Missing 'LOG' signature")
    if buf[3] != page_number % 256:
        raise ValueError(f"Page number mismatch: expected {page_number % 256}, got {buf[3]}")

    offset = 4

    while 4096 - offset > HEADER_LEN:
        sid, _, dlc = struct.unpack_from(HEADER_FMT, buf, offset)

        if sid & 0xE000_0000:
            break

        if not 0 <= dlc <= 8:
            raise ValueError(f"DLC out of range (0-8), got {dlc}")

        offset += HEADER_LEN
        data: list[int] = list(buf[offset: offset + dlc])
        offset += dlc

        yield format_can_message(sid, data)


@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.format_can_message")
def format_can_message(msg_sid: int, msg_data: list[int]) -> tuple[bytes, bytes]:
    return _ParsleyParseInternal.format_can_message(msg_sid, msg_data)


@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.encode_data")
def encode_data(parsed_data: dict[str, Any]) -> tuple[int, list[int]]:
    return _ParsleyParseInternal.encode_data(parsed_data)


@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.format_line")
def format_line(parsed_data: dict[str, Any]) -> str:
    return _ParsleyParseInternal.format_line(parsed_data)


@deprecated(version='2026.2', reason="Deprecated; use _ParsleyParseInternal.calculate_msg_bit_len")
def calculate_msg_bit_len(can_message: list[Field]) -> int:
    return _ParsleyParseInternal.calculate_msg_bit_len(can_message)
