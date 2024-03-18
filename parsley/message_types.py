"""
REMINDER: Any changes to this file should be reflected in canlib.

If canlib and this file differ, canlib is the source of truth.
"""
msg_type = {
    'GENERAL_CMD':          0x060,
    'ACTUATOR_CMD':         0x0C0,
    'ALT_ARM_CMD':          0x140,
    'RESET_CMD':            0x160,

    'DEBUG_MSG':            0x180,
    'DEBUG_PRINTF':         0x1E0,
    'DEBUG_RADIO_CMD':      0x200,

    'ALT_ARM_STATUS':       0x440,
    'ACTUATOR_STATUS':      0x460,
    'GENERAL_BOARD_STATUS': 0x520,

    'SENSOR_TEMP':          0x540,
    'SENSOR_ALTITUDE':      0x560,
    'SENSOR_ACC':           0x580,
    'SENSOR_ACC2':          0x5A0,
    'SENSOR_GYRO':          0x5E0,
    'SENSOR_MAG':           0x640,
    'SENSOR_ANALOG':        0x6A0,
    'MSG_SENSOR_RPM':       0x680,
    'MSG_SENSOR_LEVEL':     0x620,

    'GPS_TIMESTAMP':        0x6C0,
    'GPS_LATITUDE':         0x6E0,
    'GPS_LONGITUDE':        0x700,
    'GPS_ALTITUDE':         0x720,
    'GPS_INFO':             0x740,

    'FILL_LVL':             0x780,
    'RADI_VALUE':           0x7A0,

    'LEDS_ON':              0x7E0,
    'LEDS_OFF':             0x7C0
}

# canlib's msg_type is defined in 12-bit msg_sid form, so we need to
# right shift to get the adjusted (actual) 6-bit message type values
adjusted_msg_type = {k: v >> 5 for k, v in msg_type.items()}

board_id = {
    'ANY':                  0x00,
    'ACTUATOR_INJ':         0x01,
    'ACTUATOR_VENT':        0x02,
    'ACTUATOR_CAM1':        0x03,
    'ACTUATOR_CAM2':        0x04,
    'SENSOR_INJ':           0x05,
    'SENSOR_VENT':          0x06,
    'SENSOR_PAYLOAD':       0x07,
    'LOGGER':               0x08,
    'LOGGER_PAYLOAD':       0x09,
    'LOGGER_SPARE':         0x0A,
    'GPS':                  0x0B,
    'GPS_PAYLOAD':          0x0C,
    'GPS_SPARE':            0x0D,
    'CHARGING':             0x0E,
    'ARMING':               0x0F,
    'GRANDPAPA':            0x10,
    'KALMAN':               0x11,
    'TELEMETRY':            0x12,
    'USB':                  0x13,
    'RLCS':                 0x14
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

    'E_BUS_OVER_CURRENT':       0x01,
    'E_BUS_UNDER_VOLTAGE':      0x02,
    'E_BUS_OVER_VOLTAGE':       0x03,

    'E_BATT_OVER_CURRENT':      0x04,
    'E_BATT_UNDER_VOLTAGE':     0x05,
    'E_BATT_OVER_VOLTAGE':      0x06,

    'E_BOARD_FEARED_DEAD':      0x07,
    'E_NO_CAN_TRAFFIC':         0x08,
    'E_MISSING_CRITICAL_BOARD': 0x09,
    'E_RADIO_SIGNAL_LOST':      0x0A,

    'E_ACTUATOR_STATE':         0x0B,
    'E_CANNOT_INIT_DACS':       0x0C,
    'E_VENT_POT_RANGE':         0x0D,

    'E_LOGGING':                0x0E,
    'E_GPS':                    0x0F,
    'E_SENSOR':                 0x10,

    'E_ILLEGAL_CAN_MSG':        0x11,
    'E_SEGFAULT':               0x12,
    'E_UNHANDLED_INTERRUPT':    0x13,
    'E_CODING_FUCKUP':          0x14,
    'IRPTS_OUT':			0x15,
	'ICONT_OUT':			0x16,
	'IRPTS_IN':			0x17,
	'ICONT_IN':			0x18,
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

sensor_id = {
    'SENSOR_BUS_CURR':              0x00,
    'SENSOR_BATT_CURR':             0x01,
    'SENSOR_BATT_VOLT':             0x02,
    'SENSOR_CHARGE_CURR':           0x03,
    'SENSOR_GROUND_VOLT':           0x04,
    'SENSOR_PRESSURE_OX':           0x05,
    'SENSOR_PRESSURE_CC':           0x06,
    'SENSOR_PRESSURE_PNEUMATICS':   0x07,
    'SENSOR_BARO':                  0x08,
    'SENSOR_ARM_BATT_1':            0x09,
    'SENSOR_ARM_BATT_2':            0x0A,
    'SENSOR_MAG_1':                 0x0B,
    'SENSOR_MAG_2':                 0x0C,
    'SENSOR_VELOCITY':              0x0D,
    'SENSOR_VENT_TEMP':             0x0E,
    'SENSOR_RADIO_CURR':            0x0F,
	'ISENSE_24V':			0x12,
	'VSENSE_24V':			0x13,
	'ISENSE_12VD':			0x14,
	'VSENSE_12VD':			0x15,
	'ISENSE_12VA':			0x16,
	'VSENSE_12VA':			0x17,
	'ISENSE_5VD':			0x18,
	'VSENSE_5VD':			0x19,
	'ISENSE_5VA':			0x1a,
	'VSENSE_5VA':			0x1b,
	'ISENSE_3V3':			0x1c,
	'VSENSE_3V3':			0x1d,
	'RAW_ISENSE_5V':			0x1e,
	'RAW_ISENSE_12V':			0x1f,
	'RAW_ISENSE_24V':			0x20,
	'SPARE_1':			0x21,
	'C501':			0x22,
	'C502':			0x23,
	'GB_V':			0x24,
	'MB_V':			0x25,
	'GB_12V_I':			0x26,
	'MG_24V_I':			0x27,
	'MG_12V_I':			0x28,
	'MG_5V_I':			0x29,
	'MG_3V3_I':			0x2a,
	'MG_5VD_V':			0x2b,
	'MG_5VA_I':			0x2c,
	'MG_5VA_V':			0x2d,
	'MG_12VA_V':			0x2e,
	'MG_12VD_I':			0x2f,
	'MG_12VD_V':			0x30,
	'MG_3V3_V':			0x31,
	'P501':			0x32,
	'P502':			0x33,
	'P503':			0x34,
	'P504':			0x35,
	'P505':			0x36,
	'P506':			0x37,
	'P301':			0x38,
	'D501':			0x39,
	'D502':			0x3a,
	'SPARE_2':			0x3b,
	'SPARE_3':			0x3c,
	'SPARE_4':			0x3d,
	'SPARE_5':			0x3e,
	'SPARE_6':			0x3f,
	'SPARE_7':			0x40,
	'SPARE_8':			0x41,
	'A501':			0x53,
	'A502':			0x54,
	'A503':			0x55,
	'A504':			0x56,
	'PIN_T501':			0x63,
	'PIN_T502':			0x64,
	'PIN_T503':			0x65,
	'PIN_T504':			0x66,
	'PIN_T505':			0x67,
	'PIN_T506':			0x68,
	'PIN_T507':			0x69,
	'PIN_T508':			0x6a,
	'PIN_T509':			0x6b,
	'PIN_T510':			0x6c,
	'L201':			0x58,
	'L401':			0x59,
	'L402':			0x5a,
	'RPM501':			0x5c,
	'RPM502':			0x5d,


}

fill_direction = {
    'FILLING':  0x00,
    'EMPTYING': 0x01
}

actuator_id = {
	'VA101':			0x0,
	'VA201':			0x1,
	'VA102':			0x2,
	'VA202':			0x3,
	'VA301':			0x4,
	'VA302':			0x5,
	'VA303':			0x6,
	'VA304':			0x7,
	'VA401':			0x8,
	'VA_SPARE1':			0x9,
	'VA_SPARE2':			0xa,
	'VA_SPARE3':			0xb,
}
