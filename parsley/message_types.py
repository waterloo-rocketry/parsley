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
    'ACT_ANALOG_CMD':       0x220,
     
    'ALT_ARM_STATUS':       0x440,
    'ACTUATOR_STATUS':      0x460,
    'GENERAL_BOARD_STATUS': 0x520,

    'SENSOR_TEMP':          0x540,
    'SENSOR_ALTITUDE':      0x560,
    'SENSOR_ACC':           0x580,
    'SENSOR_ACC2':          0x5A0,
    'SENSOR_GYRO':          0x5E0,

    'STATE_EST_CALIB':      0x620,
    'SENSOR_MAG':           0x640,
    'SENSOR_ANALOG':        0x6A0,
    'GPS_TIMESTAMP':        0x6C0,
    'GPS_LATITUDE':         0x6E0,
    'GPS_LONGITUDE':        0x700,
    'GPS_ALTITUDE':         0x720,
    'GPS_INFO':             0x740,

    'FILL_LVL':             0x780,
    'STATE_EST_DATA':       0x7A0,

    'LEDS_ON':              0x7E0,
    'LEDS_OFF':             0x7C0
}

# canlib's msg_type is defined in 12-bit msg_sid form, so we need to
# right shift to get the adjusted (actual) 6-bit message type values
adjusted_msg_type = {k: v >> 5 for k, v in msg_type.items()}

board_id = {
    'ANY':                  0x00,
    # Ground Side
    'DAQ':                  0x01,
    'THERMOCOUPLE_1':       0x02,
    'THERMOCOUPLE_2':       0x03,
    'THERMOCOUPLE_3':       0x04,
    'THERMOCOUPLE_4':       0x05,
    # Injector/Fill Section
    'PROPULSION_INJ':       0x06,
    # Vent Section
    'PROPULSION_VENT':      0x07,
    'CAMERA_1':             0x08,
    'CAMERA_2':             0x09,
    # Airbrake Section
    'CHARGING_AIRBRAKE':    0x0A,
    # Payload Section
    'CHARGING_PAYLOAD':     0x0B,
    'VIBRATION':            0x0C,
    # Recovery Electronics(RecElec) Sled
    'CHARGING_CAN':         0x0D,
    'LOGGER':               0x0E,
    'PROCESSOR':            0x0F,
    'GPS':                  0x10,
    'ARMING':               0x11,
    'TELEMETRY':            0x12,
    'CAMERA_3':             0x13,
    # Debug
    'USB':                  0x14
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

    'E_ILLEGAL_CAN_MSG':        0x13,
    'E_SEGFAULT':               0x14,
    'E_UNHANDLED_INTERRUPT':    0x15,
    'E_CODING_FUCKUP':          0x16
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
    'SENSOR_PAYLOAD_TEMP_1':        0x16,
    'SENSOR_PAYLOAD_TEMP_2':        0x17,
    'SENSOR_9V_BATT_CURR_1':        0x18,
    'SENSOR_9V_BATT_CURR_1':        0x19
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
    'ACTUATOR_CHARGE':           0x06,
    'ACTUATOR_RADIO':            0x07,
    'ACTUATOR_PAYLOAD_SERVO':    0x08,
    'ACTUATOR_AIRBRAKES_SERVO':  0x09,
    'ACTUATOR_AIRBRAKES_ENABLE': 0x0A,
    'ACTUATOR_ROCKET_POWER':     0x0B
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
    'STATE_RATE_ROLL':   0x0E
}
