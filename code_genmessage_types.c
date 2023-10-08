#ifndef MESSAGE_TYPES_H_
#define MESSAGE_TYPES_H_

#define MSG_GENERAL_CMD               0X0003

#define MSG_ACTUATOR_CMD              0X0006

#define MSG_ALT_ARM_CMD               0X000A

#define MSG_RESET_CMD                 0X000B

#define MSG_DEBUG_MSG                 0X000C

#define MSG_DEBUG_PRINTF              0X000F

#define MSG_DEBUG_RADIO_CMD           0X0010

#define MSG_ALT_ARM_STATUS            0X0022

#define MSG_ACTUATOR_STATUS           0X0023

#define MSG_GENERAL_BOARD_STATUS      0X0029

#define MSG_SENSOR_TEMP               0X002A

#define MSG_SENSOR_ALTITUDE           0X002B

#define MSG_SENSOR_ACC                0X002C

#define MSG_SENSOR_ACC2               0X002D

#define MSG_SENSOR_GYRO               0X002F

#define MSG_SENSOR_MAG                0X0032

#define MSG_SENSOR_ANALOG             0X0035

#define MSG_GPS_TIMESTAMP             0X0036

#define MSG_GPS_LATITUDE              0X0037

#define MSG_GPS_LONGITUDE             0X0038

#define MSG_GPS_ALTITUDE              0X0039

#define MSG_GPS_INFO                  0X003A

#define MSG_FILL_LVL                  0X003C

#define MSG_RADI_VALUE                0X003D

#define MSG_LEDS_ON                   0X003F

#define MSG_LEDS_OFF                  0X003E

#define BOARD_ID_ANY                       0X0000

#define BOARD_ID_ACTUATOR_INJ              0X0001

#define BOARD_ID_ACTUATOR_VENT             0X0002

#define BOARD_ID_ACTUATOR_CAM1             0X0003

#define BOARD_ID_ACTUATOR_CAM2             0X0004

#define BOARD_ID_SENSOR_INJ                0X0005

#define BOARD_ID_SENSOR_VENT               0X0006

#define BOARD_ID_SENSOR_PAYLOAD            0X0007

#define BOARD_ID_LOGGER                    0X0008

#define BOARD_ID_LOGGER_PAYLOAD            0X0009

#define BOARD_ID_LOGGER_SPARE              0X000A

#define BOARD_ID_GPS                       0X000B

#define BOARD_ID_GPS_PAYLOAD               0X000C

#define BOARD_ID_GPS_SPARE                 0X000D

#define BOARD_ID_CHARGING                  0X000E

#define BOARD_ID_ARMING                    0X000F

#define BOARD_ID_GRANDPAPA                 0X0010

#define BOARD_ID_KALMAN                    0X0011

#define BOARD_ID_TELEMETRY                 0X0012

#define BOARD_ID_USB                       0X0013

#define BOARD_ID_RLCS                      0X0014

enum command {
    BUS_DOWN_WARNING = 0,
};

enum actuator {
    ACTUATOR_VENT_VALVE = 0,
    ACTUATOR_INJECTOR_VALVE,
    ACTUATOR_PAYLOAD,
    ACTUATOR_CAMERAS,
    ACTUATOR_CANBUS,
    ACTUATOR_CHARGE,
};

enum req_state {
    ACTUATOR_ON = 0,
    ACTUATOR_OFF,
    ACTUATOR_UNK,
    ACTUATOR_ILLEGAL,
};

enum state {
    DISARMED = 0,
    ARMED,
};

enum cur_state {
    ACTUATOR_ON = 0,
    ACTUATOR_OFF,
    ACTUATOR_UNK,
    ACTUATOR_ILLEGAL,
};

enum status {
    E_NOMINAL = 0,
    E_BUS_OVER_CURRENT,
    E_BUS_UNDER_VOLTAGE,
    E_BUS_OVER_VOLTAGE,
    E_BATT_OVER_CURRENT,
    E_BATT_UNDER_VOLTAGE,
    E_BATT_OVER_VOLTAGE,
    E_BOARD_FEARED_DEAD,
    E_NO_CAN_TRAFFIC,
    E_MISSING_CRITICAL_BOARD,
    E_RADIO_SIGNAL_LOST,
    E_ACTUATOR_STATE,
    E_CANNOT_INIT_DACS,
    E_VENT_POT_RANGE,
    E_LOGGING,
    E_GPS,
    E_SENSOR,
    E_ILLEGAL_CAN_MSG,
    E_SEGFAULT,
    E_UNHANDLED_INTERRUPT,
    E_CODING_FUCKUP,
};

enum sensor_id {
    SENSOR_BUS_CURR = 0,
    SENSOR_BATT_CURR,
    SENSOR_BATT_VOLT,
    SENSOR_CHARGE_CURR,
    SENSOR_GROUND_VOLT,
    SENSOR_PRESSURE_OX,
    SENSOR_PRESSURE_CC,
    SENSOR_PRESSURE_PNEUMATICS,
    SENSOR_BARO,
    SENSOR_ARM_BATT_1,
    SENSOR_ARM_BATT_2,
    SENSOR_MAG_1,
    SENSOR_MAG_2,
    SENSOR_VELOCITY,
    SENSOR_VENT_TEMP,
};

enum direction {
    FILLING = 0,
    EMPTYING,
};

#endif // compile guard
