import inspect, sys

from bitstring import BitString
from fields import Switch
from parsley_definitions import MESSAGE_TYPE, BOARD_ID, FIELDS

import message_types as mt

# TODO: could make this recursive, but seems overkill for current requirements
def parse(msg_type, bit_str):
    res = {}
    for field in FIELDS[msg_type]:
        data = bit_str.pop(field.length)
        res[field.name] = field.decode(data)
        if isinstance(field, Switch):
            nested_fields = field.get_fields(data)
            for nested_field in nested_fields:
                data = bit_str.pop(nested_field.length)
                res[nested_field.name] = nested_field.decode(data)
    return res

# TODO: formally comment this function ?
def parse_raw(msg_sid, msg_data):
    try:
        msg_sid = int.from_bytes(msg_sid, byteorder='big', signed=False)
        encoded_msg_type = (msg_sid & 0x7e0).to_bytes(3, byteorder='big')
        encoded_board_id = (msg_sid & 0x1f).to_bytes(3, byteorder='big')
        msg_type = parse_msg_type(encoded_msg_type)
        res["msg_type"] = msg_type
        board_id = parse_board_id(encoded_board_id)
        res["board_id"] = board_id
        res.update(parse(msg_type, BitString(msg_data)))
    except: # 
        function_name = get_exception_function_name()
        match function_name:
            case "parse_msg_type":
                res.update({"unknown_sid": msg_sid, "unknown_data": msg_data})
            case "parse_board_id": # if board_id threw, continue parsing
                res.update({"unknown_board_id": encoded_board_id})
                res.update(parse(msg_type, BitString(msg_data)))
            case "parse":
                res.update({"data": {"unknown": msg_data}})
            case _:
                res = {"error": "absolutely no clue"}
    return res

def parse_msg_type(encoded_msg_type):
    return MESSAGE_TYPE.decode(encoded_msg_type)

def parse_board_id(encoded_board_id):
    return BOARD_ID.decode(encoded_board_id)

# wizardy voodoo magic
def get_exception_function_name():
    trace_back = sys.exc_info()[-1]
    frame = trace_back.tb_frame
    function_name = frame.f_code.co_name
    return function_name

def parse_live_telemetry(line):
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

def parse_usb_debug(line):
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

def parse_logger(line):
    # see cansw_logger/can_syslog.c for format
    msg_sid, msg_data = line[:3], line[3:]
    msg_sid = int(msg_sid, 16)
    # last 'byte' is the recv_timestamp
    msg_data = [int(msg_data[i:i+2], 16) for i in range(0, len(msg_data), 2)]
    return msg_sid, msg_data

MSG_TYPE_LEN = max([len(msg_type) for msg_type in mt.msg_type])
BOARD_ID_LEN = max([len(board_id) for board_id in mt.board_id])

def format_line(parsed_data):
    msg_type = parsed_data['msg_type']
    board_id = parsed_data['board_id']
    data = parsed_data["data"]
    res = f"[ {msg_type:<{MSG_TYPE_LEN}} {board_id:<{BOARD_ID_LEN}} ]"
    for k, v in data.items():
        res += f" {k}: {v}"
    return res
