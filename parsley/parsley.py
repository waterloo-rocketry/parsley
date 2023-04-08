from typing import Tuple, Union

from parsley.bitstring import BitString
from parsley.fields import Switch
from parsley.parsley_definitions import CAN_MSG, MESSAGE_TYPE, BOARD_ID, MSG_SID

import parsley.message_types as mt

def parse(bit_str: BitString, fields: Switch) -> dict:
    """
    Parses binary data stored in a BitString using a predefined structure specified in
    parsley_definitions.py. The function iterates over the respective field types decoded from
    a Switch Field, which acts as a forkroad changing how data is parsed based on the BitString data.
    """
    res = {}
    data = bit_str.pop(fields.length)
    res[fields.name] = fields.decode(data)
    for field in fields.get_fields(res[fields.name]):
        if isinstance(field, Switch):
            res.update(parse(bit_str, field))
            continue
        data = bit_str.pop(field.length)
        res[field.name] = field.decode(data)
    return res

def parse_raw(msg_sid: bytes, msg_data: bytes) -> dict:
    """
    Extracts metadata from message_sid and with message_data, constructs a parseable CAN message.
    Upon reading poorly formatted data, the error is caught and returned in the dictionary.
    If BOARD_ID fails to parse, we will try to salvage the rest of the CAN message.
    """
    bit_str_msg_sid = BitString(msg_sid, MSG_SID.length)
    encoded_msg_type = bit_str_msg_sid.pop(MESSAGE_TYPE.length)
    encoded_board_id = bit_str_msg_sid.pop(BOARD_ID.length)

    # we can't append msg_data to msg_type since we don't always know its bit-message size
    bit_str_can_msg = BitString(msg_data)
    bit_str_can_msg.push_front(encoded_msg_type, MESSAGE_TYPE.length)
    res = parse_board_id(encoded_board_id)
    try:
        res["data"] = parse(bit_str_can_msg, CAN_MSG)
        # res.update(parse(bit_str_can_msg, CAN_MSG))
    except (ValueError, IndexError) as error:
        res = {
            "msg_type": str(encoded_msg_type),
            "board_id": str(encoded_board_id),
            "data": str(msg_data),
            "error": str(error)
        }
    return res

def parse_board_id(encoded_board_id: bytes) -> dict:
    try:
        board_id = BOARD_ID.decode(encoded_board_id)
    except:
        board_id = f"unknown: {encoded_board_id}"
    finally:
        return {"board_id": board_id}

def parse_live_telemetry(line: bytes) -> Union[Tuple[bytes, bytes], None]:
    line = line.lstrip(' \0')
    if len(line) == 0 or line[0] != '$':
        return None
    line = line[1:]

    msg_sid, msg_data = line.split(":")
    msg_data, msg_checksum = msg_data.split(";")
    msg_sid = int(msg_sid, 16)
    msg_data = [int(byte, 16) for byte in msg_data.split(",")]
    sum1 = 0
    sum2 = 0
    for c in line[:-1]:
        if c.lower() in "0123456789abcdef":
            sum1 = (sum1 + int(c, 16)) % 15
            sum2 = (sum1 + sum2) % 15
    if int(msg_checksum, 16) != sum1 ^ sum2:
        print(f"Bad checksum, expected {sum1 ^ sum2} but got {msg_checksum}")
        return None

    return msg_sid, msg_data

def parse_usb_debug(line: bytes) -> Union[Tuple[bytes, bytes], None]:
    line = line.lstrip(' \0')
    if len(line) == 0 or line[0] != '$':
        return None
    line = line[1:]

    if ":" in line:
        msg_sid, msg_data = line.split(":")
        msg_sid = int(msg_sid, 16)
        msg_data = [int(byte, 16) for byte in msg_data.split(",")]
    else:
        msg_sid = int(line, 16)
        msg_data = []

    return msg_sid, msg_data

def parse_logger(line: bytes) -> Union[Tuple[bytes, bytes], None]:
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
    msg_type = parsed_data['data']['msg_type']
    board_id = parsed_data['board_id']
    data = parsed_data['data']
    data.pop('msg_type') # changed where msg_type exists in the dict, removing to avoid duplicates
    res = f"[ {msg_type:<{MSG_TYPE_LEN}} {board_id:<{BOARD_ID_LEN}} ]"
    for k, v in data.items():
        res += f" {k}: {v}"
    return res
