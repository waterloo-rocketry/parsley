#include "can_common.h"
#include "message_types.h"
#include <stddef.h>

// this symbol should be defined in the project's Makefile, but if it
// isn't, issue a warning and set it to 0
#ifndef  BOARD_UNIQUE_ID
#warning BOARD_UNIQUE_ID not defined, please set that up in project
#define  BOARD_UNIQUE_ID 0
#endif

// Helper function for populating CAN messages
static void write_timestamp_2bytes(uint16_t timestamp, can_msg_t *output)
{
    output->data[0] = (timestamp >> 8) & 0xff;
    output->data[1] = (timestamp >> 0) & 0xff;
}

static void write_timestamp_3bytes(uint32_t timestamp, can_msg_t *output)
{
    output->data[0] = (timestamp >> 16) & 0xff;
    output->data[1] = (timestamp >> 8) & 0xff;
    output->data[2] = (timestamp >> 0) & 0xff;
}

bool build_general_cmd_msg(uint32_t timestamp,
                        enum GEN_CMD gen_cmd, 

                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_actuator_cmd_msg(uint32_t timestamp,
                        enum ACTUATOR_ID actuator_id, 
                           enum ACTUATOR_STATES actuator_states, 

                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_alt_arm_cmd_msg(uint32_t timestamp,
                        enum ARM_STATES arm_states, 

                        uint4_t altimeter, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = altimeter; 

    
    output->data_len = 4;

    return true;
}
        
bool build_reset_cmd_msg(uint32_t timestamp,
                        enum BOARD_ID board_id, 

                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_debug_msg_msg(uint32_t timestamp,
                        
                        uint4_t level, 
                           uint12_t line, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = level; 
    output->data[4] = line; 

    
    output->data_len = 5;

    return true;
}
        
bool build_debug_printf_msg(uint32_t timestamp,
                        
                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_debug_radio_cmd_msg(uint32_t timestamp,
                        
                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_actuator_status_msg(uint32_t timestamp,
                        enum ACTUATOR_ID actuator_id, 
                           enum ACTUATOR_STATES actuator_states, 
                           enum ACTUATOR_STATES actuator_states, 

                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_alt_arm_status_msg(uint32_t timestamp,
                        enum ARM_STATES arm_states, 

                        uint4_t altimeter, 
                           uint16_t drogue_v, 
                           uint16_t main_v, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = altimeter; 
    output->data[4] = drogue_v; 
    output->data[5] = main_v; 

    
    output->data_len = 6;

    return true;
}
        
bool build_general_board_status_msg(uint32_t timestamp,
                        enum BOARD_STATUS board_status, 

                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    
    
    output->data_len = 3;

    return true;
}
        
bool build_sensor_temp_msg(uint32_t timestamp,
                        
                        uint8_t sensor_id, 
                           uint24_t temperature, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = sensor_id; 
    output->data[4] = temperature; 

    
    output->data_len = 5;

    return true;
}
        
bool build_sensor_altitude_msg(uint32_t timestamp,
                        
                        uint32_t altitude, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = altitude; 

    
    output->data_len = 4;

    return true;
}
        
bool build_sensor_acc_msg(uint32_t timestamp,
                        
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = x; 
    output->data[4] = y; 
    output->data[5] = z; 

    
    output->data_len = 6;

    return true;
}
        
bool build_sensor_acc2_msg(uint32_t timestamp,
                        
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = x; 
    output->data[4] = y; 
    output->data[5] = z; 

    
    output->data_len = 6;

    return true;
}
        
bool build_sensor_gyro_msg(uint32_t timestamp,
                        
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = x; 
    output->data[4] = y; 
    output->data[5] = z; 

    
    output->data_len = 6;

    return true;
}
        
bool build_sensor_mag_msg(uint32_t timestamp,
                        
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = x; 
    output->data[4] = y; 
    output->data[5] = z; 

    
    output->data_len = 6;

    return true;
}
        
bool build_sensor_analog_msg(uint32_t timestamp,
                        enum SENSOR_ID sensor_id, 

                        uint16_t value, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = value; 

    
    output->data_len = 4;

    return true;
}
        
bool build_gps_timestamp_msg(uint32_t timestamp,
                        
                        uint8_t hrs, 
                           uint8_t mins, 
                           uint8_t secs, 
                           uint8_t dsecs, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = hrs; 
    output->data[4] = mins; 
    output->data[5] = secs; 
    output->data[6] = dsecs; 

    
    output->data_len = 7;

    return true;
}
        
bool build_gps_latitude_msg(uint32_t timestamp,
                        
                        uint8_t degs, 
                           uint8_t mins, 
                           uint16_t dmins, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = degs; 
    output->data[4] = mins; 
    output->data[5] = dmins; 

    
    output->data_len = 6;

    return true;
}
        
bool build_gps_longitude_msg(uint32_t timestamp,
                        
                        uint8_t degs, 
                           uint8_t mins, 
                           uint16_t dmins, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = degs; 
    output->data[4] = mins; 
    output->data[5] = dmins; 

    
    output->data_len = 6;

    return true;
}
        
bool build_gps_altitude_msg(uint32_t timestamp,
                        
                        uint16_t altitude, 
                           uint8_t daltitude, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = altitude; 
    output->data[4] = daltitude; 

    
    output->data_len = 5;

    return true;
}
        
bool build_gps_info_msg(uint32_t timestamp,
                        
                        uint8_t num_sats, 
                           uint8_t quality, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = num_sats; 
    output->data[4] = quality; 

    
    output->data_len = 5;

    return true;
}
        
bool build_fill_lvl_msg(uint32_t timestamp,
                        enum FILL_DIRECTION fill_direction, 

                        uint8_t level, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = level; 

    
    output->data_len = 4;

    return true;
}
        
bool build_radi_value_msg(uint32_t timestamp,
                        
                        uint8_t radi_board, 
                           uint16_t radi, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    output->data[3] = radi_board; 
    output->data[4] = radi; 

    
    output->data_len = 5;

    return true;
}
        