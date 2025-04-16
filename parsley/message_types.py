# Auto generated file, do not edit directly

msg_prio = {
    'HIGHEST': 0x0,
    'HIGH':    0x1,
    'MEDIUM':  0x2,
    'LOW':     0x3
}

msg_type = {
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
    'SENSOR_TEMP':          0x00B,
    'SENSOR_ALTITUDE':      0x00C,
    'SENSOR_IMU_X':         0x00D,
    'SENSOR_IMU_Y':         0x00E,
    'SENSOR_IMU_Z':         0x00F,
    'SENSOR_MAG_X':         0x010,
    'SENSOR_MAG_Y':         0x011,
    'SENSOR_MAG_Z':         0x012,
    'SENSOR_BARO':          0x013,
    'SENSOR_ANALOG':        0x014,
    'GPS_TIMESTAMP':        0x015,
    'GPS_LATITUDE':         0x016,
    'GPS_LONGITUDE':        0x017,
    'GPS_ALTITUDE':         0x018,
    'GPS_INFO':             0x019,
    'STATE_EST_DATA':       0x01A,
    'LEDS_ON':              0x01B,
    'LEDS_OFF':             0x01C,
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
    'PAY_SENSOR':           0x40,
    'PAY_MOTOR':            0x41,
    'RLCS_GLS':             0x80,
    'RLCS_RELAY':           0x81,
    'RLCS_HEATING':         0x82,
    'DAQ':                  0x83,
    'CHARGING':             0x84,
    'THERMOCOUPLE':         0x85,
    'USB':                  0x86,
    'FYDP25_TVCA':          0xC0,
}

board_inst_id = {
    'ANY':         0x00,
    'GENERIC':     0x01,
    'PRIMARY':     0x02,
    'FAILSAFE':    0x03,
    'INJ_A':       0x04,
    'INJ_B':       0x05,
    'VENT_A':      0x06,
    'VENT_B':      0x07,
    'VENT_C':      0x08,
    'VENT_D':      0x09,
    'RECOVERY':    0x0A,
    'ROCKET':      0x0B,
    'PAYLOAD':     0x0C,
    '1':           0x0D,
    '2':           0x0E,
    '3':           0x0F,
    '4':           0x10,
}

actuator_id = {
    'ACTUATOR_OX_INJECTOR_VALVE':      0x00,
    'ACTUATOR_FUEL_INJECTOR_VALVE':    0x01,
    'ACTUATOR_CHARGE_ENABLE':          0x02,
    'ACTUATOR_5V_RAIL_ROCKET':         0x03,
    'ACTUATOR_5V_RAIL_PAYLOAD':        0x04,
    'ACTUATOR_TELEMETRY':              0x05,
    'ACTUATOR_CAMERA_INJ_A':           0x06,
    'ACTUATOR_CAMERA_INJ_B':           0x07,
    'ACTUATOR_CAMERA_VENT_A':          0x08,
    'ACTUATOR_CAMERA_VENT_B':          0x09,
    'ACTUATOR_CAMERA_VENT_C':          0x0A,
    'ACTUATOR_CAMERA_VENT_D':          0x0B,
    'ACTUATOR_CAMERA_RECOVERY':        0x0C,
    'ACTUATOR_PROC_ESTIMATOR_INIT':    0x0D,
    'ACTUATOR_CANARD_ENABLE':          0x0E,
    'ACTUATOR_CANARD_ANGLE':           0x0F,
}

actuator_state = {
    'ACT_STATE_ON':                    0x00,
    'ACT_STATE_OFF':                   0x01,
    'ACT_STATE_UNK':                   0x02,
    'ACT_STATE_ILLEGAL':               0x03,
}

altimeter_id = {
    'ALTIMETER_RAVEN':                 0x00,
    'ALTIMETER_STRATOLOGGER':          0x01,
    'ALTIMETER_SRAD':                  0x02,
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
    'SENSOR_PRESSURE_OX':              0x09,
    'SENSOR_PRESSURE_FUEL':            0x0A,
    'SENSOR_PRESSURE_CC':              0x0B,
    'SENSOR_BARO_PRESSURE':            0x0C,
    'SENSOR_BARO_TEMP':                0x0D,
    'SENSOR_RA_BATT_VOLT_1':           0x0E,
    'SENSOR_RA_BATT_VOLT_2':           0x0F,
    'SENSOR_RA_BATT_CURR_1':           0x10,
    'SENSOR_RA_BATT_CURR_2':           0x11,
    'SENSOR_RA_MAG_VOLT_1':            0x12,
    'SENSOR_RA_MAG_VOLT_2':            0x13,
    'SENSOR_FPS':                      0x14,
    'SENSOR_CANARD_ENCODER_1':         0x15,
    'SENSOR_CANARD_ENCODER_2':         0x16,
    'SENSOR_PROC_FLIGHT_PHASE_STATUS': 0x17,
    'SENSOR_VELOCITY':                 0x18,
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

general_board_status_offset = {
    'E_5V_OVER_CURRENT':   0x00,
    'E_5V_OVER_VOLTAGE':   0x01,
    'E_5V_UNDER_VOLTAGE':  0x02,
    'E_12V_OVER_CURRENT':  0x03,
    'E_12V_OVER_VOLTAGE':  0x04,
    'E_12V_UNDER_VOLTAGE': 0x05,
    'E_IO_ERROR':          0x06,
    'E_FS_ERROR':          0x07,
}

general_board_status = {
    'E_NOMINAL':                     0x00,
    'E_5V_OVER_CURRENT':             0x01,
    'E_5V_OVER_VOLTAGE':             0x02,
    'E_5V_UNDER_VOLTAGE':            0x04,
    'E_12V_OVER_CURRENT':            0x08,
    'E_12V_OVER_VOLTAGE':            0x10,
    'E_12V_UNDER_VOLTAGE':           0x20,
    'E_IO_ERROR':                    0x40,
    'E_FS_ERROR':                    0x80,
}