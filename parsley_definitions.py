from fields import ASCII, Enum, Numeric, Switch
import message_types as mt

# I think value *= scale is much more intuitive than divide
TIMESTAMP_2 = Numeric("time", 16, scale=1/1000)
TIMESTAMP_3 = Numeric("time", 24, scale=1/1000)

BOARD_STATUS = {
    "E_NOMINAL": [],
    "E_BUS_OVER_CURRENT": [Numeric("current", 16)],
    **{key: Numeric("voltage", 16) for key in ["E_BUS_UNDER_VOLTAGE", "E_BUS_OVER_VOLTAGE", "E_BATT_UNDER_VOLTAGE", "E_BATT_OVER_VOLTAGE"]},
    **{key: Enum("board_id", 8, mt.board_id_hex) for key in ["E_BOARD_FEARED_DEAD", "E_MISSING_CRITICAL_BOARD"]},
    **{key: Numeric("err_time", 16) for key in ["E_NO_CAN_TRAFFIC", "E_RADIO_SIGNAL_LOST"]},
    "E_SENSOR": [Enum("sensor_id", 8, mt.sensor_id_hex)],
    "E_ACTUATOR_STATE": [Enum("req_state", 8, mt.actuator_states_hex), Enum("cur_state", 8, mt.actuator_states_hex)]
}
"""
 missing: 
 - E_CANNOT_INIT_DACS
 - E_VENT_POT_RANGE
 - E_GPS
 - E_LOGGING
 - E_ILLEGAL_CAN_MSG
 - E_SEGFAULT
 - E_UNHANDLED_INTERRUPT
 - E_CODING_SCREWUP
 """

# FIELDS[MSG_TYPE] = ([mandatory-fields], [optional-fields])
FIELDS = {
    "GENERAL_CMD": [TIMESTAMP_3, Enum("command", 8, mt.gen_cmd_hex)],
    "ACTUATOR_CMD": [TIMESTAMP_3, Enum("actuator", 8, mt.actuator_id_hex), Enum("req_state", 8, mt.actuator_states_hex)],
    "ALT_ARM_CMD": [TIMESTAMP_3, Enum("state", 4, mt.arm_states_hex), Numeric("altimeter", 4)],
    "RESET_CMD": [TIMESTAMP_3, Enum("board_id", 8, mt.board_id_hex)],

    "DEBUG_MSG": [TIMESTAMP_3, Numeric("level", 4), Numeric("line", 12), ASCII("data", 24, optional=True)],
    "DEBUG_PRINTF": [ASCII("string", 64, optional=True)],
    "DEBUG_RADIO_CMD": [ASCII("string", 64, optional=True)],

    "ACTUATOR_STATUS": [TIMESTAMP_3, Enum("actuator", 8, mt.actuator_id_hex), Enum("req_state", 8, mt.actuator_states_hex), Enum("cur_state", 8, mt.actuator_states_hex)],
    "ALT_ARM_STATUS": [TIMESTAMP_3, Enum("state", 4, mt.arm_states_hex), Numeric("altimeter", 4), Numeric("drogue_v", 16), Numeric("main_v", 16)],
    "BOARD_STATUS": [TIMESTAMP_3, Switch(Enum("status", 8, mt.board_stat_hex), BOARD_STATUS)],

    "SENSOR_TEMP": [TIMESTAMP_3, Numeric("sensor_id", 8), Numeric("temperature", 24, scale=1/2**10, signed=True)],
    "SENSOR_ALTITUDE": [TIMESTAMP_3, Numeric("altitude", 32, signed=True)],
    "SENSOR_ACC": [TIMESTAMP_2, Numeric("x", 16, scale=8/2**16, signed=True), Numeric("y", 16, scale=8/2**16, signed=True), Numeric("z", 16, scale=8/2**16, signed=True)],
    "SENSOR_GYRO": [TIMESTAMP_2, Numeric("x", 16, scale=2000/2**16, signed=True), Numeric("y", 16, scale=2000/2**16, signed=True), Numeric("z", 16, scale=2000/2**16, signed=True)],
    "SENSOR_MAG": [TIMESTAMP_2, Numeric("x", 16, signed=True), Numeric("y", 16, signed=True), Numeric("z", 16, signed=True)],
    "SENSOR_ANALOG": [TIMESTAMP_2, Enum("sensor_id", 8, mt.sensor_id_hex), Numeric("value", 16)],

    "GPS_TIMESTAMP": [TIMESTAMP_3, Numeric("hrs", 8), Numeric("mins", 8), Numeric("secs", 8), Numeric("dsecs", 8)],
    "GPS_LATITUDE": [TIMESTAMP_3, Numeric("degs", 8), Numeric("mins", 8), Numeric("dmins", 16), ASCII("direction", 8)],
    "GPS_LONGITUDE": [TIMESTAMP_3, Numeric("degs", 8), Numeric("mins", 8), Numeric("dmins", 16), ASCII("direction", 8)],
    "GPS_ALTITUDE": [TIMESTAMP_3, Numeric("altitude", 16), Numeric("daltitude", 8), ASCII("unit", 8)],
    "GPS_INFO": [TIMESTAMP_3, Numeric("num_sats", 8), Numeric("quality", 8)],

    "FILL_LVL": [TIMESTAMP_3, Numeric("level", 8), Enum("direction", 8, mt.fill_direction_hex)],

    "RADI_VALUE": [TIMESTAMP_3, Numeric("radi_board", 8), Numeric("radi", 16)],

    "LEDS_ON": [],
    "LEDS_OFF": []
}
