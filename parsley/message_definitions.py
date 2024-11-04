from parsley.fields import ASCII, Enum, Numeric, Switch, Floating

import parsley.message_types as mt

# returns data scaled in seconds (ie. reads raw data in milliseconds and outputs seconds)
TIMESTAMP_2 = Numeric('time', 16, scale=1/1000, unit='s')
TIMESTAMP_3 = Numeric('time', 24, scale=1/1000, unit='s')

MESSAGE_PRIO = Enum('msg_prio', 2, mt.msg_prio)
MESSAGE_TYPE = Enum('msg_type', 9, mt.msg_type)
BOARD_TYPE_ID = Enum('board_type_id', 8, mt.board_type_id)
BOARD_INST_ID = Enum('board_inst_id', 8, mt.board_inst_id)
MESSAGE_SID = Enum('msg_sid', MESSAGE_PRIO.length + MESSAGE_TYPE.length + 2 + BOARD_TYPE_ID.length + BOARD_INST_ID.length, {}) # used purely as a length constant

BOARD_STATUS = {
    'E_NOMINAL':                [],

    'E_5V_OVER_CURRENT':        [Numeric('current', 16)],
    'E_5V_UNDER_VOLTAGE':       [Numeric('voltage', 16)],
    'E_5V_OVER_VOLTAGE':        [Numeric('voltage', 16)],

    'E_BATT_OVER_CURRENT':      [Numeric('current', 16)],
    'E_BATT_UNDER_VOLTAGE':     [Numeric('voltage', 16)],
    'E_BATT_OVER_VOLTAGE':      [Numeric('voltage', 16)],

    'E_13V_OVER_CURRENT':       [],
    'E_MOTOR_OVER_CURRENT':     [],

    'E_BOARD_FEARED_DEAD':      [Enum('dead_board_id', 8, mt.board_type_id)],
    'E_NO_CAN_TRAFFIC':         [Numeric('err_time', 16)],
    'E_MISSING_CRITICAL_BOARD': [Enum('missing_board_id', 8, mt.board_type_id)],
    'E_RADIO_SIGNAL_LOST':      [Numeric('err_time', 16)],

    'E_ACTUATOR_STATE':         [Enum('req_state', 8, mt.actuator_states), Enum('cur_state', 8, mt.actuator_states)],
    'E_CANNOT_INIT_DACS':       [],
    'E_VENT_POT_RANGE':         [Numeric('upper', 8, scale=1/1000), Numeric('lower', 8, scale=1/1000), Numeric('pot', 8, scale=1/1000)],

    'E_LOGGING':                [Enum('error', 8, mt.logger_error)],
    'E_GPS':                    [],
    'E_SENSOR':                 [Enum('sensor_id', 8, mt.sensor_id)],
    'E_VIDEO':                  [Enum('state', 8, mt.video_state)],

    'E_ILLEGAL_CAN_MSG':        [],
    'E_SEGFAULT':               [],
    'E_UNHANDLED_INTERRUPT':    [],
    'E_CODING_SCREWUP':         []
}

# we parse BOARD_ID seperately from the CAN message (since we want to continue parsing even if BOARD_ID throws)
# but BOARD_ID is still here so that Omnibus has all the fields it needs when creating messages to send
MESSAGES = {
    'GENERAL_CMD':          [BOARD_TYPE_ID, TIMESTAMP_3, Enum('command', 8, mt.gen_cmd)],
    'ACTUATOR_CMD':         [BOARD_TYPE_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Enum('req_state', 8, mt.actuator_states)],
    'ALT_ARM_CMD':          [BOARD_TYPE_ID, TIMESTAMP_3, Enum('state', 4, mt.arm_states), Numeric('altimeter', 4)],
    'RESET_CMD':            [BOARD_TYPE_ID, TIMESTAMP_3, Enum('reset_board_id', 8, mt.board_type_id)],

    'DEBUG_MSG':            [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('level', 4), Numeric('line', 12), ASCII('data', 24)],
    'DEBUG_PRINTF':         [BOARD_TYPE_ID, ASCII('string', 64)],
    'DEBUG_RADIO_CMD':      [BOARD_TYPE_ID, ASCII('string', 64)],
    'ACT_ANALOG_CMD':       [BOARD_TYPE_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Numeric('act_state', 8)],

    'ACTUATOR_STATUS':      [BOARD_TYPE_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Enum('cur_state', 8, mt.actuator_states), Enum('req_state', 8, mt.actuator_states)],
    'ALT_ARM_STATUS':       [BOARD_TYPE_ID, TIMESTAMP_3, Enum('state', 4, mt.arm_states), Numeric('altimeter', 4), Numeric('drogue_v', 16), Numeric('main_v', 16)],
    'GENERAL_BOARD_STATUS': [BOARD_TYPE_ID, TIMESTAMP_3, Switch('status', 8, mt.board_status, BOARD_STATUS)],

    'SENSOR_TEMP':          [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('sensor_id', 8), Numeric('temperature', 24, scale=1/2**10, unit='°C', signed=True)],
    'SENSOR_ALTITUDE':      [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('altitude', 32, signed=True)],
    'SENSOR_ACC':           [BOARD_TYPE_ID, TIMESTAMP_2, Numeric('x', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('y', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('z', 16, scale=8/2**16, unit='m/s²', signed=True)],
    'SENSOR_ACC2':          [BOARD_TYPE_ID, TIMESTAMP_2, Numeric('x', 16, scale=16/2**16, unit='m/s²', signed=True), Numeric('y', 16, scale=16/2**16, unit='m/s²', signed=True), Numeric('z', 16, scale=16/2**16, unit='m/s²', signed=True)],
    'SENSOR_GYRO':          [BOARD_TYPE_ID, TIMESTAMP_2, Numeric('x', 16, scale=2000/2**16, unit='°/s', signed=True), Numeric('y', 16, scale=2000/2**16, unit='°/s', signed=True), Numeric('z', 16, scale=2000/2**16, unit='°/s', signed=True)],

    'STATE_EST_CALIB':      [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('ack_flag', 8), Numeric('apogee', 16)],
    'SENSOR_MAG':           [BOARD_TYPE_ID, TIMESTAMP_2, Numeric('x', 16, unit='µT', signed=True), Numeric('y', 16, unit='µT', signed=True), Numeric('z', 16, unit='µT', signed=True)],
    'SENSOR_ANALOG':        [BOARD_TYPE_ID, TIMESTAMP_2, Enum('sensor_id', 8, mt.sensor_id), Numeric('value', 16, signed=True)],

    'GPS_TIMESTAMP':        [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('hrs', 8), Numeric('mins', 8), Numeric('secs', 8), Numeric('dsecs', 8)],
    'GPS_LATITUDE':         [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_LONGITUDE':        [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_ALTITUDE':         [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('altitude', 16), Numeric('daltitude', 8), ASCII('unit', 8)],
    'GPS_INFO':             [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('num_sats', 8), Numeric('quality', 8)],

    'FILL_LVL':             [BOARD_TYPE_ID, TIMESTAMP_3, Numeric('level', 8), Enum('direction', 8, mt.fill_direction)],
    'STATE_EST_DATA':       [BOARD_TYPE_ID, TIMESTAMP_3, Floating('data', big_endian=False), Enum('state_id', 8, mt.state_id)],

    'LEDS_ON':              [BOARD_TYPE_ID],
    'LEDS_OFF':             [BOARD_TYPE_ID]
}

# entire CAN message minus board_id
# board_id is parsed seperately because if it throws, we want to continue parsing
CAN_MESSAGE = Switch('msg_type', MESSAGE_TYPE.length, mt.msg_type, MESSAGES)
