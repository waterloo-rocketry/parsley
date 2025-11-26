'''
Contains the new static class implementation of Parsley.py
'''
from typing import Tuple, Union, List, TypeVar, Iterator
from parsley.parsley_message import ParsleyObject, ParsleyError
from parsley.bitstring import BitString
from parsley.message_definitions import CAN_MESSAGE, MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import parsley.parse_utils as pu
from parsley.fields import Field, Switch, Bitfield
from abc import ABC, abstractmethod
import struct
import crc8
import parsley.message_types as mt

T = TypeVar("T")
MSG_PRIO_LEN = max([len(msg_prio) for msg_prio in mt.msg_prio])
MSG_TYPE_LEN = max([len(msg_type) for msg_type in mt.msg_type])
BOARD_TYPE_ID_LEN = max([len(board_type_id) for board_type_id in mt.board_type_id])
BOARD_INST_ID_LEN = max([len(board_inst_id) for board_inst_id in mt.board_inst_id])

class _ParsleyParseInternal:
    def __init__(self):
        raise NotImplementedError("This class is static-only")

    @staticmethod
    def format_line(parsed_data: dict) -> str:
        msg_prio = parsed_data['msg_prio']
        msg_type = parsed_data['msg_type']
        board_type_id = parsed_data['board_type_id']
        board_inst_id = parsed_data['board_inst_id']
        data = parsed_data['data']
        res = f'[ {msg_prio:<{MSG_PRIO_LEN}} {msg_type:<{MSG_TYPE_LEN}} {board_type_id:<{BOARD_TYPE_ID_LEN}} {board_inst_id:<{BOARD_INST_ID_LEN}} ]'
        for k, v in data.items():
            formatted_value = f"{v:.3f}" if isinstance(v, float) else v
            res += f' {k}: {formatted_value}'
        return res

    @staticmethod
    def calculate_msg_bit_len(can_message):
        bit_len = 0
        for field in can_message:
            bit_len += field.length
        return bit_len

    @staticmethod
    def encode_data(parsed_data: dict) -> Tuple[int, List[int]]:
        msg_prio = parsed_data['msg_prio']
        msg_type = parsed_data['msg_type']
        board_type_id = parsed_data['board_type_id']
        board_inst_id = parsed_data['board_inst_id']

        bit_str = BitString()
        bit_str.push(*MESSAGE_PRIO.encode(msg_prio))
        bit_str.push(*MESSAGE_TYPE.encode(msg_type))
        bit_str.push(bytes([0, 0]), 2)
        bit_str.push(*BOARD_TYPE_ID.encode(board_type_id))
        bit_str.push(*BOARD_INST_ID.encode(board_inst_id))
        msg_sid = int.from_bytes(bit_str.pop(bit_str.length), byteorder='big')

        # skip the first field (board_id) since thats parsed separately
        for field in CAN_MESSAGE.get_fields(msg_type)[3:]:
            bit_str.push(*field.encode(parsed_data[field.name]))
        msg_data = [byte for byte in bit_str.pop(bit_str.length)]
        return msg_sid, msg_data

    @staticmethod
    def _parse_fields(bit_str: BitString, fields: List[Field]) -> dict[str, T]:
        """
        Parses binary data stored in a BitString and decodes the data
        based on each field's decode() implementation. Returns a dictionary
        of each field's name to its decoded python value.
        """
        res: dict[str, T] = {}
        for field in fields:
            data = bit_str.pop(field.length, field.variable_length)
            res[field.name] = field.decode(data)
            if isinstance(field, Switch):
                nested_fields = field.get_fields(res[field.name])
                res.update(_ParsleyParseInternal._parse_fields(bit_str, nested_fields))
            if isinstance(field, Bitfield):
                res[field.name] = field.decode(data)
        return res

    @staticmethod
    def _format_can_message(msg_sid: int, msg_data: List[int]) -> Union[Tuple[bytes, bytes], None]:
        msg_sid_length = (msg_sid.bit_length() + 7) // 8
        formatted_msg_sid = msg_sid.to_bytes(msg_sid_length, byteorder='big')
        formatted_msg_data = bytes(msg_data)
        return formatted_msg_sid, formatted_msg_data

    @staticmethod
    def _parse_board_type_id(encoded_board_type_id: bytes) -> dict:
        board_type_id = None
        try:
            board_type_id = BOARD_TYPE_ID.decode(encoded_board_type_id)
        except ValueError:
            board_type_id = pu.hexify(encoded_board_type_id)
        return board_type_id

    @staticmethod
    def _parse_board_inst_id(encoded_board_inst_id: bytes) -> str:
        board_inst_id = None
        try:
            board_inst_id = BOARD_INST_ID.decode(encoded_board_inst_id)
        except ValueError:
            board_inst_id = pu.hexify(encoded_board_inst_id)
        return board_inst_id
    
    @staticmethod
    def parse_to_object(msg_sid: bytes, msg_data: bytes) -> Union[ParsleyObject, ParsleyError]:
        """Parse msg_sid and msg_data into a ParsleyObject."""
        
        # begin parsing
        bit_str_msg_sid = BitString(msg_sid, MESSAGE_SID.length)
        encoded_msg_prio = bit_str_msg_sid.pop(MESSAGE_PRIO.length)
        encoded_msg_type = bit_str_msg_sid.pop(MESSAGE_TYPE.length)
        bit_str_msg_sid.pop(2)  # reserved field
        encoded_board_type_id = bit_str_msg_sid.pop(BOARD_TYPE_ID.length)
        encoded_board_inst_id = bit_str_msg_sid.pop(BOARD_INST_ID.length)

        board_type_id = _ParsleyParseInternal._parse_board_type_id(encoded_board_type_id)
        board_inst_id = _ParsleyParseInternal._parse_board_inst_id(encoded_board_inst_id)

        msg_prio = ''
        msg_type = ''
        data: T = {} 

        try:
            msg_prio = MESSAGE_PRIO.decode(encoded_msg_prio)
            msg_type = MESSAGE_TYPE.decode(encoded_msg_type)
            # we splice the first element since we've already manually parsed BOARD_ID
            # if BOARD_ID threw an error, we want to try and parse the rest of the CAN message
            fields = CAN_MESSAGE.get_fields(msg_type)[3:]
            data = _ParsleyParseInternal._parse_fields(BitString(msg_data), fields)
        except (ValueError, IndexError) as error:
            # convert the 6-bit msg_type into its canlib 12-bit form and include an error object
            # raise ValueError(f"Failed to parse CAN message type {pu.hexify(encoded_msg_type, is_msg_type=True)}: {error}") from error WANTED A THROWN ERROR?
            return ParsleyError(
                msg_type=pu.hexify(encoded_msg_type, is_msg_type=True),
                msg_data =pu.hexify(msg_data),
                error=str(error)
            )
            
        return ParsleyObject(
            msg_prio=msg_prio,
            msg_type=msg_type,
            board_type_id=board_type_id,
            board_inst_id=board_inst_id,
            data=data,
        )

    @staticmethod
    def parse(msg_sid: Union[int, bytes], msg_data: Union[List[int], bytes]) -> Union[ParsleyObject, ParsleyError]:
        """Normalize inputs and parse into a ParsleyObject.

        Accepts either an integer `msg_sid` with a list/bytes `msg_data`,
        or already-formatted `bytes` for `msg_sid` and `msg_data`.
        """
        # If caller provided integer SID, convert to bytes using the standard formatter
        if isinstance(msg_sid, int):
            sid_bytes, data_bytes = _ParsleyParseInternal._format_can_message(msg_sid, list(msg_data) if not isinstance(msg_data, (bytes, bytearray)) else list(msg_data))
        else:
            sid_bytes = msg_sid
            if isinstance(msg_data, (list, tuple)):
                data_bytes = bytes(msg_data)
            else:
                data_bytes = msg_data

        return _ParsleyParseInternal.parse_to_object(sid_bytes, data_bytes)

class ParsleyParser(ABC):
    """ Abstract base for different input-format parsers """

    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError("This class is an abstract class")

class USBDebugParser(ParsleyParser):
    """ Parse ASCII USB-debug lines """

    def parse(self, line: str) -> Union[ParsleyObject, ParsleyError]:
        line = line.strip(' \0\r\n')
        if len(line) == 0 or line[0] != '$':
            raise ValueError('Incorrect line format')
        line = line[1:]

        if ':' in line:
            msg_sid, msg_data = line.split(':')
            msg_sid_int = int(msg_sid, 16)
            msg_data_list = [int(byte, 16) for byte in msg_data.split(',')]
        else:
            msg_sid_int = int(line, 16)
            msg_data_list = []

        return _ParsleyParseInternal.parse(msg_sid_int, msg_data_list)

class LiveTelemetryParser(ParsleyParser):
    """ Parse binary live-telemetry """

    def parse(self, frame: bytes) -> Union[ParsleyObject, ParsleyError]:
        if len(frame) < 7:
            raise ValueError('Incorrect frame length')
        if frame[0] != 0x02:
            raise ValueError('Incorrect frame header')

        frame_len = frame[1]
        msg_sid = int.from_bytes(bytes([frame[2] & 0x1F]) + frame[3:6], byteorder='big')
        msg_data = frame[6:frame_len-1]
        exp_crc = frame[frame_len-1]
        msg_crc = crc8.crc8(frame[:frame_len-1]).digest()[0]

        if msg_crc != exp_crc:
            raise ValueError(f'Bad checksum, expected {exp_crc:02X} but got {msg_crc:02X}')

        return _ParsleyParseInternal.parse(msg_sid, list(msg_data))

class LoggerParser(ParsleyParser):
    """ Parses logger pages and yields `ParsleyObject` items """
    
    """
    Parse one logger record.

    Layout  (little-endian unless stated):
        0  – 2  : ASCII 'L','O','G'
        3       : page number (uint8)
        4  – 12 : SID (uint32 LE) | timestamp (uint32 LE) | DLC (uint8)
        13 – .. : up to 8 bytes CAN payload
        -- ff-padding may follow, removed before parsing --

    Returns whatever `format_can_message()` returns.
    Raises ValueError on any structural problem.
    """

    LOG_MAGIC = b'LOG'
    HEADER_FMT = '<IIB'
    HEADER_LEN = struct.calcsize(HEADER_FMT)

    def parse(self, buf: bytes, page_number: int) -> Union[ParsleyObject, ParsleyError]:
        if len(buf) != 4096:
            raise ValueError('Logger message must be exactly 4096 bytes')
        
        if not buf.startswith(self.LOG_MAGIC):
            raise ValueError("Missing 'LOG' signature")
        
        if buf[3] != page_number % 256:
            raise ValueError(f'Page number mismatch: expected {page_number % 256}, got {buf[3]}')

        offset = 4
        while (4096 - offset > self.HEADER_LEN):
            sid, _, dlc = struct.unpack_from(self.HEADER_FMT, buf, offset)

            if sid & 0xE000_0000:
                break

            if not 0 <= dlc <= 8:
                raise ValueError(f'DLC out of range (0-8), got {dlc}')

            offset += self.HEADER_LEN
            data_list: List[int] = list(buf[offset: offset + dlc])
            offset += dlc

            yield _ParsleyParseInternal.parse(sid, data_list)
            
class BitstringParser(ParsleyParser):

    def parse(self, bit_str: BitString) -> Union[ParsleyObject, ParsleyError]:
        msg_sid = int.from_bytes(bit_str.pop(MESSAGE_SID.length), byteorder='big')
        msg_data = [byte for byte in bit_str.pop(bit_str.length)]
        return _ParsleyParseInternal.parse(msg_sid, msg_data)
