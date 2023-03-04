from bitstring import BitString
from parsley_definitions import *
import message_types as mt


@register("GENERAL_BOARD_STATUS")
def parse_board_status(msg_data):
    timestamp = _parse_timestamp(msg_data[:3])
    board_stat = mt.board_stat_str[msg_data[3]]

    res = {"time": timestamp, "status": board_stat}

    if board_stat == 'E_BUS_OVER_CURRENT':
        current = msg_data[4] << 8 | msg_data[5]
        res["current"] = current

    elif board_stat in ["E_BUS_UNDER_VOLTAGE", "E_BUS_OVER_VOLTAGE",
                        "E_BATT_UNDER_VOLTAGE", "E_BATT_OVER_VOLTAGE"]:
        voltage = msg_data[4] << 8 | msg_data[5]
        res["voltage"] = voltage

    elif board_stat in ["E_BOARD_FEARED_DEAD", "E_MISSING_CRITICAL_BOARD"]:
        board_id = mt.board_id_str[msg_data[4]]
        res["board_id"] = board_id

    elif board_stat in ["E_NO_CAN_TRAFFIC", "E_RADIO_SIGNAL_LOST"]:
        time = msg_data[4] << 8 | msg_data[5]
        res["err_time"] = time

    elif board_stat == "E_SENSOR":
        sensor_id = mt.sensor_id_str[msg_data[4]]
        res["sensor_id"] = sensor_id

    elif board_stat == "E_ACTUATOR_STATE":
        expected_state = mt.actuator_states_str[msg_data[4]]
        cur_state = mt.actuator_states_str[msg_data[5]]
        res["req_state"] = expected_state
        res["cur_state"] = cur_state

    elif board_stat == "E_LOGGING":
        res["err"] = msg_data[4]

    return res

def parse(msg_sid, msg_data):
    msg_type = mt.msg_type_str[msg_sid & 0x7e0]
    board_id = mt.board_id_str[msg_sid & 0x1f]

    res = {"msg_type":msg_type, "board_id": board_id}
    if msg_type in FIELDS.keys():
        bit_str = BitString(msg_data)
        for field in FIELDS[msg_type]:
            data = bit_str.pop(field.length)
            res[field.name] = field.decode(data)
    else:
        res["data"] = {"unknown": msg_data}
    return res




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


MSG_TYPE_LEN = max([len(msg_type) for msg_type in mt.msg_type_hex])
BOARD_ID_LEN = max([len(board_id) for board_id in mt.board_id_hex])


def fmt_line(parsed_data):
    msg_type = parsed_data['msg_type']
    board_id = parsed_data['board_id']
    data = parsed_data["data"]
    res = f"[ {msg_type:<{MSG_TYPE_LEN}} {board_id:<{BOARD_ID_LEN}} ]"
    for k, v in data.items():
        res += f" {k}: {v}"
    return res
