from parsley.fields import ASCII, Enum, Numeric, Switch, Raw

import parsley.message_types as mt

# returns data scaled in seconds (ie. reads raw data in milliseconds and outputs seconds)
TIMESTAMP_1 = Numeric('time', 8, scale=1/11718.75, unit='s')
TIMESTAMP_2 = Numeric('time', 16, scale=1/11718.75, unit='s')
TIMESTAMP_3 = Numeric('time', 24, scale=1/11718.75, unit='s')
SENSOR_ID = Enum('sensor_id', 8, mt.sensor_id)

MESSAGE_TYPE = Enum('msg_type', 6, mt.adjusted_msg_type)
BOARD_ID = Enum('board_id', 5, mt.board_id)
MESSAGE_SID = Enum('msg_sid', MESSAGE_TYPE.length + BOARD_ID.length, {}) # used purely as a length constant
PT_SCALE = (3000)/((20.0-4.0)*100);
PT_OFFSET = -PT_SCALE*4*100;
D_SCALE = 1 #(4.0/5000.0)*(39.3701/1.00000054)*(3+10)/10.0; #40.99448/1000   should be 102.35 71.46, 90.32, 113.22 
D_OFFSET = 0 #-D_SCALE*1000.0;#157.6538
ISNS_SCALE = 1/(50.0*5.0);
RPM_CONV = 60.0/2;
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
    'E_CODING_FUCKUP':         []
}
#0-1500PSIG scaling on PTs
RPM_CHANNELS = {
    'RPM501_S': [Numeric('RPM_S',32, scale=RPM_CONV*8.35)],
    'RPM502_S': [Numeric('RPM_S',32, scale=RPM_CONV*8.35)],
    'RPM501_H': [Numeric('RPM_H',32, scale=RPM_CONV*20.85*4)],
    'RPM502_H': [Numeric('RPM_H',32, scale=RPM_CONV*20.85*4)],

    'RPM501_MAX': [Numeric('RPM_H_MAX',32, scale=RPM_CONV*20.85*4)],
    'RPM502_MAX': [Numeric('RPM_H_MAX',32, scale=RPM_CONV*20.85*4)]
}
ANALOG_CHANNELS = {
    #pressure transducers
    'P501': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P502': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P503': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P504': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P505': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P506': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P301': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P506': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P301': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],
    'P506': [Numeric('pressure',16, scale=PT_SCALE, offset=PT_OFFSET)],

    #displacement
    'D501': [Numeric('displacement',16, scale=D_SCALE, offset=D_OFFSET)],
    'D502': [Numeric('displacement',16, scale=D_SCALE, offset=D_OFFSET)],
    'D501_MAX': [Numeric('displacement',16, scale=D_SCALE, offset=D_OFFSET)],
    'D502_MAX': [Numeric('displacement',16, scale=D_SCALE, offset=D_OFFSET)],

    #voltage & current monitoring
    'ISENSE_24V': [Numeric('current',16, scale=ISNS_SCALE)],
    'VSENSE_24V': [Numeric('voltage',16, scale=(56+10)/10000.0)],
    'ISENSE_12VD': [Numeric('current',16, scale=ISNS_SCALE)],
    'VSENSE_12VD': [Numeric('voltage',16, scale=(22+10)/10000.0, offset=D_OFFSET)],
    'ISENSE_12VA': [Numeric('current',16, scale=ISNS_SCALE)],
    'VSENSE_12VA': [Numeric('voltage',16, scale=(22+10)/10000.0)],
    'ISENSE_5VD': [Numeric('current',16, scale=ISNS_SCALE)],
    'VSENSE_5VD': [Numeric('voltage',16, scale=(3+10)/10000.0)],
    'ISENSE_5VD': [Numeric('current',16, scale=ISNS_SCALE)],
    'VSENSE_5VA': [Numeric('voltage',16, scale=(3+10)/10000.0)],
    'ISENSE_5VA': [Numeric('current',16, scale=ISNS_SCALE)],
    'VSENSE_3V3': [Numeric('voltage',16, scale=1/1000.0)],
    'ISENSE_3V3': [Numeric('current',16, scale=ISNS_SCALE)],
    'RAW_ISENSE_5V': [Numeric('voltage',16, scale=ISNS_SCALE)],
    'RAW_ISENSE_12V': [Numeric('current',16, scale=ISNS_SCALE)],
    'RAW_ISENSE_24V': [Numeric('voltage',16, scale=ISNS_SCALE)],
    'GOG_ISENSE': [Numeric('current',16, scale=D_SCALE)],

}

# we parse BOARD_ID seperately from the CAN message (since we want to continue parsing even if BOARD_ID throws)
# but BOARD_ID is still here so that Omnibus has all the fields it needs when creating messages to send
MESSAGES = {
    'GENERAL_CMD':          [BOARD_ID, TIMESTAMP_3, Enum('command', 8, mt.gen_cmd)],
    'ACTUATOR_CMD':         [BOARD_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Enum('req_state', 8, mt.actuator_states)],
    'ALT_ARM_CMD':          [BOARD_ID, TIMESTAMP_3, Enum('state', 4, mt.arm_states), Numeric('altimeter', 4)],
    'RESET_CMD':            [BOARD_ID, TIMESTAMP_3, Enum('reset_board_id', 8, mt.board_id)],

    'DEBUG_MSG':            [BOARD_ID, TIMESTAMP_3, Numeric('tmrh', 8), Numeric('tmrl', 8), Numeric('typ', 8),Numeric('id', 8)],
    'DEBUG_PRINTF':         [BOARD_ID, Raw('string', 64)],

    'DEBUG_RADIO_CMD':      [BOARD_ID, ASCII('string', 64)],

    'ACTUATOR_STATUS':      [BOARD_ID, TIMESTAMP_3, Enum('actuator', 8, mt.actuator_id), Enum('cur_state', 8, mt.actuator_states), Enum('req_state', 8, mt.actuator_states)],
    'ALT_ARM_STATUS':       [BOARD_ID, TIMESTAMP_3, Enum('state', 4, mt.arm_states), Numeric('altimeter', 4), Numeric('drogue_v', 16), Numeric('main_v', 16)],
    'GENERAL_BOARD_STATUS': [BOARD_ID, TIMESTAMP_3, Switch('status', 8, mt.board_status, BOARD_STATUS), Numeric('data', 8, signed=False)],

    'SENSOR_TEMP':          [BOARD_ID, TIMESTAMP_3, SENSOR_ID, Numeric('temperature', 16, unit='°C', scale = 1/4, signed=True)],
    'SENSOR_ALTITUDE':      [BOARD_ID, TIMESTAMP_3, Numeric('altitude', 32, signed=True)],
    'SENSOR_ACC':           [BOARD_ID, TIMESTAMP_1, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'SENSOR_ACC2':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, scale=16/2**16, unit='m/s²', signed=True), Numeric('y', 16, scale=16/2**16, unit='m/s²', signed=True), Numeric('z', 16, scale=16/2**16, unit='m/s²', signed=True)],
    'SENSOR_GYRO':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, scale=2000/2**16, unit='°/s', signed=True), Numeric('y', 16, scale=2000/2**16, unit='°/s', signed=True), Numeric('z', 16, scale=2000/2**16, unit='°/s', signed=True)],
    'SENSOR_MAG':           [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='µT', signed=True), Numeric('y', 16, unit='µT', signed=True), Numeric('z', 16, unit='µT', signed=True)],
    'SENSOR_ANALOG':        [BOARD_ID, TIMESTAMP_3, Switch('sensor_id', 8, mt.sensor_id, ANALOG_CHANNELS)],
    'SENSOR_RPM':           [BOARD_ID, TIMESTAMP_3, Switch('sensor_id', 8, mt.sensor_id, RPM_CHANNELS)],
    'SENSOR_LEVEL':         [BOARD_ID, TIMESTAMP_3, SENSOR_ID],
    'SENSOR_A501':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'SENSOR_A502':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'SENSOR_A503':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'SENSOR_A504':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'SENSOR_A505':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'SENSOR_A506':          [BOARD_ID, TIMESTAMP_2, Numeric('x', 16, unit='m/s²', signed=True), Numeric('y', 16, unit='m/s²', signed=True), Numeric('z', 16, unit='m/s²', signed=True)],
    'FAKE_RPM':             [BOARD_ID, TIMESTAMP_3, SENSOR_ID, Numeric('rpm_counts', 32)],
    'SENSOR_SPOOF':         [BOARD_ID, SENSOR_ID, Numeric('value', 16, signed=False)],
    'CLEAR_SENSOR_SPOOF':   [BOARD_ID, SENSOR_ID],




    'GPS_TIMESTAMP':        [BOARD_ID, TIMESTAMP_3, Numeric('hrs', 8), Numeric('mins', 8), Numeric('secs', 8), Numeric('dsecs', 8)],
    'GPS_LATITUDE':         [BOARD_ID, TIMESTAMP_3, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_LONGITUDE':        [BOARD_ID, TIMESTAMP_3, Numeric('degs', 8), Numeric('mins', 8), Numeric('dmins', 16), ASCII('direction', 8)],
    'GPS_ALTITUDE':         [BOARD_ID, TIMESTAMP_3, Numeric('altitude', 16), Numeric('daltitude', 8), ASCII('unit', 8)],
    'GPS_INFO':             [BOARD_ID, TIMESTAMP_3, Numeric('num_sats', 8), Numeric('quality', 8)],

    'FILL_LVL':             [BOARD_ID, TIMESTAMP_3, Numeric('level', 8), Enum('direction', 8, mt.fill_direction)],

    'RADI_VALUE':           [BOARD_ID, TIMESTAMP_3, Numeric('radi_board', 8), Numeric('radi', 16)],

    'LEDS_ON':              [BOARD_ID],
    'LEDS_OFF':             [BOARD_ID]
}

# entire CAN message minus board_id 
# board_id is parsed seperately because if it throws, we want to continue parsing
CAN_MESSAGE = Switch('msg_type', MESSAGE_TYPE.length, mt.adjusted_msg_type, MESSAGES)
