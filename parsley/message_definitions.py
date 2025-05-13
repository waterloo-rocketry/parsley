from parsley.fields import ASCII, Enum, Numeric, Switch, Floating, Bitfield

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
    'GENERAL_BOARD_STATUS': [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Bitfield(name="general_board_status", default="E_NOMINAL", length=8, width=8, map_name_offset=mt.general_board_status_offset), Numeric('general_error_bitfield', 32), Numeric('board_error_bitfield', 16)],
    'RESET_CMD':            [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('board_type_id', 8, mt.board_type_id), Enum('board_inst_id', 8, mt.board_inst_id)],
    'DEBUG_RAW':            [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, ASCII('string', 48)],
    'CONFIG_SET':           [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('board_type_id', 8, mt.board_type_id), Enum('board_inst_id', 8, mt.board_inst_id), Numeric('config_id', 16), Numeric('config_value', 16)],
    'CONFIG_STATUS':        [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('config_id', 16), Numeric('config_value', 16)],
    'ACTUATOR_CMD':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('actuator', 8, mt.actuator_id), Enum('cmd_state', 8, mt.actuator_state)],
    'ACTUATOR_ANALOG_CMD':  [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('actuator', 8, mt.actuator_id), Numeric('cmd_state', 16)],
    'ACTUATOR_STATUS':      [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('actuator', 8, mt.actuator_id), Enum('curr_state', 8, mt.actuator_state), Enum('cmd_state', 8, mt.actuator_state)],
    'ALT_ARM_CMD':          [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('alt_id', 8, mt.altimeter_id), Enum('alt_arm_state', 8, mt.alt_arm_state)],
    'ALT_ARM_STATUS':       [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('alt_id', 8, mt.altimeter_id), Enum('alt_arm_state', 8, mt.alt_arm_state), Numeric('drogue_v', 16), Numeric('main_v', 16)],
    'SENSOR_TEMP':          [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('temp_sensor_id', 8), Numeric('temperature', 32, scale=1/2**10, unit='°C', signed=True)],
    'SENSOR_ALTITUDE':      [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('altitude', 32, signed=True)],
    'SENSOR_IMU_X':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('linear_accel', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('angular_velocity', 16, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_IMU_Y':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('linear_accel', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('angular_velocity', 16, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_IMU_Z':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('linear_accel', 16, scale=8/2**16, unit='m/s²', signed=True), Numeric('angular_velocity', 16, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_MAG_X':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('mag', 16)],
    'SENSOR_MAG_Y':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('mag', 16)],
    'SENSOR_MAG_Z':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('mag', 16)],
    'SENSOR_BARO':          [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('imu_id', 8, mt.imu_id), Numeric('pressure', 24), Numeric('temp', 16)],
    'SENSOR_ANALOG':        [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('sensor_id', 8, mt.analog_sensor_id), Numeric('value', 16)],
    'GPS_TIMESTAMP':        [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('hrs', 8), Numeric('mins', 8), Numeric('secs', 8), Numeric('dsecs', 8)],
    'GPS_LATITUDE':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_LONGITUDE':        [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_ALTITUDE':         [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('altitude', 16), Numeric('daltitude', 8), ASCII('unit', 8)],
    'GPS_INFO':             [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Numeric('num_sats', 8), Numeric('quality', 8)],
    'STATE_EST_DATA':       [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, TIMESTAMP_2, Enum('state_id', 8, mt.state_est_id), Floating('data', big_endian=True)],
    'LEDS_ON':              [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID],
    'LEDS_OFF':             [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID]
}

# entire CAN message minus board_id
# board_id is parsed seperately because if it throws, we want to continue parsing
CAN_MESSAGE = Switch('msg_type', MESSAGE_TYPE.length, mt.msg_type, MESSAGES)
