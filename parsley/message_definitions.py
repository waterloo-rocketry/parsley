from parsley.fields import ASCII, Enum, Numeric, Switch

import parsley.message_types as mt

# returns data scaled in seconds (ie. reads raw data in milliseconds and outputs seconds)
TIMESTAMP_2 = Numeric('time', 16, scale=1/1000, unit='s')
TIMESTAMP_3 = Numeric('time', 24, scale=1/1000, unit='s')

MESSAGE_TYPE = Enum('msg_type', 6, mt.adjusted_msg_type)
BOARD_ID = Enum('board_id', 5, mt.board_id)
MESSAGE_SID = Enum('msg_sid', MESSAGE_TYPE.length + BOARD_ID.length, {}) # used purely as a length constant

BOARD_STATUS = {
    'E_NOMINAL':                [],

    'E_BUS_OVER_CURRENT':       [Numeric('current', 16)],
    'E_BUS_UNDER_VOLTAGE':      [Numeric('voltage', 16)],
    'E_BUS_OVER_VOLTAGE':       [Numeric('voltage', 16)],

    'E_BATT_OVER_CURRENT':      [Numeric('current', 16)],
    'E_BATT_UNDER_VOLTAGE':     [Numeric('voltage', 16)],
    'E_BATT_OVER_VOLTAGE':      [Numeric('voltage', 16)],

    'E_BOARD_FEARED_DEAD':      [Enum('dead_board_id', 8, mt.board_id)],
    'E_NO_CAN_TRAFFIC':         [Numeric('err_time', 16)],
    'E_MISSING_CRITICAL_BOARD': [Enum('missing_board_id', 8, mt.board_id)],
    'E_RADIO_SIGNAL_LOST':      [Numeric('err_time', 16)],

    'E_ACTUATOR_STATE':         [Enum('req_state', 8, mt.actuator_states), Enum('cur_state', 8, mt.actuator_states)],
    'E_CANNOT_INIT_DACS':       [],
    'E_VENT_POT_RANGE':         [Numeric('upper', 8, scale=1/1000), Numeric('lower', 8, scale=1/1000), Numeric('pot', 8, scale=1/1000)],

    'E_LOGGING':                [Enum('error', 8, mt.logger_error)],
    'E_GPS':                    [],
    'E_SENSOR':                 [Enum('sensor_id', 8, mt.sensor_id)],

    'E_ILLEGAL_CAN_MSG':        [],
    'E_SEGFAULT':               [],
    'E_UNHANDLED_INTERRUPT':    [],
    'E_CODING_SCREWUP':         []
}

# we parse BOARD_ID seperately from the CAN message (since we want to continue parsing even if BOARD_ID throws)
# but BOARD_ID is still here so that Omnibus has all the fields it needs when creating messages to send
MESSAGES = {
    'GENERAL_CMD':          [BOARD_ID, TIMESTAMP_3, Enum('command', 8, mt.gen_cmd)],
    'ACTUATOR_CMD':         [BOARD_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Enum('req_state', 8, mt.actuator_states)],
    'ALT_ARM_CMD':          [BOARD_ID, TIMESTAMP_3, Enum('state', 4, mt.arm_states), Numeric('altimeter', 4)],
    'RESET_CMD':            [BOARD_ID, TIMESTAMP_3, Enum('reset_board_id', 8, mt.board_id)],

    'DEBUG_MSG':            [BOARD_ID, TIMESTAMP_3, Numeric('level', 4), Numeric('line', 12), ASCII('data', 24)],
    'DEBUG_PRINTF':         [BOARD_ID, ASCII('string', 64)],
    'DEBUG_RADIO_CMD':      [BOARD_ID, ASCII('string', 64)],
    'ACT_ANALOG_CMD':       [BOARD_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Numeric('act_state', 32)],

    'ACTUATOR_STATUS':      [BOARD_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Enum('cur_state', 8, mt.actuator_states), Enum('req_state', 8, mt.actuator_states)],
    'ALT_ARM_STATUS':       [BOARD_ID, TIMESTAMP_3, Enum('state', 4, mt.arm_states), Numeric('altimeter', 4), Numeric('drogue_v', 16), Numeric('main_v', 16)],
    'GENERAL_BOARD_STATUS': [BOARD_ID, TIMESTAMP_3, Switch('status', 8, mt.board_status, BOARD_STATUS)],

    'SENSOR_TEMP':          [BOARD_ID, TIMESTAMP_3, Numeric('sensor_id', 8), Numeric('temperature', 24, scale=1/2**10, unit='°C', signed=True)],
    'SENSOR_ALTITUDE':      [BOARD_ID, TIMESTAMP_3, Numeric('altitude', 32, signed=True)],
    'SENSOR_ACC':           [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('y', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('z', 16, scale=8/2**16, unit='m/s²', signed=True)],
    'SENSOR_ACC2':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, scale=16/2**16, unit='m/s²', signed=True), Numeric('y', 16, scale=16/2**16, unit='m/s²', signed=True), Numeric('z', 16, scale=16/2**16, unit='m/s²', signed=True)],
    'SENSOR_GYRO':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, scale=2000/2**16, unit='°/s', signed=True), Numeric('y', 16, scale=2000/2**16, unit='°/s', signed=True), Numeric('z', 16, scale=2000/2**16, unit='°/s', signed=True)],

    'STATE_EST_CALIB':      [BOARD_ID, TIMESTAMP_3, Numeric('ack_flag', 8), Numeric('apogee', 16)],
    'SENSOR_MAG':           [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='µT', signed=True), Numeric('y', 16, unit='µT', signed=True), Numeric('z', 16, unit='µT', signed=True)],
    'SENSOR_ANALOG':        [BOARD_ID, TIMESTAMP_2, Enum('sensor_id', 8, mt.sensor_id), Numeric('value', 16, signed=True)],

    'GPS_TIMESTAMP':        [BOARD_ID, TIMESTAMP_3, Numeric('hrs', 8), Numeric('mins', 8), Numeric('secs', 8), Numeric('dsecs', 8)],
    'GPS_LATITUDE':         [BOARD_ID, TIMESTAMP_3, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_LONGITUDE':        [BOARD_ID, TIMESTAMP_3, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_ALTITUDE':         [BOARD_ID, TIMESTAMP_3, Numeric('altitude', 16), Numeric('daltitude', 8), ASCII('unit', 8)],
    'GPS_INFO':             [BOARD_ID, TIMESTAMP_3, Numeric('num_sats', 8), Numeric('quality', 8)],

    'FILL_LVL':             [BOARD_ID, TIMESTAMP_3, Numeric('level', 8), Enum('direction', 8, mt.fill_direction)],
    'STATE_EST_DATA':       [BOARD_ID, TIMESTAMP_3, Numeric('data', 32), Enum('state_id', 8, mt.state_id)],

    'LEDS_ON':              [BOARD_ID],
    'LEDS_OFF':             [BOARD_ID]
}

# entire CAN message minus board_id 
# board_id is parsed seperately because if it throws, we want to continue parsing
CAN_MESSAGE = Switch('msg_type', MESSAGE_TYPE.length, mt.adjusted_msg_type, MESSAGES)
