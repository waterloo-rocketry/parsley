import crc8
from typing import List, Tuple, Union

from parsley.bitstring import BitString
from parsley.fields import Field, Switch
from parsley.message_definitions import CAN_MESSAGE, MESSAGE_TYPE, BOARD_ID, MESSAGE_SID

import parsley.message_types as mt
import parsley.parse_utils as pu

def parse_fields(bit_str: BitString, fields: List[Field]) -> dict:
    """
    Parses binary data stored in a BitString and decodes the data
    based on each field's decode() implementation. Returns a dictionary
    of each field's name to its decoded python value.
    """
    res = {}
    for field in fields:
        data = bit_str.pop(field.length)
        res[field.name] = field.decode(data)
        if isinstance(field, Switch):
            nested_fields = field.get_fields(res[field.name])
            res.update(parse_fields(bit_str, nested_fields))
    return res

def parse(msg_sid: bytes, msg_data: bytes) -> dict:
    """
    Extracts the message_type and board_id from msg_sid to construct a CAN message along with message_data.
    Upon reading poorly formatted data, the error is caught and returned in the dictionary.
    """
    bit_str_msg_sid = BitString(msg_sid, MESSAGE_SID.length)
    encoded_msg_type = bit_str_msg_sid.pop(MESSAGE_TYPE.length)
    encoded_board_id = bit_str_msg_sid.pop(BOARD_ID.length)

    res = parse_board_id(encoded_board_id)
    try:
        res['msg_type'] = MESSAGE_TYPE.decode(encoded_msg_type)
        # we splice the first element since we've already manually parsed BOARD_ID
        # if BOARD_ID threw an error, we want to try and parse the rest of the CAN message
        fields = CAN_MESSAGE.get_fields(res['msg_type'])[1:]
        res['data'] = parse_fields(BitString(msg_data), fields)
    except (ValueError, IndexError) as error:
        res.update({
            # convert the 6-bit msg_type into its canlib 12-bit form
            'msg_type': pu.hexify(encoded_msg_type, is_msg_type=True),
            'data': {
                'msg_data': pu.hexify(msg_data),
                'error': str(error)
            }
        })
    return res

def parse_board_id(encoded_board_id: bytes) -> dict:
    try:
        board_id = BOARD_ID.decode(encoded_board_id)
    except ValueError:
        board_id = pu.hexify(encoded_board_id)
    finally:
        return {'board_id': board_id}

def parse_bitstring(bit_str: BitString) -> Tuple[bytes, bytes]:
    msg_sid = int.from_bytes(bit_str.pop(MESSAGE_SID.length), byteorder='big')
    msg_data = [byte for byte in bit_str.pop(bit_str.length)]
    return format_can_message(msg_sid, msg_data)

def parse_live_telemetry(line: str) -> Union[Tuple[bytes, bytes], None]:
    line = line.lstrip(' \0')
    if len(line) == 0 or line[0] != '$':
        return None
    line = line[1:]

    msg_sid, msg_data = line.split(':')
    msg_data, msg_checksum = msg_data.split(';')
    msg_sid = int(msg_sid, 16)
    msg_data = [int(byte, 16) for byte in msg_data.split(',')]
    exp_sum = crc8.crc8(msg_sid.to_bytes(2, byteorder='big'))
    for c in msg_data:
        exp_sum.update(c.to_bytes(1, byteorder='big'))
    exp_sum_value = exp_sum.hexdigest().upper()
    if msg_checksum != exp_sum_value:
        print(f'Bad checksum, expected {exp_sum_value} but got {msg_checksum}')
        return None

    return format_can_message(msg_sid, msg_data)

def parse_usb_debug(line: str) -> Union[Tuple[bytes, bytes], None]:
    line = line.lstrip(' \0')
    if len(line) == 0 or line[0] != '$':
        return None
    line = line[1:]

    if ':' in line:
        msg_sid, msg_data = line.split(':')
        msg_sid = int(msg_sid, 16)
        msg_data = [int(byte, 16) for byte in msg_data.split(',')]
    else:
        msg_sid = int(line, 16)
        msg_data = []

    return format_can_message(msg_sid, msg_data)

def parse_logger(line: str) -> Union[Tuple[bytes, bytes], None]:
    # see cansw_logger/can_syslog.c for format
    msg_sid, msg_data = line[:3], line[3:]
    msg_sid = int(msg_sid, 16)
    # last 'byte' is the recv_timestamp
    msg_data = [int(msg_data[i:i+2], 16) for i in range(0, len(msg_data), 2)]
    return format_can_message(msg_sid, msg_data)

# our three parsing functions create ints, but after the rewrite, they should return bytes
def format_can_message(msg_sid: int, msg_data: List[int]) -> Tuple[bytes, bytes]:
    msg_sid_length = (msg_sid.bit_length() + 7) // 8
    formatted_msg_sid = msg_sid.to_bytes(msg_sid_length, byteorder='big')
    formatted_msg_data = bytes(msg_data)
    return formatted_msg_sid, formatted_msg_data

# given a dictionary of CAN message data, return the CAN message bits
def encode_data(parsed_data: dict) -> Tuple[bytes, bytes]:
    msg_type = parsed_data.pop('msg_type')
    board_id = parsed_data.pop('board_id')

    bit_str = BitString()
    bit_str.push(*MESSAGE_TYPE.encode(msg_type))
    bit_str.push(*BOARD_ID.encode(board_id))
    msg_sid = int.from_bytes(bit_str.pop(bit_str.length), byteorder='big')

    # skip the first field (board_id) since thats parsed separately
    for field in CAN_MESSAGE.get_fields(msg_type)[1:]:
        bit_str.push(*field.encode(parsed_data[field.name]))
    msg_data = [byte for byte in bit_str.pop(bit_str.length)]
    return msg_sid, msg_data

MSG_TYPE_LEN = max([len(msg_type) for msg_type in mt.msg_type])
BOARD_ID_LEN = max([len(board_id) for board_id in mt.board_id])

# formats a parsed CAN message (dictionary) into a singular line
def format_line(parsed_data: dict) -> str:
    msg_type = parsed_data['msg_type']
    board_id = parsed_data['board_id']
    data = parsed_data['data']
    res = f'[ {msg_type:<{MSG_TYPE_LEN}} {board_id:<{BOARD_ID_LEN}} ]'
    for k, v in data.items():
        formatted_value = f"{v:.3f}" if isinstance(v, float) else v
        res += f' {k}: {formatted_value}'
    return res
