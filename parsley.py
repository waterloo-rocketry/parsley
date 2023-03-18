from parsley_definitions import *

# TODO: could make this recursive, but seems overkill for current usage
def parse_cmd(msg_type, msg_data):
    res = {}
    for field in FIELDS[msg_type]:
        data = msg_data.pop(field.length)
        res[field.name] = field.decode(data)
        if isinstance(field, Switch):
            nested_fields = field.get_fields(data)
            for nested_field in nested_fields:
                data = msg_data.pop(field.length)
                res[nested_field.name] = nested_field.decode(data)
    return res

# def parse(msg_sid, msg_data):
#     msg_type = mt.msg_type_str[msg_sid & 0x7e0]
#     board_id = mt.board_id_str[msg_sid & 0x1f]

#     res = {"msg_type": msg_type, "board_id": board_id}
#     if msg_type in FIELDS.keys():
#         bit_str = BitString(msg_data)
#         for field in FIELDS[msg_type]:
#             data = bit_str.pop(field.length)
#             if isinstance(field, Switch):
#                 res[field.name] = field.decode(data)
#                 nested_fields = field.get_fields(data)
#                 for nested_field in nested_fields:
#                     data = bit_str.pop(nested_field.length)
#                     res[nested_field.name] = nested_field.decode(data)
#             else: 
#                 res[field.name] = field.decode(data)
#     else:
#         res["data"] = {"unknown": msg_data}
#     return res

# def parse_live_telemetry(line):
#     line = line.lstrip(' \0')
#     if len(line) == 0 or line[0] != '$':
#         return None
#     line = line[1:]

#     msg_sid, msg_data = line.split(":")
#     msg_data, msg_checksum = msg_data.split(";")
#     msg_sid = int(msg_sid, 16)
#     msg_data = [int(byte, 16) for byte in msg_data.split(",")]
#     sum1 = 0
#     sum2 = 0
#     for c in line[:-1]:
#         if c.lower() in "0123456789abcdef":
#             sum1 = (sum1 + int(c, 16)) % 15
#             sum2 = (sum1 + sum2) % 15
#     if int(msg_checksum, 16) != sum1 ^ sum2:
#         print(f"Bad checksum, expected {sum1 ^ sum2} but got {msg_checksum}")
#         return None

#     return msg_sid, msg_data

# def parse_usb_debug(line):
#     line = line.lstrip(' \0')
#     if len(line) == 0 or line[0] != '$':
#         return None
#     line = line[1:]

#     if ":" in line:
#         msg_sid, msg_data = line.split(":")
#         msg_sid = int(msg_sid, 16)
#         msg_data = [int(byte, 16) for byte in msg_data.split(",")]
#     else:
#         msg_sid = int(line, 16)
#         msg_data = []

#     return msg_sid, msg_data


# def parse_logger(line):
#     # see cansw_logger/can_syslog.c for format
#     msg_sid, msg_data = line[:3], line[3:]
#     msg_sid = int(msg_sid, 16)
#     # last 'byte' is the recv_timestamp
#     msg_data = [int(msg_data[i:i+2], 16) for i in range(0, len(msg_data), 2)]
#     return msg_sid, msg_data


# MSG_TYPE_LEN = max([len(msg_type) for msg_type in mt.msg_type_hex])
# BOARD_ID_LEN = max([len(board_id) for board_id in mt.board_id_hex])


# def fmt_line(parsed_data):
#     msg_type = parsed_data['msg_type']
#     board_id = parsed_data['board_id']
#     data = parsed_data["data"]
#     res = f"[ {msg_type:<{MSG_TYPE_LEN}} {board_id:<{BOARD_ID_LEN}} ]"
#     for k, v in data.items():
#         res += f" {k}: {v}"
#     return res
