"""
Everything defined here tracks the information from canlib
If this file and canlib differ, canlib is the source of truth.
"""

msg_type = {
    "GENERAL_CMD":          0x060,
    "ACTUATOR_CMD":         0x0C0,
    "ALT_ARM_CMD":          0x140,
    "RESET_CMD":            0x160,

    "DEBUG_MSG":            0x180,
    "DEBUG_PRINTF":         0x1E0,
    "DEBUG_RADIO_CMD":      0x200,

    "ALT_ARM_STATUS":       0x440,
    "ACTUATOR_STATUS":      0x460,
    "GENERAL_BOARD_STATUS": 0x520,

    "SENSOR_TEMP":          0x540,
    "SENSOR_ALTITUDE":      0x560,
    "SENSOR_ACC":           0x580,
    "SENSOR_ACC2":          0x5A0,
    "SENSOR_GYRO":          0x5E0,
    "SENSOR_MAG":           0x640,
    "SENSOR_ANALOG":        0x6A0,

    "GPS_TIMESTAMP":        0x6C0,
    "GPS_LATITUDE":         0x6E0,
    "GPS_LONGITUDE":        0x700,
    "GPS_ALTITUDE":         0x720,
    "GPS_INFO":             0x740,

    "FILL_LVL":             0x780,

    "RADI_VALUE":           0x7A0,

    "LEDS_ON":              0x7E0,
    "LEDS_OFF":             0x7C0
}

board_id = {
    "ANY":                  0x00,
    "INJECTOR":             0x01,
    "INJECTOR_SPARE":       0x02,
    "LOGGER":               0x03,
    "LOGGER_SPARE":         0x04,
    "RADIO":                0x05,
    "RADIO_SPARE":          0x06,
    "SENSOR":               0x07,
    "SENSOR_SPARE":         0x08,
    "USB":                  0x09,
    "USB_SPARE":            0x0A,
    "VENT":                 0x0B,
    "VENT_SPARE":           0x0C,
    "GPS":                  0x0D,
    "GPS_SPARE":            0x0E,
    "FILL":                 0x0F,
    "FILL_SPARE":           0x10,
    "ARMING":               0x11,
    "ARMING_SPARE":         0X12,
    "PAPA":                 0x13,
    "PAPA_SPARE":           0x14,
    "ROCKET_PI":            0x15,
    "ROCKET_PI_2":          0x16,
    "ROCLET_PI_SPARE":      0x17,
    "ROCKET_PI_2_SPARE":    0x18,
    "SENSOR_2":             0x19,
    "SENSOR_2_SPARE":       0x1A,
    "SENSOR_3":             0x1B,
    "SENSOR_4":             0x1C,
    "LOGGER_2":             0x1D,
    "RLCS":                 0x1E
}

gen_cmd = {
    "BUS_DOWN_WARNING": 0
}

actuator_states = {
    "ACTUATOR_OPEN":  0,
    "ACTUATOR_CLOSED": 1,
    "ACTUATOR_UNK": 2,
    "ACTUATOR_ILLEGAL": 3
}

arm_states = {
    "DISARMED": 0,
    "ARMED": 1
}

board_status = {
    "E_NOMINAL": 0,

    "E_BUS_OVER_CURRENT": 1,
    "E_BUS_UNDER_VOLTAGE": 2,
    "E_BUS_OVER_VOLTAGE": 3,

    "E_BATT_UNDER_VOLTAGE": 4,
    "E_BATT_OVER_VOLTAGE": 5,

    "E_BOARD_FEARED_DEAD": 6,
    "E_NO_CAN_TRAFFIC": 7,
    "E_MISSING_CRITICAL_BOARD": 8,
    "E_RADIO_SIGNAL_LOST": 9,

    "E_ACTUATOR_STATE": 10,
    "E_CANNOT_INIT_DACS": 11,
    "E_VENT_POT_RANGE": 12,

    "E_LOGGING": 13,
    "E_GPS": 14,
    "E_SENSOR": 15,

    "E_ILLEGAL_CAN_MSG": 16,
    "E_SEGFAULT": 17,
    "E_UNHANDLED_INTERRUPT": 18,
    "E_CODING_FUCKUP": 19,

    "E_BATT_OVER_CURRENT": 20
}

logger_error = {
    # SD card related failures
    "E_SD_NONE": 0,
    "E_SD_FAIL_READ_BLOCK": 1,
    "E_SD_FAIL_GO_IDLE": 2,
    "E_SD_FAIL_SEND_IF_COND": 3,
    "E_SD_FAIL_VOLTAGE_CHECK": 4,
    "E_SD_FAIL_FS_INIT": 5,
    "E_SD_FAIL_READ_FILE": 6,
    "E_SD_FAIL_UNIMPLEMENTED_FUNCTION": 7,
    "E_SD_FAIL_WRITE_BLOCK": 8,
    "E_SD_FAIL_OPEN_FILE": 9,
    "E_SD_FAIL_WRITE_DATA_RESP": 10,
    # syslog related failures
    "E_SYSLOG_ALL_BUFFERS_FULL": 11
}

sensor_id = {
    "SENSOR_IMU1": 0,
    "SENSOR_IMU2": 1,
    "SENSOR_BARO": 2,
    "SENSOR_PRESSURE_OX": 3,
    "SENSOR_PRESSURE_CC": 4,
    "SENSOR_VENT_BATT": 5,
    "SENSOR_INJ_BATT": 6,
    "SENSOR_ARM_BATT_1": 7,
    "SENSOR_ARM_BATT_2": 8,
    "SENSOR_BATT_CURR": 9,
    "SENSOR_BUS_CURR": 10,
    "SENSOR_VELOCITY": 11,
    "SENSOR_MAG_1": 12,
    "SENSOR_MAG_2": 13,
    "SENSOR_ROCKET_BATT": 14,
    "SENSOR_PRESSURE_PNEUMATICS": 15,
    "SENSOR_VENT_TEMP": 16,
    "SENSOR_PICAM_CURRENT": 17
}

fill_direction = {
    "FILLING": 0,
    "EMPTYING": 1
}

actuator_id = {
    "ACTUATOR_VENT_VALVE": 0,
    "ACTUATOR_INJECTOR_VALVE": 1,
    "MAMA_BOARD_ACTIVATE": 2,
    "PICAM": 3,
    "CANBUS": 4
}
