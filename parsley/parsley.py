import crc8
from typing import List, Tuple, Union

from parsley.bitstring import BitString
from parsley.fields import Field, Switch
from parsley.message_definitions import CAN_MSG, MESSAGE_TYPE, BOARD_ID, MSG_SID

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
    bit_str_msg_sid = BitString(msg_sid, MSG_SID.length)
    encoded_msg_type = bit_str_msg_sid.pop(MESSAGE_TYPE.length)
    encoded_board_id = bit_str_msg_sid.pop(BOARD_ID.length)

    res = parse_board_id(encoded_board_id)
    try:
        res['msg_type'] = MESSAGE_TYPE.decode(encoded_msg_type)
        # we splice the first element since we've already manually parsed BOARD_ID
        # if BOARD_ID threw an error, we want to try and parse the rest of the CAN message
        fields = CAN_MSG.get_fields(res['msg_type'])[1:]
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

# TODO: check what pyserial returns (I think its a byte string but thees look like strings to me)
# TODO: might also have to modify msg_data (currently an array), I'm not so sure if it'll work with the current
# parsley parse function (case we expect a byte string)
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

    return msg_sid, msg_data

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

    return msg_sid, msg_data

def parse_logger(line: str) -> Union[Tuple[bytes, bytes], None]:
    # see cansw_logger/can_syslog.c for format
    msg_sid, msg_data = line[:3], line[3:]
    msg_sid = int(msg_sid, 16)
    # last 'byte' is the recv_timestamp
    msg_data = [int(msg_data[i:i+2], 16) for i in range(0, len(msg_data), 2)]
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
        res += f' {k}: {v}'
    return res
