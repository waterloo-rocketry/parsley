#ifndef CAN_COMMON_H_
#define CAN_COMMON_H_

#include <stdint.h>
#include <stdbool.h>
#include "can.h"
#include "message_types.h"

/*
 * Debug levels for the debugging messages (MSG_DEBUG_MSG). Lower
 * numbers are more serious debug things
 */
typedef enum {
    NONE      = 0,
    ERROR     = 1,
    WARN      = 2,
    INFO      = 3,
    DEBUGGING = 4
} can_debug_level_t;

/*
 * This macro creates a new debug message, and stores it in
 * debug_macro_output. The reason that this is a macro and not a
 * function is that debug messages have the line number at which they
 * are created embedded in their data. This is so that we can review
 * the code later to see where the debug was issued from, and
 * hopefully find the cause of the problem
 */
#define LOG_MSG(debug_macro_level, debug_macro_timestamp, debug_macro_output) \
    do { \
        uint8_t debug_macro_data[5] = {(debug_macro_level << 4) | ((__LINE__ >> 8) & 0xF), \
                                       __LINE__ & 0xFF, \
                                       0,0,0}; \
        build_debug_msg( debug_macro_timestamp, \
                         debug_macro_data, \
                         &debug_macro_output); \
    } while(0)

bool build_general_cmd_msg(uint32_t timestamp,
                           enum GEN_CMD gen_cmd, 

                           
                           can_msg_t *output);


bool build_actuator_cmd_msg(uint32_t timestamp,
                           enum ACTUATOR_ID actuator_id, 
                           enum ACTUATOR_STATES actuator_states, 

                           
                           can_msg_t *output);


bool build_alt_arm_cmd_msg(uint32_t timestamp,
                           enum ARM_STATES arm_states, 

                           uint4_t altimeter, 

                           can_msg_t *output);


bool build_reset_cmd_msg(uint32_t timestamp,
                           enum BOARD_ID board_id, 

                           
                           can_msg_t *output);


bool build_debug_msg_msg(uint32_t timestamp,
                           
                           uint4_t level, 
                           uint12_t line, 

                           can_msg_t *output);


bool build_debug_printf_msg(uint32_t timestamp,
                           
                           
                           can_msg_t *output);


bool build_debug_radio_cmd_msg(uint32_t timestamp,
                           
                           
                           can_msg_t *output);


bool build_actuator_status_msg(uint32_t timestamp,
                           enum ACTUATOR_ID actuator_id, 
                           enum ACTUATOR_STATES actuator_states, 
                           enum ACTUATOR_STATES actuator_states, 

                           
                           can_msg_t *output);


bool build_alt_arm_status_msg(uint32_t timestamp,
                           enum ARM_STATES arm_states, 

                           uint4_t altimeter, 
                           uint16_t drogue_v, 
                           uint16_t main_v, 

                           can_msg_t *output);


bool build_general_board_status_msg(uint32_t timestamp,
                           enum BOARD_STATUS board_status, 

                           
                           can_msg_t *output);


bool build_sensor_temp_msg(uint32_t timestamp,
                           
                           uint8_t sensor_id, 
                           uint24_t temperature, 

                           can_msg_t *output);


bool build_sensor_altitude_msg(uint32_t timestamp,
                           
                           uint32_t altitude, 

                           can_msg_t *output);


bool build_sensor_acc_msg(uint32_t timestamp,
                           
                           uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                           can_msg_t *output);


bool build_sensor_acc2_msg(uint32_t timestamp,
                           
                           uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                           can_msg_t *output);


bool build_sensor_gyro_msg(uint32_t timestamp,
                           
                           uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                           can_msg_t *output);


bool build_sensor_mag_msg(uint32_t timestamp,
                           
                           uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                           can_msg_t *output);


bool build_sensor_analog_msg(uint32_t timestamp,
                           enum SENSOR_ID sensor_id, 

                           uint16_t value, 

                           can_msg_t *output);


bool build_gps_timestamp_msg(uint32_t timestamp,
                           
                           uint8_t hrs, 
                           uint8_t mins, 
                           uint8_t secs, 
                           uint8_t dsecs, 

                           can_msg_t *output);


bool build_gps_latitude_msg(uint32_t timestamp,
                           
                           uint8_t degs, 
                           uint8_t mins, 
                           uint16_t dmins, 

                           can_msg_t *output);


bool build_gps_longitude_msg(uint32_t timestamp,
                           
                           uint8_t degs, 
                           uint8_t mins, 
                           uint16_t dmins, 

                           can_msg_t *output);


bool build_gps_altitude_msg(uint32_t timestamp,
                           
                           uint16_t altitude, 
                           uint8_t daltitude, 

                           can_msg_t *output);


bool build_gps_info_msg(uint32_t timestamp,
                           
                           uint8_t num_sats, 
                           uint8_t quality, 

                           can_msg_t *output);


bool build_fill_lvl_msg(uint32_t timestamp,
                           enum FILL_DIRECTION fill_direction, 

                           uint8_t level, 

                           can_msg_t *output);


bool build_radi_value_msg(uint32_t timestamp,
                           
                           uint8_t radi_board, 
                           uint16_t radi, 

                           can_msg_t *output);


int get_general_cmd(const can_msg_t *msg,
                        );

int get_actuator_cmd(const can_msg_t *msg,
                        );

bool get_alt_arm_cmd(const can_msg_t *msg,
                        );

int get_reset_cmd(const can_msg_t *msg,
                        );

bool get_debug_msg(const can_msg_t *msg,
                                                   uint12_t *line, 
                           uint24_t *data, 
);

int get_debug_printf(const can_msg_t *msg,
                        );

int get_debug_radio_cmd(const can_msg_t *msg,
                        );

int get_actuator_status(const can_msg_t *msg,
                        );

bool get_alt_arm_status(const can_msg_t *msg,
                                                   uint16_t *drogue_v, 
                           uint16_t *main_v, 
);

int get_general_board_status(const can_msg_t *msg,
                        );

bool get_sensor_temp(const can_msg_t *msg,
                        uint8_t *sensor_id, 
                           uint24_t *temperature, 
);

bool get_sensor_altitude(const can_msg_t *msg,
                        uint32_t *altitude, 
);

bool get_sensor_acc(const can_msg_t *msg,
                        uint16_t *x, 
                           uint16_t *y, 
                           uint16_t *z, 
);

bool get_sensor_acc2(const can_msg_t *msg,
                        uint16_t *x, 
                           uint16_t *y, 
                           uint16_t *z, 
);

bool get_sensor_gyro(const can_msg_t *msg,
                        uint16_t *x, 
                           uint16_t *y, 
                           uint16_t *z, 
);

bool get_sensor_mag(const can_msg_t *msg,
                        uint16_t *x, 
                           uint16_t *y, 
                           uint16_t *z, 
);

bool get_sensor_analog(const can_msg_t *msg,
                        uint16_t *value, 
);

bool get_gps_timestamp(const can_msg_t *msg,
                        uint8_t *hrs, 
                           uint8_t *mins, 
                           uint8_t *secs, 
                           uint8_t *dsecs, 
);

bool get_gps_latitude(const can_msg_t *msg,
                        uint8_t *degs, 
                           uint8_t *mins, 
                           uint16_t *dmins, 
                           uint8_t *direction, 
);

bool get_gps_longitude(const can_msg_t *msg,
                        uint8_t *degs, 
                           uint8_t *mins, 
                           uint16_t *dmins, 
                           uint8_t *direction, 
);

bool get_gps_altitude(const can_msg_t *msg,
                        uint16_t *altitude, 
                           uint8_t *daltitude, 
                           uint8_t *unit, 
);

bool get_gps_info(const can_msg_t *msg,
                        uint8_t *num_sats, 
                           uint8_t *quality, 
);

bool get_fill_lvl(const can_msg_t *msg,
                        uint8_t *level, 
);

bool get_radi_value(const can_msg_t *msg,
                        uint8_t *radi_board, 
                           uint16_t *radi, 
);
