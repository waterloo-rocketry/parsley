"""
REMINDER: Any changes to this file should be reflected in canlib.

If canlib and this file differ, canlib is the source of truth.
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

# canlib's msg_type is defined in 12-bit msg_sid form, so we need to
# right shift to get the adjusted (actual) 6-bit message type values
adjusted_msg_type = {k: v >> 5 for k, v in msg_type.items()}

board_id = {
    "ANY":                  0x00,
    "ACTUATOR_INJ":         0x01,
    "ACTUATOR_VENT":        0x02,
    "ACTUATOR_CAM1":        0x03,
    "ACTUATOR_CAM2":        0x04,
    "SENSOR_INJ":           0x05,
    "SENSOR_VENT":          0x06,
    "SENSOR_PAYLOAD":       0x07,
    "LOGGER":               0x08,
    "LOGGER_PAYLOAD":       0x09,
    "LOGGER_SPARE":         0x0A,
    "GPS":                  0x0B,
    "GPS_PAYLOAD":          0x0C,
    "GPS_SPARE":            0x0D,
    "CHARGING":             0x0E,
    "ARMING":               0x0F,
    "GRANDPAPA":            0x10,
    "KALMAN":               0x11,
    "TELEMETRY":            0x12,
    "USB":                  0x13,
    "RLCS":                 0x14
}

gen_cmd = {
    "BUS_DOWN_WARNING": 0x00
}

actuator_states = {
    "ACTUATOR_ON":      0x00,
    "ACTUATOR_OFF":     0x01,
    "ACTUATOR_UNK":     0x02,
    "ACTUATOR_ILLEGAL": 0x03
}

arm_states = {
    "DISARMED": 0x00,
    "ARMED":    0x01
}

board_status = {
    "E_NOMINAL":                0x00,

    "E_BUS_OVER_CURRENT":       0x01,
    "E_BUS_UNDER_VOLTAGE":      0x02,
    "E_BUS_OVER_VOLTAGE":       0x03,

    "E_BATT_OVER_CURRENT":      0x05,
    "E_BATT_UNDER_VOLTAGE":     0x06,
    "E_BATT_OVER_VOLTAGE":      0x07,

    "E_BOARD_FEARED_DEAD":      0x08,
    "E_NO_CAN_TRAFFIC":         0x09,
    "E_MISSING_CRITICAL_BOARD": 0x0A,
    "E_RADIO_SIGNAL_LOST":      0x0B,

    "E_ACTUATOR_STATE":         0x0C,
    "E_CANNOT_INIT_DACS":       0x0D,
    "E_VENT_POT_RANGE":         0x0E,

    "E_LOGGING":                0x0F,
    "E_GPS":                    0x10,
    "E_SENSOR":                 0x11,

    "E_ILLEGAL_CAN_MSG":        0x12,
    "E_SEGFAULT":               0x13,
    "E_UNHANDLED_INTERRUPT":    0x14,
    "E_CODING_FUCKUP":          0x15
}

logger_error = {
    # SD card related failures
    "E_SD_NONE":                        0x00,
    "E_SD_FAIL_READ_BLOCK":             0x01,
    "E_SD_FAIL_GO_IDLE":                0x02,
    "E_SD_FAIL_SEND_IF_COND":           0x03,
    "E_SD_FAIL_VOLTAGE_CHECK":          0x04,
    "E_SD_FAIL_FS_INIT":                0x05,
    "E_SD_FAIL_READ_FILE":              0x06,
    "E_SD_FAIL_UNIMPLEMENTED_FUNCTION": 0x07,
    "E_SD_FAIL_WRITE_BLOCK":            0x08,
    "E_SD_FAIL_OPEN_FILE":              0x09,
    "E_SD_FAIL_WRITE_DATA_RESP":        0x0A,
    # syslog related failures
    "E_SYSLOG_ALL_BUFFERS_FULL":        0x0B
}

sensor_id = {
    "SENSOR_BUS_CURR":              0x00,
    "SENSOR_BATT_CURR":             0x01,
    "SENSOR_BATT_VOLT":             0x02,
    "SENSOR_CHARGE_CURR":           0x03,
    "SENSOR_CHARGE_VOLT":           0x04,
    "SENSOR_PRESSURE_OX":           0x05,
    "SENSOR_PRESSURE_CC":           0x06,
    "SENSOR_PRESSURE_PNEUMATICS":   0x07,
    "SENSOR_BARO":                  0x08,
    "SENSOR_ARM_BATT_1":            0x09,
    "SENSOR_ARM_BATT_2":            0x0A,
    "SENSOR_MAG_1":                 0x0B,
    "SENSOR_MAG_2":                 0x0C,
    "SENSOR_VELOCITY":              0x0D,
    "SENSOR_VENT_TEMP":             0x0E
}

fill_direction = {
    "FILLING":  0x00,
    "EMPTYING": 0x01
}

actuator_id = {
    "ACTUATOR_VENT_VALVE":      0x00,
    "ACTUATOR_INJECTOR_VALVE":  0x01,
    "ACTUATOR_PAYLOAD":         0x02,
    "ACTUATOR_CAMERAS":         0x03,
    "ACTUATOR_CANBUS":          0x04
}
