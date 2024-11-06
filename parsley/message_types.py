"""
REMINDER: Any changes to this file should be reflected in canlib.

If canlib and this file differ, canlib is the source of truth.
"""

msg_prio = {
    'HIGHEST': 0x0,
    'HIGH':    0x1,
    'MEDIUM':  0x2,
    'LOW':     0x3
}

msg_type = {
    'GENERAL_CMD':          0x001,
    'ACTUATOR_CMD':         0x002,
    'ALT_ARM_CMD':          0x003,
    'RESET_CMD':            0x004,

    'DEBUG_MSG':            0x005,
    'DEBUG_PRINTF':         0x006,
    'DEBUG_RADIO_CMD':      0x007,
    'ACT_ANALOG_CMD':       0x008,
     
    'ALT_ARM_STATUS':       0x009,
    'ACTUATOR_STATUS':      0x00A,
    'GENERAL_BOARD_STATUS': 0x00B,

    'SENSOR_TEMP':          0x00C,
    'SENSOR_ALTITUDE':      0x00D,
    'SENSOR_ACC':           0x00E,
    'SENSOR_ACC2':          0x00F,
    'SENSOR_GYRO':          0x010,

    'STATE_EST_CALIB':      0x011,
    'SENSOR_MAG':           0x012,
    'SENSOR_ANALOG':        0x013,
    'GPS_TIMESTAMP':        0x014,
    'GPS_LATITUDE':         0x015,
    'GPS_LONGITUDE':        0x016,
    'GPS_ALTITUDE':         0x017,
    'GPS_INFO':             0x018,

    'FILL_LVL':             0x019,
    'STATE_EST_DATA':       0x01A,

    'LEDS_ON':              0x01B,
    'LEDS_OFF':             0x01C
}

board_type_id = {
    'ANY': 0x00,

    'INJ_SENSOR':   0x01,
    'CANARD_MOTOR': 0x02,
    'CAMERA':       0x03,
    'ROCKET_POWER': 0x04,
    'LOGGER':       0x05,
    'PROCESSOR':    0x06,
    'TELEMETRY':    0x07,
    'GPS':          0x08,
    'SRAD_GNSS':    0x09,
    'ALTIMETER':    0x0A,
    'ARMING':       0x0B,

    'PAY_SENSOR':   0x40,
    'PAY_MOTOR':    0x41,

    'RLCS_GLS':     0x80,
    'RLCS_RELAY':   0x81,
    'RLCS_HEATING': 0x82,
    'DAQ':          0x83,
    'CHARGING':     0x84,
    'THERMOCOUPLE': 0x85,
    'USB':          0x86
}

board_inst_id = {
    'ANY':      0x00,
    'GENERIC':  0x01,
    'ROCKET':   0x02,
    'PAYLOAD':  0x03,
    'INJ_A':    0x04,
    'INJ_B':    0x05,
    'VENT_A':   0x06,
    'VENT_B':   0x07,
    'VENT_C':   0x08,
    'VENT_D':   0x09,
    'RECOVERY': 0x0A,
    '1':        0x0B,
    '2':        0x0C,
    '3':        0x0D,
    '4':        0x0E
}

gen_cmd = {
    'BUS_DOWN_WARNING': 0x00
}

actuator_states = {
    'ACTUATOR_ON':      0x00,
    'ACTUATOR_OFF':     0x01,
    'ACTUATOR_UNK':     0x02,
    'ACTUATOR_ILLEGAL': 0x03
}

arm_states = {
    'DISARMED': 0x00,
    'ARMED':    0x01
}

board_status = {
    'E_NOMINAL':                0x00,

    'E_5V_OVER_CURRENT':        0x01,
    'E_5V_UNDER_VOLTAGE':       0x02,
    'E_5V_OVER_VOLTAGE':        0x03,

    'E_BATT_OVER_CURRENT':      0x04,
    'E_BATT_UNDER_VOLTAGE':     0x05,
    'E_BATT_OVER_VOLTAGE':      0x06,

    'E_13V_OVER_CURRENT':       0x07,
    'E_MOTOR_OVER_CURRENT':     0x08,

    'E_BOARD_FEARED_DEAD':      0x09,
    'E_NO_CAN_TRAFFIC':         0x0A,
    'E_MISSING_CRITICAL_BOARD': 0x0B,
    'E_RADIO_SIGNAL_LOST':      0x0C,

    'E_ACTUATOR_STATE':         0x0D,
    'E_CANNOT_INIT_DACS':       0x0E,
    'E_VENT_POT_RANGE':         0x0F,

    'E_LOGGING':                0x10,
    'E_GPS':                    0x11,
    'E_SENSOR':                 0x12,
    'E_VIDEO':                  0x13,

    'E_ILLEGAL_CAN_MSG':        0x14,
    'E_SEGFAULT':               0x15,
    'E_UNHANDLED_INTERRUPT':    0x16,
    'E_CODING_FUCKUP':          0x17
}

logger_error = {
    # SD card related failures
    'E_SD_NONE':                        0x00,
    'E_SD_FAIL_READ_BLOCK':             0x01,
    'E_SD_FAIL_GO_IDLE':                0x02,
    'E_SD_FAIL_SEND_IF_COND':           0x03,
    'E_SD_FAIL_VOLTAGE_CHECK':          0x04,
    'E_SD_FAIL_FS_INIT':                0x05,
    'E_SD_FAIL_READ_FILE':              0x06,
    'E_SD_FAIL_UNIMPLEMENTED_FUNCTION': 0x07,
    'E_SD_FAIL_WRITE_BLOCK':            0x08,
    'E_SD_FAIL_OPEN_FILE':              0x09,
    'E_SD_FAIL_WRITE_DATA_RESP':        0x0A,
    # syslog related failures
    'E_SYSLOG_ALL_BUFFERS_FULL':        0x0B
}

video_state = {
    'VIDEO_OFF':      0x00,
    'VIDEO_ON':       0x01,
    'VIDEO_ERR_SD':   0x02,
    'VIDEO_ERR_CAM':  0x03
}

sensor_id = {
    'SENSOR_5V_CURR':               0x00,
    'SENSOR_BATT_CURR':             0x01,
    'SENSOR_BATT_VOLT':             0x02,
    'SENSOR_CHARGE_CURR':           0x03,
    'SENSOR_13V_CURR':              0x04,
    'SENSOR_MOTOR_CURR':            0x05,
    'SENSOR_GROUND_VOLT':           0x06,
    'SENSOR_PRESSURE_OX':           0x07,
    'SENSOR_PRESSURE_FUEL':         0x08,
    'SENSOR_PRESSURE_CC':           0x09,
    'SENSOR_PRESSURE_PNEUMATICS':   0x0A,
    'SENSOR_HALL_OX_INJ':           0x0B,
    'SENSOR_HALL_FUEL_INJ':         0x0C,
    'SENSOR_HALL_FILL':             0x0D,
    'SENSOR_BARO':                  0x0E,
    'SENSOR_ARM_BATT_1':            0x0F,
    'SENSOR_ARM_BATT_2':            0x10,
    'SENSOR_MAG_1':                 0x11,
    'SENSOR_MAG_2':                 0x12,
    'SENSOR_VELOCITY':              0x13,
    'SENSOR_VENT_TEMP':             0x14,
    'SENSOR_RADIO_CURR':            0x15,
    'SENSOR_PAYLOAD_TEMP':          0x16,
    'SENSOR_PAYLOAD_FLOW_RATE':     0x17,
    'SENSOR_9V_BATT_CURR_1':        0x18,
    'SENSOR_9V_BATT_CURR_2':        0x19,
    'SENSOR_FPS':                   0x1A
}

fill_direction = {
    'FILLING':  0x00,
    'EMPTYING': 0x01
}

actuator_id = {
    'ACTUATOR_VENT_VALVE':       0x00,
    'ACTUATOR_INJECTOR_VALVE':   0x01,
    'ACTUATOR_FILL_DUMP_VALVE':  0x02,
    'ACTUATOR_CAMERA_1':         0x03,
    'ACTUATOR_CAMERA_2':         0x04,
    'ACTUATOR_CANBUS':           0x05,
    'ACTUATOR_CHARGE_CAN':       0x06,
    'ACTUATOR_RADIO':            0x07,
    'ACTUATOR_PAYLOAD_SERVO':    0x08,
    'ACTUATOR_AIRBRAKES_SERVO':  0x09,
    'ACTUATOR_AIRBRAKES_ENABLE': 0x0A,
    'ACTUATOR_ROCKET_POWER':     0x0B,
    'ACTUATOR_OX_INJECTOR':      0x0C,
    'ACTUATOR_FUEL_INJECTOR':    0x0D,
    'ACTUATOR_CHARGE_AIRBRAKE':  0x0E,
    'ACTUATOR_CHARGE_PAYLOAD':   0x0F
}

state_id = {
    'STATE_POS_X':       0x00,
    'STATE_POS_Y':       0x01,
    'STATE_POS_Z':       0x02,
    'STATE_VEL_X':       0x03,
    'STATE_VEL_Y':       0x04,
    'STATE_VEL_Z':       0x05,
    'STATE_ACC_X':       0x06,
    'STATE_ACC_Y':       0x07,
    'STATE_ACC_Z':       0x08,
    'STATE_ANGLE_YAW':   0x09,
    'STATE_ANGLE_PITCH': 0x0A,
    'STATE_ANGLE_ROLL':  0x0B,
    'STATE_RATE_YAW':    0x0C,
    'STATE_RATE_PITCH':  0x0D,
    'STATE_RATE_ROLL':   0x0E,
    'STATE_FILTER_YAW':  0x0F,
    'STATE_FILTER_PITCH':0x10, 
    'STATE_FILTER_ROLL': 0x11
}
