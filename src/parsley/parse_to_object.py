"""Parser classes for CAN message input formats."""

from __future__ import annotations

from abc import ABC, abstractmethod
import struct
from typing import Generator

import crc8

from parsley.bitstring import BitString
from parsley.fields import Enum, Numeric, Field
from parsley.parsley_message import ParsleyObject, ParsleyError
from parsley.payloads import ParsleyDataPayload, get_payload_type
import parsley.message_types as mt
import parsley.parse_utils as pu


# ── SID-level field constants (private) ────────────────────────────────────

_MESSAGE_PRIO = Enum('msg_prio', 2, mt.msg_prio)
_MESSAGE_TYPE = Enum('msg_type', 7, mt.msg_type)
_BOARD_TYPE_ID = Enum('board_type_id', 6, mt.board_type_id)
_BOARD_INST_ID = Enum('board_inst_id', 6, mt.board_inst_id)
_MESSAGE_METADATA = Numeric('msg_metadata', 8)
_MESSAGE_SID = Enum(
    'msg_sid',
    _MESSAGE_PRIO.length + _MESSAGE_TYPE.length + _BOARD_TYPE_ID.length
    + _BOARD_INST_ID.length + _MESSAGE_METADATA.length,
    {},
)

# Used for formatting lines
_MSG_PRIO_LEN = max(len(p) for p in mt.msg_prio)
_MSG_TYPE_LEN = max(len(t) for t in mt.msg_type)
_BOARD_TYPE_ID_LEN = max(len(b) for b in mt.board_type_id)
_BOARD_INST_ID_LEN = max(len(b) for b in mt.board_inst_id)


class _ParsleyParseInternal:
    def __init__(self) -> None:
        raise NotImplementedError("This class is static only do not instantiate it")

    @staticmethod
    def parse_fields(bit_str: BitString, fields: list[Field]) -> dict[str, object]:
        """Parse binary data stored in a BitString using the given fields."""
        res: dict[str, object] = {}
        for field in fields:
            data = bit_str.pop(field.length, field.variable_length)
            res[field.name] = field.decode(data)
        return res

    @staticmethod
    def format_line(parsed_data: dict[str, object]) -> str:
        msg_prio = parsed_data['msg_prio']
        msg_type = parsed_data['msg_type']
        board_type_id = parsed_data['board_type_id']
        board_inst_id = parsed_data['board_inst_id']
        data = parsed_data['data']
        res = (
            f'[ {msg_prio:<{_MSG_PRIO_LEN}} {msg_type:<{_MSG_TYPE_LEN}}'
            f' {board_type_id:<{_BOARD_TYPE_ID_LEN}} {board_inst_id:<{_BOARD_INST_ID_LEN}} ]'
        )
        if isinstance(data, dict):
            for k, v in data.items():
                formatted_value = f"{v:.3f}" if isinstance(v, float) else v
                res += f' {k}: {formatted_value}'
        elif isinstance(data, ParsleyDataPayload):
            for k, v in data.to_dict().items():
                formatted_value = f"{v:.3f}" if isinstance(v, float) else v
                res += f' {k}: {formatted_value}'
        return res

    @staticmethod
    def calculate_msg_bit_len(can_message: list[Field]) -> int:
        bit_len = 0
        for field in can_message:
            bit_len += field.length
        return bit_len

    @staticmethod
    def encode_data(parsed_data: dict[str, object]) -> tuple[int, list[int]]:
        msg_prio = parsed_data['msg_prio']
        msg_type = parsed_data['msg_type']
        board_type_id = parsed_data['board_type_id']
        board_inst_id = parsed_data['board_inst_id']
        msg_metadata = parsed_data['msg_metadata']

        bit_str = BitString()
        bit_str.push(*_MESSAGE_PRIO.encode(msg_prio))
        bit_str.push(*_MESSAGE_TYPE.encode(msg_type))
        bit_str.push(*_BOARD_TYPE_ID.encode(board_type_id))
        bit_str.push(*_BOARD_INST_ID.encode(board_inst_id))
        bit_str.push(*_MESSAGE_METADATA.encode(msg_metadata))
        msg_sid = int.from_bytes(bit_str.pop(bit_str.length), byteorder='big')

        payload_cls = get_payload_type(str(msg_type))
        if payload_cls is not None:
            for field in payload_cls.FIELDS:
                bit_str.push(*field.encode(parsed_data[field.name]))
        msg_data = list(bit_str.pop(bit_str.length))
        return msg_sid, msg_data

    @staticmethod
    def format_can_message(msg_sid: int, msg_data: list[int]) -> tuple[bytes, bytes]:
        msg_sid_length = (msg_sid.bit_length() + 7) // 8
        formatted_msg_sid = msg_sid.to_bytes(msg_sid_length, byteorder='big')
        formatted_msg_data = bytes(msg_data)
        return formatted_msg_sid, formatted_msg_data

    @staticmethod
    def parse_board_type_id(encoded_board_type_id: bytes) -> str:
        try:
            return _BOARD_TYPE_ID.decode(encoded_board_type_id)
        except ValueError:
            return pu.hexify(encoded_board_type_id)

    @staticmethod
    def parse_board_inst_id(encoded_board_inst_id: bytes) -> str:
        try:
            return _BOARD_INST_ID.decode(encoded_board_inst_id)
        except ValueError:
            return pu.hexify(encoded_board_inst_id)

    @staticmethod
    def parse_msg_metadata(encoded_msg_metadata: bytes) -> int:
        return _MESSAGE_METADATA.decode(encoded_msg_metadata)

    @staticmethod
    def parse_to_object(msg_sid: bytes | int, msg_data: bytes | list[int]) -> ParsleyObject | ParsleyError:
        """Extract msg_type and board_id from msg_sid to construct a ParsleyObject.

        Returns ParsleyError on malformed data.
        """
        if isinstance(msg_sid, int):
            sid_bytes, data_bytes = _ParsleyParseInternal.format_can_message(msg_sid, list(msg_data))
            msg_sid = sid_bytes
            msg_data = data_bytes

        bit_str_msg_sid = BitString(msg_sid, _MESSAGE_SID.length)
        encoded_msg_prio = bit_str_msg_sid.pop(_MESSAGE_PRIO.length)
        encoded_msg_type = bit_str_msg_sid.pop(_MESSAGE_TYPE.length)
        encoded_board_type_id = bit_str_msg_sid.pop(_BOARD_TYPE_ID.length)
        encoded_board_inst_id = bit_str_msg_sid.pop(_BOARD_INST_ID.length)
        encoded_msg_metadata = bit_str_msg_sid.pop(_MESSAGE_METADATA.length)

        board_type_id = _ParsleyParseInternal.parse_board_type_id(encoded_board_type_id)
        board_inst_id = _ParsleyParseInternal.parse_board_inst_id(encoded_board_inst_id)
        msg_metadata = _ParsleyParseInternal.parse_msg_metadata(encoded_msg_metadata)

        try:
            msg_prio: str = _MESSAGE_PRIO.decode(encoded_msg_prio)
            msg_type: str = _MESSAGE_TYPE.decode(encoded_msg_type)
            payload_cls = get_payload_type(msg_type)
            data: ParsleyDataPayload | None = payload_cls.from_bitstring(BitString(msg_data)) if payload_cls else None
        except (ValueError, IndexError, KeyError) as error:
            return ParsleyError(
                board_type_id=board_type_id,
                board_inst_id=board_inst_id,
                msg_type=pu.hexify(encoded_msg_type, is_msg_type=True),
                msg_metadata=msg_metadata,
                msg_data=pu.hexify(msg_data),
                error=f"error: {error}",
            )

        return ParsleyObject(
            msg_prio=msg_prio,
            msg_type=msg_type,
            board_type_id=board_type_id,
            board_inst_id=board_inst_id,
            msg_metadata=msg_metadata,
            data=data,
        )


class ParsleyParser(ABC):
    """Abstract base for different input-format parsers."""

    @abstractmethod
    def parse(self, *args: object, **kwargs: object) -> object:
        raise NotImplementedError("This class is an abstract class")


class USBDebugParser(ParsleyParser):
    """Parse ASCII USB-debug lines."""

    def parse(self, line: str) -> ParsleyObject | ParsleyError:
        line = line.strip(' \0\r\n')
        if len(line) == 0 or line[0] != '$':
            raise ValueError('Incorrect line format')
        line = line[1:]

        if ':' in line:
            msg_sid_str, msg_data_str = line.split(':')
            msg_sid_int = int(msg_sid_str, 16)
            msg_data_list = [int(byte, 16) for byte in msg_data_str.split(',')]
        else:
            msg_sid_int = int(line, 16)
            msg_data_list: list[int] = []

        return _ParsleyParseInternal.parse_to_object(msg_sid_int, msg_data_list)


class LiveTelemetryParser(ParsleyParser):
    """Parse binary live-telemetry frames."""

    def parse(self, frame: bytes) -> ParsleyObject | ParsleyError:
        if len(frame) < 7:
            raise ValueError('Incorrect frame length')
        if frame[0] != 0x02:
            raise ValueError('Incorrect frame header')

        frame_len = frame[1]
        msg_sid = int.from_bytes(bytes([frame[2] & 0x1F]) + frame[3:6], byteorder='big')
        msg_data = frame[6:frame_len - 1]
        exp_crc = frame[frame_len - 1]
        msg_crc = crc8.crc8(frame[:frame_len - 1]).digest()[0]

        if msg_crc != exp_crc:
            raise ValueError(f'Bad checksum, expected {exp_crc:02X} but got {msg_crc:02X}')

        return _ParsleyParseInternal.parse_to_object(msg_sid, list(msg_data))


class LoggerParser(ParsleyParser):
    """Parses logger pages and yields ParsleyObject items.

    Layout (little-endian unless stated):
        0  - 2  : ASCII 'L','O','G'
        3       : page number (uint8)
        4  - 12 : SID (uint32 LE) | timestamp (uint32 LE) | DLC (uint8)
        13 - .. : up to 8 bytes CAN payload
        -- ff-padding may follow, removed before parsing --
    """

    LOG_MAGIC = b'LOG'
    HEADER_FMT = '<IIB'
    HEADER_LEN = struct.calcsize(HEADER_FMT)  # == 9
    PARSE_LOGGER_PAGE_SIZE = 4096

    def parse(self, buf: bytes, page_number: int) -> Generator[ParsleyObject | ParsleyError, None, None]:
        if len(buf) != self.PARSE_LOGGER_PAGE_SIZE:
            raise ValueError('Logger message must be exactly 4096 bytes')

        if not buf.startswith(self.LOG_MAGIC):
            raise ValueError("Missing 'LOG' signature")

        if buf[3] != page_number % 256:
            raise ValueError(f'Page number mismatch: expected {page_number % 256}, got {buf[3]}')

        offset = 4

        while self.PARSE_LOGGER_PAGE_SIZE - offset > self.HEADER_LEN:
            sid, _, dlc = struct.unpack_from(self.HEADER_FMT, buf, offset)

            if sid & 0xE000_0000:
                break

            if not 0 <= dlc <= 8:
                raise ValueError(f'DLC out of range (0-8), got {dlc}')

            offset += self.HEADER_LEN
            data_list: list[int] = list(buf[offset: offset + dlc])
            offset += dlc

            yield _ParsleyParseInternal.parse_to_object(sid, data_list)


class BitstringParser(ParsleyParser):
    """Parse BitString objects."""

    def parse(self, bit_str: BitString) -> ParsleyObject | ParsleyError:
        msg_sid = int.from_bytes(bit_str.pop(_MESSAGE_SID.length), byteorder='big')
        msg_data = list(bit_str.pop(bit_str.length))
        return _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
