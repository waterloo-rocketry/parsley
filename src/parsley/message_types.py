# Auto generated file, do not edit directly

msg_prio = {
    'HIGHEST': 0x0,
    'HIGH':    0x1,
    'MEDIUM':  0x2,
    'LOW':     0x3
}

msg_type = {
    'UNDEFINED':            0x000,
    'GENERAL_BOARD_STATUS': 0x001,
    'RESET_CMD':            0x002,
    'DEBUG_RAW':            0x003,
    'CONFIG_SET':           0x004,
    'CONFIG_STATUS':        0x005,
    'ACTUATOR_CMD':         0x006,
    'ACTUATOR_ANALOG_CMD':  0x007,
    'ACTUATOR_STATUS':      0x008,
    'ALT_ARM_CMD':          0x009,
    'ALT_ARM_STATUS':       0x00A,
    'SENSOR_ALTITUDE':      0x00B,
    'SENSOR_IMU_X':         0x00C,
    'SENSOR_IMU_Y':         0x00D,
    'SENSOR_IMU_Z':         0x00E,
    'SENSOR_MAG_X':         0x00F,
    'SENSOR_MAG_Y':         0x010,
    'SENSOR_MAG_Z':         0x011,
    'SENSOR_BARO':          0x012,
    'SENSOR_ANALOG':        0x013,
    'GPS_TIMESTAMP':        0x014,
    'GPS_LATITUDE':         0x015,
    'GPS_LONGITUDE':        0x016,
    'GPS_ALTITUDE':         0x017,
    'GPS_INFO':             0x018,
    'STATE_EST_DATA':       0x019,
    'STREAM_STATUS':        0x01A,
    'STREAM_DATA':          0x01B,
    'STREAM_RETRY':         0x01C,
    'LEDS_ON':              0x01D,
    'LEDS_OFF':             0x01E,
}

board_type_id = {
    'ANY':                  0x00,
    'INJ_SENSOR':           0x01,
    'CANARD_MOTOR':         0x02,
    'CAMERA':               0x03,
    'POWER':                0x04,
    'LOGGER':               0x05,
    'PROCESSOR':            0x06,
    'TELEMETRY':            0x07,
    'GPS':                  0x08,
    'SRAD_GNSS':            0x09,
    'ALTIMETER':            0x0A,
    'ARMING':               0x0B,
    'PHESEUS':              0x0C,
    'PAY_SENSOR':           0x40,
    'PAY_MOTOR':            0x41,
    'RLCS_GLS':             0x80,
    'RLCS_RELAY':           0x81,
    'DAQ':                  0x82,
}

board_inst_id = {
    'ANY':         0x00,
    'GROUND':      0x01,
    'ROCKET':      0x02,
    'PAYLOAD':     0x03,
    'PRIMARY':     0x04,
    'FAILSAFE':    0x05,
    'CANARD_A':    0x06,
    'CANARD_B':    0x07,
    'RECOVERY':    0x08,
}

actuator_id = {
    'ACTUATOR_OX_INJECTOR_VALVE':      0x00,
    'ACTUATOR_FUEL_INJECTOR_VALVE':    0x01,
    'ACTUATOR_ROCKET_CHARGE_ENABLE':   0x02,
    'ACTUATOR_PAYLOAD_CHARGE_ENABLE':  0x03,
    'ACTUATOR_5V_RAIL_ROCKET':         0x04,
    'ACTUATOR_5V_RAIL_PAYLOAD':        0x05,
    'ACTUATOR_12V_RAIL_ROCKET':        0x06,
    'ACTUATOR_12V_RAIL_PAYLOAD':       0x07,
    'ACTUATOR_TELEMETRY':              0x08,
    'ACTUATOR_CAMERA_CANARD_A':        0x09,
    'ACTUATOR_CAMERA_CANARD_B':        0x0A,
    'ACTUATOR_CAMERA_RECOVERY':        0x0B,
    'ACTUATOR_CAMERA_PAYLOAD':         0x0C,
    'ACTUATOR_PROC_ESTIMATOR_INIT':    0x0D,
    'ACTUATOR_SRAD_ALT_ESTIMATOR_INIT':0x0E,
    'ACTUATOR_SRAD_ALT_GPS_RESET':     0x0F,
    'ACTUATOR_CANARD_ENABLE':          0x10,
    'ACTUATOR_CANARD_ANGLE':           0x11,
    'ACTUATOR_CAMERA_CAPTURE':         0x12,
    'ACTUATOR_PAYLOAD_LOGGING_ENABLE': 0x13,
    'ACTUATOR_THESEUS_ACTUATOR_1':     0x14,
    'ACTUATOR_THESEUS_ACTUATOR_2':     0x15,
    'ACTUATOR_RLCS_RELAY_POWER':       0x16,
    'ACTUATOR_RLCS_RELAY_SELECT':      0x17,
}

actuator_state = {
    'ACT_STATE_ON':                    0x00,
    'ACT_STATE_OFF':                   0x01,
    'ACT_STATE_UNK':                   0x02,
    'ACT_STATE_ILLEGAL':               0x03,
}

altimeter_id = {
    'ALTIMETER_ROCKET_RAVEN':          0x00,
    'ALTIMETER_ROCKET_STRATOLOGGER':   0x01,
    'ALTIMETER_ROCKET_SRAD':           0x02,
    'ALTIMETER_PAYLOAD_RAVEN':         0x03,
    'ALTIMETER_PAYLOAD_STRATOLOGGER':  0x04,
}

alt_arm_state = {
    'ALT_ARM_STATE_DISARMED':          0x00,
    'ALT_ARM_STATE_ARMED':             0x01,
}

imu_id = {
    'IMU_PROC_ALTIMU10':               0x00,
    'IMU_PROC_MTI630':                 0x01,
    'IMU_PROC_LSM6DSO32':              0x02,
    'IMU_SRAD_ALT_ALTIMU10':           0x03,
}

analog_sensor_id = {
    'SENSOR_5V_VOLT':                  0x00,
    'SENSOR_5V_CURR':                  0x01,
    'SENSOR_12V_VOLT':                 0x02,
    'SENSOR_12V_CURR':                 0x03,
    'SENSOR_CHARGE_VOLT':              0x04,
    'SENSOR_CHARGE_CURR':              0x05,
    'SENSOR_BATT_VOLT':                0x06,
    'SENSOR_BATT_CURR':                0x07,
    'SENSOR_MOTOR_CURR':               0x08,
    'SENSOR_RADIO_CURR':               0x09,
    'SENSOR_GPS_CURR':                 0x0A,
    'SENSOR_LOCAL_CURR':               0x0B,
    'SENSOR_PT_CHANNEL_1':             0x0C,
    'SENSOR_PT_CHANNEL_2':             0x0D,
    'SENSOR_PT_CHANNEL_3':             0x0E,
    'SENSOR_PT_CHANNEL_4':             0x0F,
    'SENSOR_PT_CHANNEL_5':             0x10,
    'SENSOR_HALL_CHANNEL_1':           0x11,
    'SENSOR_HALL_CHANNEL_2':           0x12,
    'SENSOR_HALL_CHANNEL_3':           0x13,
    'SENSOR_BARO_PRESSURE':            0x14,
    'SENSOR_BARO_TEMP':                0x15,
    'SENSOR_RA_BATT_VOLT_1':           0x16,
    'SENSOR_RA_BATT_VOLT_2':           0x17,
    'SENSOR_RA_BATT_CURR_1':           0x18,
    'SENSOR_RA_BATT_CURR_2':           0x19,
    'SENSOR_RA_MAG_VOLT_1':            0x1A,
    'SENSOR_RA_MAG_VOLT_2':            0x1B,
    'SENSOR_FPS':                      0x1C,
    'SENSOR_CANARD_ENCODER_1':         0x1D,
    'SENSOR_CANARD_ENCODER_2':         0x1E,
    'SENSOR_PROC_FLIGHT_PHASE_STATUS': 0x1F,
    'SENSOR_PAYLOAD_LIM_1':            0x20,
    'SENSOR_PAYLOAD_LIM_2':            0x21,
    'SENSOR_PAYLOAD_SERVO_DIRECTION':  0x22,
    'SENSOR_PAYLOAD_INFRARED':         0x23,
    'SENSOR_THESEUS_TEMP_1':           0x24,
    'SENSOR_THESEUS_TEMP_2':           0x25,
    'SENSOR_THESEUS_TEMP_3':           0x26,
    'SENSOR_RLCS_RELAY_OUTPUT_VOLT_A': 0x27,
    'SENSOR_RLCS_RELAY_OUTPUT_VOLT_B': 0x28,
    'SENSOR_RLCS_RELAY_OUTPUT_CURR_A': 0x29,
    'SENSOR_RLCS_RELAY_OUTPUT_CURR_B': 0x2A,
    'SENSOR_RLCS_RELAY_LIM_VOLT_A':    0x2B,
    'SENSOR_RLCS_RELAY_LIM_VOLT_B':    0x2C,
}

state_est_id = {
    'STATE_ID_ATT_Q0':                 0x00,
    'STATE_ID_ATT_Q1':                 0x01,
    'STATE_ID_ATT_Q2':                 0x02,
    'STATE_ID_ATT_Q3':                 0x03,
    'STATE_ID_RATE_WX':                0x04,
    'STATE_ID_RATE_WY':                0x05,
    'STATE_ID_RATE_WZ':                0x06,
    'STATE_ID_VEL_VX':                 0x07,
    'STATE_ID_VEL_VY':                 0x08,
    'STATE_ID_VEL_VZ':                 0x09,
    'STATE_ID_ALT':                    0x0A,
    'STATE_ID_COEFF_CL':               0x0B,
    'STATE_ID_CANARD_ANGLE':           0x0C,
}

apogee_state = {
    'APOGEE_UNKNOWN':                  0x00,
    'APOGEE_NOT_REACHED':              0x01,
    'APOGEE_REACHED':                  0x02,
}

general_board_status_offset = {
    'E_5V_OVER_CURRENT':   0x00,
    'E_5V_OVER_VOLTAGE':   0x01,
    'E_5V_UNDER_VOLTAGE':  0x02,
    'E_12V_OVER_CURRENT':  0x03,
    'E_12V_OVER_VOLTAGE':  0x04,
    'E_12V_UNDER_VOLTAGE': 0x05,
    'E_BATT_OVER_CURRENT': 0x06,
    'E_BATT_OVER_VOLTAGE': 0x07,
    'E_BATT_UNDER_VOLTAGE':0x08,
    'E_MOTOR_OVER_CURRENT':0x09,
    'E_IO_ERROR':          0x0A,
    'E_FS_ERROR':          0x0B,
    'E_WATCHDOG_TIMEOUT':  0x0C,
}

board_specific_status_offset = {
    'E_12V_EFUSE_FAULT':   0x00,
    'E_5V_EFUSE_FAULT':    0x01,
    'E_PT_OUT_OF_RANGE':   0x02,
}

