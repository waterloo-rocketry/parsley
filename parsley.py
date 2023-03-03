from ascii import Ascii
from bitstring import BitString
from enum_was_taken import Enum
from field import Field
from numeric import Numeric
import message_types as mt

TIMESTAMP_2 = Numeric("time", 16, scale=1000, signed=True)
TIMESTAMP_3 = Numeric("time", 24, scale=1000)

FIELDS = {
    "GENERAL_CMD": [TIMESTAMP_3, Enum("command", 8, mt.gen_cmd_hex)],
    "ACTUATOR_CMD": [TIMESTAMP_3, Enum("actuator", 8, mt.actuator_id_hex), Enum("state", 8, mt.actuator_states_hex)],
    "ALT_ARM_CMD": [TIMESTAMP_3, Enum("state", 4, mt.arm_states_hex), Numeric("number", 4)],
    "RESET_CMD": [TIMESTAMP_3, Enum("id", 8, mt.board_id_hex)],

    "DEBUG_MSG": [TIMESTAMP_3, Numeric("level", 4), Numeric("line", 12), Ascii("data", 24)],
    "DEBUG_PRINTF": [Ascii("string", 64)],
    "DEBUG_RADIO_CMD": [Ascii("string", 64)],

    "ACTUATOR_STAT": [TIMESTAMP_3, Enum("actuator", 8, mt.actuator_id_hex), Enum("req_state", 8, mt.actuator_states_hex), Enum("cur_state", 8, mt.actuator_states_hex)],
    "ALT_ARM_STAT": [TIMESTAMP_3, Enum("state", 4, mt.arm_states_hex), Numeric("number", 4), Numeric("drogue_v", 16, signed=True), Numeric("main_v", 16, signed=True)],
    "BOARD_STAT": [TIMESTAMP_3, Enum("stat", 8, mt.board_stat_hex) ], # TODO HALP

    "SENSOR_TEMP": [TIMESTAMP_3, Numeric("sensor", 8), Numeric("temperature", 24, scale=0.001, signed=True)],
    "SENSOR_ALTITUDE": [TIMESTAMP_3, Numeric("altitude", 32, signed=False)], # weird signed 2s compliment subtraction
    "SENSOR_ACC": [TIMESTAMP_2, Numeric("x", 16, scale=0.0001, signed=True), Numeric("y", 16, scale=0.0001, signed=True), Numeric("z", 16, scale=0.0001, signed=True)], # weird a / (2**16) * 8 going on but also x16 for ACC2 ?? or just a parlsey thing, signed in parsley parse
    "SENSOR_GYRO": [TIMESTAMP_2, Numeric("x", 16, scale=0.03, signed=True), Numeric("y", 16, scale=0.03, signed=True), Numeric("z", 16, scale=0.03, signed=True)], # unsure about rounding, signed in parsley parse
    "SENSOR_MAG": [TIMESTAMP_2, Numeric("x", 16, signed=True), Numeric("y", 16, signed=True), Numeric("z", 16, signed=True)], # they're signed in parsley parse
    "SENSOR_ANALOG": [TIMESTAMP_2, Enum("id", 8, mt.sensor_id_hex), Numeric("value", 16, signed=True)],

    "GPS_TIMESTAMP": [TIMESTAMP_3, Numeric("hours", 8), Numeric("minutes", 8), Numeric("seconds", 8), Numeric("dseconds", 8)],
    "GPS_LATITUDE": [TIMESTAMP_3, Numeric("degrees", 8), Numeric("minutes", 8), Numeric("dminutes", 16, signed=True), Ascii("direction", 8)],
    "GPS_LONGITUDE": [TIMESTAMP_3, Numeric("degrees", 8), Numeric("minutes", 8), Numeric("dminutes", 16, signed=True), Ascii("direction", 8)],
    "GPS_ALTITUDE": [TIMESTAMP_3, Numeric("altitude", 16, signed=True), Numeric("daltitude", 8), Ascii("unit", 8)],
    "GPS_INFO": [TIMESTAMP_3, Numeric("numsat", 8), Numeric("quality", 8)],

    "FILL_LVL": [TIMESTAMP_3, Numeric("level", 8), Enum("direction", 8, mt.fill_direction_hex)],

    "RADI_VALUE": [TIMESTAMP_3, Numeric("board", 8), Numeric("radi", 16, signed=True)],

    "LEDS_ON": [],
    "LEDS_OFF": []
}

def parse(msg_sid, msg_data):
    msg_type = mt.msg_type_str[msg_sid & 0x7e0]
    board_id = mt.board_id_str[msg_sid & 0x1f]
    msg_data = BitString(msg_data)

    result = {"msg_type": msg_type, "board_id": board_id, "data": {}}
    for field in FIELDS[msg_type]:
        result["data"][field.name] = field.decode(msg_data.pop(field.length))

    return result
