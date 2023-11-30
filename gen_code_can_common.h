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
bool build_general_cmd_msg(uint32_t timestamp,enum gen_cmd arg0_gen_cmd, can_msg_t *output)bool build_actuator_cmd_msg(uint32_t timestamp,enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, can_msg_t *output)bool build_alt_arm_cmd_msg(uint32_t timestamp,enum arm_states arg0_arm_states, uint8_t arg1_altimeter, can_msg_t *output)bool build_reset_cmd_msg(uint32_t timestamp,enum board_id arg0_board_id, can_msg_t *output)bool build_debug_msg_msg(uint32_t timestamp,uint8_t arg0_level, uint16_t arg1_line, enum data arg2_data, can_msg_t *output)bool build_debug_printf_msg(uint32_t timestamp,, can_msg_t *output)bool build_debug_radio_cmd_msg(uint32_t timestamp,, can_msg_t *output)bool build_actuator_status_msg(uint32_t timestamp,enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, enum actuator_states arg2_actuator_states, can_msg_t *output)bool build_alt_arm_status_msg(uint32_t timestamp,enum arm_states arg0_arm_states, uint8_t arg1_altimeter, uint16_t arg2_drogue_v, uint16_t arg3_main_v, can_msg_t *output)bool build_general_board_status_msg(uint32_t timestamp,enum board_status arg0_board_status, can_msg_t *output)bool build_sensor_temp_msg(uint32_t timestamp,uint8_t arg0_sensor_id, uint32_t arg1_temperature, can_msg_t *output)bool build_sensor_altitude_msg(uint32_t timestamp,uint32_t arg0_altitude, can_msg_t *output)bool build_sensor_acc_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output)bool build_sensor_acc2_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output)bool build_sensor_gyro_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output)bool build_sensor_mag_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output)bool build_sensor_analog_msg(uint32_t timestamp,enum sensor_id arg0_sensor_id, uint16_t arg1_value, can_msg_t *output)bool build_gps_timestamp_msg(uint32_t timestamp,uint8_t arg0_hrs, uint8_t arg1_mins, uint8_t arg2_secs, uint8_t arg3_dsecs, can_msg_t *output)bool build_gps_latitude_msg(uint32_t timestamp,uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction, can_msg_t *output)bool build_gps_longitude_msg(uint32_t timestamp,uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction, can_msg_t *output)bool build_gps_altitude_msg(uint32_t timestamp,uint16_t arg0_altitude, uint8_t arg1_daltitude, enum unit arg2_unit, can_msg_t *output)bool build_gps_info_msg(uint32_t timestamp,uint8_t arg0_num_sats, uint8_t arg1_quality, can_msg_t *output)bool build_fill_lvl_msg(uint32_t timestamp,uint8_t arg0_level, enum fill_direction arg1_fill_direction, can_msg_t *output)bool build_radi_value_msg(uint32_t timestamp,uint8_t arg0_radi_board, uint16_t arg1_radi, can_msg_t *output)
int get_general_cmd(const can_msg_t *msg,
                        enum gen_cmd arg0_gen_cmd);

int get_actuator_cmd(const can_msg_t *msg,
                        enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states);

bool get_alt_arm_cmd(const can_msg_t *msg,
                        enum arm_states arg0_arm_states, uint8_t arg1_altimeter);

int get_reset_cmd(const can_msg_t *msg,
                        enum board_id arg0_board_id);

bool get_debug_msg(const can_msg_t *msg,
                        uint8_t arg0_level, uint16_t arg1_line, enum data arg2_data);

bool get_debug_printf(const can_msg_t *msg,
                        );

bool get_debug_radio_cmd(const can_msg_t *msg,
                        );

int get_actuator_status(const can_msg_t *msg,
                        enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, enum actuator_states arg2_actuator_states);

bool get_alt_arm_status(const can_msg_t *msg,
                        enum arm_states arg0_arm_states, uint8_t arg1_altimeter, uint16_t arg2_drogue_v, uint16_t arg3_main_v);

int get_general_board_status(const can_msg_t *msg,
                        enum board_status arg0_board_status);

bool get_sensor_temp(const can_msg_t *msg,
                        uint8_t arg0_sensor_id, uint32_t arg1_temperature);

bool get_sensor_altitude(const can_msg_t *msg,
                        uint32_t arg0_altitude);

bool get_sensor_acc(const can_msg_t *msg,
                        uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z);

bool get_sensor_acc2(const can_msg_t *msg,
                        uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z);

bool get_sensor_gyro(const can_msg_t *msg,
                        uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z);

bool get_sensor_mag(const can_msg_t *msg,
                        uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z);

bool get_sensor_analog(const can_msg_t *msg,
                        enum sensor_id arg0_sensor_id, uint16_t arg1_value);

bool get_gps_timestamp(const can_msg_t *msg,
                        uint8_t arg0_hrs, uint8_t arg1_mins, uint8_t arg2_secs, uint8_t arg3_dsecs);

bool get_gps_latitude(const can_msg_t *msg,
                        uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction);

bool get_gps_longitude(const can_msg_t *msg,
                        uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction);

bool get_gps_altitude(const can_msg_t *msg,
                        uint16_t arg0_altitude, uint8_t arg1_daltitude, enum unit arg2_unit);

bool get_gps_info(const can_msg_t *msg,
                        uint8_t arg0_num_sats, uint8_t arg1_quality);

bool get_fill_lvl(const can_msg_t *msg,
                        uint8_t arg0_level, enum fill_direction arg1_fill_direction);

bool get_radi_value(const can_msg_t *msg,
                        uint8_t arg0_radi_board, uint16_t arg1_radi);
#endif // compile guard