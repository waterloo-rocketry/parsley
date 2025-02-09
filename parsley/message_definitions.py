from parsley.fields import ASCII, Enum, Numeric, Switch, Floating

import parsley.message_types as mt

# returns data scaled in seconds (ie. reads raw data in milliseconds and outputs seconds)
TIMESTAMP_2 = Numeric('time', 16, scale=1/1000, unit='s')

MESSAGE_PRIO = Enum('msg_prio', 2, mt.msg_prio)
MESSAGE_TYPE = Enum('msg_type', 9, mt.msg_type)
BOARD_TYPE_ID = Enum('board_type_id', 8, mt.board_type_id)
BOARD_INST_ID = Enum('board_inst_id', 8, mt.board_inst_id)
MESSAGE_SID = Enum('msg_sid', MESSAGE_PRIO.length + MESSAGE_TYPE.length + 2 + BOARD_TYPE_ID.length + BOARD_INST_ID.length, {}) # used purely as a length constant

# we parse BOARD_ID seperately from the CAN message (since we want to continue parsing even if BOARD_ID throws)
# but BOARD_ID is still here so that Omnibus has all the fields it needs when creating messages to send
MESSAGES = {
    'GENERAL_BOARD_STATUS': [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('general_error_bitfield', 32), Numeric('board_error_bitfield', 16)],
    'RESET_CMD':            [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('board_type_id', 8, mt.board_type_id), Enum('board_inst_id', 8, mt.board_inst_id)],
    'DEBUG_RAW':            [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, ASCII('string', 48)],
    'CONFIG_SET':           [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('config_id', 16), Numeric('config_value', 32)],
    'CONFIG_STATUS':        [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('config_id', 16), Numeric('config_value', 32)],
    'ACTUATOR_CMD':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('actuator', 8, mt.actuator_id), Enum('req_state', 8, mt.actuator_state)],
    'ACTUATOR_ANALOG_CMD':  [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('actuator', 8, mt.actuator_id), Numeric('act_state', 16)],
    'ACTUATOR_STATUS':      [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('actuator', 8, mt.actuator_id), Enum('curr_state', 8, mt.actuator_state), Enum('req_state', 8, mt.actuator_state)],
    'ALT_ARM_CMD':          [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('alt_id', 8, mt.altimeter_id), Enum('alt_arm_state', 8, mt.alt_arm_state)],
    'ALT_ARM_STATUS':       [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('alt_id', 8, mt.altimeter_id), Enum('alt_arm_state', 8, mt.alt_arm_state), Numeric('drogue_v', 16), Numeric('main_v', 16)],
    'SENSOR_TEMP':          [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('temp_sensor_id', 8), Numeric('temperature', 32, scale=1/2**10, unit='°C', signed=True)],
    'SENSOR_ALTITUDE':      [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('altitude', 32, signed=True)],
    'SENSOR_IMU_X':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('linear_accel', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('angular_velocity', 166, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_IMU_Y':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('linear_accel', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('angular_velocity', 166, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_IMU_Z':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('linear_accel', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('angular_velocity', 166, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_MAG_X':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('mag', 16)],
    'SENSOR_MAG_Y':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('mag', 16)],
    'SENSOR_MAG_Z':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('mag', 16)],
    'SENSOR_ANALOG':        [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('sensor_id', 8, mt.analog_sensor_id), Numeric('value', 16)],
    'GPS_TIMESTAMP':        [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('hrs', 8), Numeric('mins', 8), Numeric('secs', 8), Numeric('dsecs', 8)],
    'GPS_LATITUDE':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_LONGITUDE':        [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_ALTITUDE':         [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('altitude', 16), Numeric('daltitude', 8), ASCII('unit', 8)],
    'GPS_INFO':             [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('num_sats', 8), Numeric('quality', 8)],
    'STATE_EST_DATA':       [BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('state_id', 8, mt.state_est_id), Floating('data', big_endian=True)],
    'LEDS_ON':              [BOARD_TYPE_ID, BOARD_INST_ID],
    'LEDS_OFF':             [BOARD_TYPE_ID, BOARD_INST_ID]
}

# entire CAN message minus board_id
# board_id is parsed seperately because if it throws, we want to continue parsing
CAN_MESSAGE = Switch('msg_type', MESSAGE_TYPE.length, mt.msg_type, MESSAGES)
