#ifndef MESSAGE_TYPES_H_
#define MESSAGE_TYPES_H_

#define MSG_GENERAL_CMD               0X0060

#define MSG_ACTUATOR_CMD              0X00C0

#define MSG_ALT_ARM_CMD               0X0140

#define MSG_RESET_CMD                 0X0160

#define MSG_DEBUG_MSG                 0X0180

#define MSG_DEBUG_PRINTF              0X01E0

#define MSG_DEBUG_RADIO_CMD           0X0200

#define MSG_ALT_ARM_STATUS            0X0440

#define MSG_ACTUATOR_STATUS           0X0460

#define MSG_GENERAL_BOARD_STATUS      0X0520

#define MSG_SENSOR_TEMP               0X0540

#define MSG_SENSOR_ALTITUDE           0X0560

#define MSG_SENSOR_ACC                0X0580

#define MSG_SENSOR_ACC2               0X05A0

#define MSG_SENSOR_GYRO               0X05E0

#define MSG_SENSOR_MAG                0X0640

#define MSG_SENSOR_ANALOG             0X06A0

#define MSG_GPS_TIMESTAMP             0X06C0

#define MSG_GPS_LATITUDE              0X06E0

#define MSG_GPS_LONGITUDE             0X0700

#define MSG_GPS_ALTITUDE              0X0720

#define MSG_GPS_INFO                  0X0740

#define MSG_FILL_LVL                  0X0780

#define MSG_RADI_VALUE                0X07A0

#define MSG_LEDS_ON                   0X07E0

#define MSG_LEDS_OFF                  0X07C0

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

enum GEN_CMD {
    BUS_DOWN_WARNING = 0,
};

enum ACTUATOR_STATE {
    ACTUATOR_ON = 0,
    ACTUATOR_OFF,
    ACTUATOR_UNK,
    ACTUATOR_ILLEGAL,
};

enum ARM_STATE {
    DISARMED = 0,
    ARMED,
};

enum BOARD_STATUS {
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

enum SENSOR_ID {
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

enum FILL_DIRECTION {
    FILLING = 0,
    EMPTYING,
};

enum ACTUATOR_ID {
    ACTUATOR_VENT_VALVE = 0,
    ACTUATOR_INJECTOR_VALVE,
    ACTUATOR_PAYLOAD,
    ACTUATOR_CAMERAS,
    ACTUATOR_CANBUS,
    ACTUATOR_CHARGE,
};

#endif // compile guard
