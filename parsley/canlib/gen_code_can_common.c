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

bool build_general_cmd_msg(uint32_t timestamp, enum GEN_CMD gen_cmd, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[6] = gen_cmd; 


    output->data_len = 6;

    return true;
}

bool build_actuator_cmd_msg(uint32_t timestamp, enum ACTUATOR_ID actuator_id, enum ACTUATOR_STATES actuator_states, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[6] = actuator_id; 

	output->data[7] = actuator_states; 


    output->data_len = 7;

    return true;
}

bool build_alt_arm_cmd_msg(uint32_t timestamp, enum ARM_STATES arm_states, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 




    output->data_len = 5;

    return true;
}

bool build_reset_cmd_msg(uint32_t timestamp, enum BOARD_ID board_id, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[6] = board_id; 


    output->data_len = 6;

    return true;
}

bool build_debug_msg_msg(uint32_t timestamp, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 


	output->data[5] = (line >> 4) & 0xff; 



    output->data_len = 6;

    return true;
}

bool build_debug_printf_msg(uint32_t timestamp, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);



    output->data_len = 2;

    return true;
}

bool build_debug_radio_cmd_msg(uint32_t timestamp, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);



    output->data_len = 2;

    return true;
}

bool build_actuator_status_msg(uint32_t timestamp, enum ACTUATOR_ID actuator_id, enum ACTUATOR_STATES actuator_states, enum ACTUATOR_STATES actuator_states, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[6] = actuator_id; 

	output->data[7] = actuator_states; 

	output->data[8] = actuator_states; 


    output->data_len = 8;

    return true;
}

bool build_alt_arm_status_msg(uint32_t timestamp, enum ARM_STATES arm_states, uint16_t drogue_v, uint16_t main_v, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 



	output->data[5] = (drogue_v >> 8) & 0xff; 
	output->data[6] = (drogue_v >> 0) & 0xff; 

	output->data[7] = (main_v >> 8) & 0xff; 
	output->data[8] = (main_v >> 0) & 0xff; 


    output->data_len = 9;

    return true;
}

bool build_general_board_status_msg(uint32_t timestamp, enum BOARD_STATUS board_status, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[6] = board_status; 


    output->data_len = 6;

    return true;
}

bool build_sensor_temp_msg(uint32_t timestamp, uint8_t sensor_id, uint24_t temperature, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (sensor_id >> 0) & 0xff; 

	output->data[6] = (temperature >> 16) & 0xff; 
	output->data[7] = (temperature >> 8) & 0xff; 
	output->data[8] = (temperature >> 0) & 0xff; 


    output->data_len = 9;

    return true;
}

bool build_sensor_altitude_msg(uint32_t timestamp, uint32_t altitude, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (altitude >> 24) & 0xff; 
	output->data[6] = (altitude >> 16) & 0xff; 
	output->data[7] = (altitude >> 8) & 0xff; 
	output->data[8] = (altitude >> 0) & 0xff; 


    output->data_len = 9;

    return true;
}

bool build_sensor_acc_msg(uint32_t timestamp, uint16_t x, uint16_t y, uint16_t z, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 8) & 0xff; 
	output->data[3] = (time >> 0) & 0xff; 

	output->data[4] = (x >> 8) & 0xff; 
	output->data[5] = (x >> 0) & 0xff; 

	output->data[6] = (y >> 8) & 0xff; 
	output->data[7] = (y >> 0) & 0xff; 

	output->data[8] = (z >> 8) & 0xff; 
	output->data[9] = (z >> 0) & 0xff; 


    output->data_len = 10;

    return true;
}

bool build_sensor_acc2_msg(uint32_t timestamp, uint16_t x, uint16_t y, uint16_t z, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 8) & 0xff; 
	output->data[3] = (time >> 0) & 0xff; 

	output->data[4] = (x >> 8) & 0xff; 
	output->data[5] = (x >> 0) & 0xff; 

	output->data[6] = (y >> 8) & 0xff; 
	output->data[7] = (y >> 0) & 0xff; 

	output->data[8] = (z >> 8) & 0xff; 
	output->data[9] = (z >> 0) & 0xff; 


    output->data_len = 10;

    return true;
}

bool build_sensor_gyro_msg(uint32_t timestamp, uint16_t x, uint16_t y, uint16_t z, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 8) & 0xff; 
	output->data[3] = (time >> 0) & 0xff; 

	output->data[4] = (x >> 8) & 0xff; 
	output->data[5] = (x >> 0) & 0xff; 

	output->data[6] = (y >> 8) & 0xff; 
	output->data[7] = (y >> 0) & 0xff; 

	output->data[8] = (z >> 8) & 0xff; 
	output->data[9] = (z >> 0) & 0xff; 


    output->data_len = 10;

    return true;
}

bool build_sensor_mag_msg(uint32_t timestamp, uint16_t x, uint16_t y, uint16_t z, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 8) & 0xff; 
	output->data[3] = (time >> 0) & 0xff; 

	output->data[4] = (x >> 8) & 0xff; 
	output->data[5] = (x >> 0) & 0xff; 

	output->data[6] = (y >> 8) & 0xff; 
	output->data[7] = (y >> 0) & 0xff; 

	output->data[8] = (z >> 8) & 0xff; 
	output->data[9] = (z >> 0) & 0xff; 


    output->data_len = 10;

    return true;
}

bool build_sensor_analog_msg(uint32_t timestamp, enum SENSOR_ID sensor_id, uint16_t value, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 8) & 0xff; 
	output->data[3] = (time >> 0) & 0xff; 

	output->data[5] = sensor_id; 

	output->data[5] = (value >> 8) & 0xff; 
	output->data[6] = (value >> 0) & 0xff; 


    output->data_len = 7;

    return true;
}

bool build_gps_timestamp_msg(uint32_t timestamp, uint8_t hrs, uint8_t mins, uint8_t secs, uint8_t dsecs, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (hrs >> 0) & 0xff; 

	output->data[6] = (mins >> 0) & 0xff; 

	output->data[7] = (secs >> 0) & 0xff; 

	output->data[8] = (dsecs >> 0) & 0xff; 


    output->data_len = 9;

    return true;
}

bool build_gps_latitude_msg(uint32_t timestamp, uint8_t degs, uint8_t mins, uint16_t dmins, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (degs >> 0) & 0xff; 

	output->data[6] = (mins >> 0) & 0xff; 

	output->data[7] = (dmins >> 8) & 0xff; 
	output->data[8] = (dmins >> 0) & 0xff; 



    output->data_len = 9;

    return true;
}

bool build_gps_longitude_msg(uint32_t timestamp, uint8_t degs, uint8_t mins, uint16_t dmins, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (degs >> 0) & 0xff; 

	output->data[6] = (mins >> 0) & 0xff; 

	output->data[7] = (dmins >> 8) & 0xff; 
	output->data[8] = (dmins >> 0) & 0xff; 



    output->data_len = 9;

    return true;
}

bool build_gps_altitude_msg(uint32_t timestamp, uint16_t altitude, uint8_t daltitude, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (altitude >> 8) & 0xff; 
	output->data[6] = (altitude >> 0) & 0xff; 

	output->data[7] = (daltitude >> 0) & 0xff; 



    output->data_len = 8;

    return true;
}

bool build_gps_info_msg(uint32_t timestamp, uint8_t num_sats, uint8_t quality, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (num_sats >> 0) & 0xff; 

	output->data[6] = (quality >> 0) & 0xff; 


    output->data_len = 7;

    return true;
}

bool build_fill_lvl_msg(uint32_t timestamp, uint8_t level, enum FILL_DIRECTION fill_direction, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (level >> 0) & 0xff; 

	output->data[7] = fill_direction; 


    output->data_len = 7;

    return true;
}

bool build_radi_value_msg(uint32_t timestamp, uint8_t radi_board, uint16_t radi, can_msg_t *output)
{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);

	output->data[2] = (time >> 16) & 0xff; 
	output->data[3] = (time >> 8) & 0xff; 
	output->data[4] = (time >> 0) & 0xff; 

	output->data[5] = (radi_board >> 0) & 0xff; 

	output->data[6] = (radi >> 8) & 0xff; 
	output->data[7] = (radi >> 0) & 0xff; 


    output->data_len = 8;

    return true;
}
int get_general_cmd(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_GENERAL_CMD) {return false;}


    return true;
}
int get_actuator_cmd(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_ACTUATOR_CMD) {return false;}


    return true;
}
bool get_alt_arm_cmd(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (!altimeter) { return false; }
	if (get_message_type(msg) != MSG_ALT_ARM_CMD) {return false;}

	*altimeter = msg->data[4];

    return true;
}
int get_reset_cmd(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_RESET_CMD) {return false;}


    return true;
}
bool get_debug_msg(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (!level) { return false; }
	if (!line) { return false; }
	if (get_message_type(msg) != MSG_DEBUG_MSG) {return false;}

	*level = msg->data[3];
	*line = (uint12_t)msg->data[4] << 12 | msg->data[5];

    return true;
}
bool get_debug_printf(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_DEBUG_PRINTF) {return false;}


    return true;
}
bool get_debug_radio_cmd(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_DEBUG_RADIO_CMD) {return false;}


    return true;
}
int get_actuator_status(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_ACTUATOR_STATUS) {return false;}


    return true;
}
bool get_alt_arm_status(const can_msg_t *msg, uint16_t drogue_v, uint16_t main_v)
{
    if (!msg) { return false };
	if (!altimeter) { return false; }
	if (!drogue_v) { return false; }
	if (!main_v) { return false; }
	if (get_message_type(msg) != MSG_ALT_ARM_STATUS) {return false;}

	*altimeter = msg->data[4];
	*drogue_v = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*drogue_v = msg->data[6]	*main_v = (uint16_t)msg->data[6] << 16 | msg->data[7];
	*main_v = msg->data[7]
    return true;
}
int get_general_board_status(const can_msg_t *msg)
{
    if (!msg) { return false };
	if (get_message_type(msg) != MSG_GENERAL_BOARD_STATUS) {return false;}


    return true;
}
bool get_sensor_temp(const can_msg_t *msg, uint8_t sensor_id, uint24_t temperature)
{
    if (!msg) { return false };
	if (!sensor_id) { return false; }
	if (!temperature) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_TEMP) {return false;}

	*sensor_id = msg->data[3];
	*temperature = (uint24_t)msg->data[4] << 24 | msg->data[5];
	*temperature |= (uint24_t)msg->data[5] << 12 | msg->data[6];
	*temperature = msg->data[6]
    return true;
}
bool get_sensor_altitude(const can_msg_t *msg, uint32_t altitude)
{
    if (!msg) { return false };
	if (!altitude) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_ALTITUDE) {return false;}

	*altitude = (uint32_t)msg->data[3] << 32 | msg->data[4];
	*altitude |= (uint32_t)msg->data[4] << 16 | msg->data[5];
	*altitude |= (uint32_t)msg->data[5] << 10 | msg->data[6];
	*altitude = msg->data[6]
    return true;
}
bool get_sensor_acc(const can_msg_t *msg, uint16_t x, uint16_t y, uint16_t z)
{
    if (!msg) { return false };
	if (!x) { return false; }
	if (!y) { return false; }
	if (!z) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_ACC) {return false;}

	*x = (uint16_t)msg->data[3] << 16 | msg->data[4];
	*x = msg->data[4]	*y = (uint16_t)msg->data[4] << 16 | msg->data[5];
	*y = msg->data[5]	*z = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*z = msg->data[6]
    return true;
}
bool get_sensor_acc2(const can_msg_t *msg, uint16_t x, uint16_t y, uint16_t z)
{
    if (!msg) { return false };
	if (!x) { return false; }
	if (!y) { return false; }
	if (!z) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_ACC2) {return false;}

	*x = (uint16_t)msg->data[3] << 16 | msg->data[4];
	*x = msg->data[4]	*y = (uint16_t)msg->data[4] << 16 | msg->data[5];
	*y = msg->data[5]	*z = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*z = msg->data[6]
    return true;
}
bool get_sensor_gyro(const can_msg_t *msg, uint16_t x, uint16_t y, uint16_t z)
{
    if (!msg) { return false };
	if (!x) { return false; }
	if (!y) { return false; }
	if (!z) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_GYRO) {return false;}

	*x = (uint16_t)msg->data[3] << 16 | msg->data[4];
	*x = msg->data[4]	*y = (uint16_t)msg->data[4] << 16 | msg->data[5];
	*y = msg->data[5]	*z = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*z = msg->data[6]
    return true;
}
bool get_sensor_mag(const can_msg_t *msg, uint16_t x, uint16_t y, uint16_t z)
{
    if (!msg) { return false };
	if (!x) { return false; }
	if (!y) { return false; }
	if (!z) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_MAG) {return false;}

	*x = (uint16_t)msg->data[3] << 16 | msg->data[4];
	*x = msg->data[4]	*y = (uint16_t)msg->data[4] << 16 | msg->data[5];
	*y = msg->data[5]	*z = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*z = msg->data[6]
    return true;
}
bool get_sensor_analog(const can_msg_t *msg, uint16_t value)
{
    if (!msg) { return false };
	if (!value) { return false; }
	if (get_message_type(msg) != MSG_SENSOR_ANALOG) {return false;}

	*value = (uint16_t)msg->data[4] << 16 | msg->data[5];
	*value = msg->data[5]
    return true;
}
bool get_gps_timestamp(const can_msg_t *msg, uint8_t hrs, uint8_t mins, uint8_t secs, uint8_t dsecs)
{
    if (!msg) { return false };
	if (!hrs) { return false; }
	if (!mins) { return false; }
	if (!secs) { return false; }
	if (!dsecs) { return false; }
	if (get_message_type(msg) != MSG_GPS_TIMESTAMP) {return false;}

	*hrs = msg->data[3];
	*mins = msg->data[4];
	*secs = msg->data[5];
	*dsecs = msg->data[6];

    return true;
}
bool get_gps_latitude(const can_msg_t *msg, uint8_t degs, uint8_t mins, uint16_t dmins)
{
    if (!msg) { return false };
	if (!degs) { return false; }
	if (!mins) { return false; }
	if (!dmins) { return false; }
	if (get_message_type(msg) != MSG_GPS_LATITUDE) {return false;}

	*degs = msg->data[3];
	*mins = msg->data[4];
	*dmins = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*dmins = msg->data[6]
    return true;
}
bool get_gps_longitude(const can_msg_t *msg, uint8_t degs, uint8_t mins, uint16_t dmins)
{
    if (!msg) { return false };
	if (!degs) { return false; }
	if (!mins) { return false; }
	if (!dmins) { return false; }
	if (get_message_type(msg) != MSG_GPS_LONGITUDE) {return false;}

	*degs = msg->data[3];
	*mins = msg->data[4];
	*dmins = (uint16_t)msg->data[5] << 16 | msg->data[6];
	*dmins = msg->data[6]
    return true;
}
bool get_gps_altitude(const can_msg_t *msg, uint16_t altitude, uint8_t daltitude)
{
    if (!msg) { return false };
	if (!altitude) { return false; }
	if (!daltitude) { return false; }
	if (get_message_type(msg) != MSG_GPS_ALTITUDE) {return false;}

	*altitude = (uint16_t)msg->data[3] << 16 | msg->data[4];
	*altitude = msg->data[4]	*daltitude = msg->data[4];

    return true;
}
bool get_gps_info(const can_msg_t *msg, uint8_t num_sats, uint8_t quality)
{
    if (!msg) { return false };
	if (!num_sats) { return false; }
	if (!quality) { return false; }
	if (get_message_type(msg) != MSG_GPS_INFO) {return false;}

	*num_sats = msg->data[3];
	*quality = msg->data[4];

    return true;
}
bool get_fill_lvl(const can_msg_t *msg, uint8_t level)
{
    if (!msg) { return false };
	if (!level) { return false; }
	if (get_message_type(msg) != MSG_FILL_LVL) {return false;}

	*level = msg->data[3];

    return true;
}
bool get_radi_value(const can_msg_t *msg, uint8_t radi_board, uint16_t radi)
{
    if (!msg) { return false };
	if (!radi_board) { return false; }
	if (!radi) { return false; }
	if (get_message_type(msg) != MSG_RADI_VALUE) {return false;}

	*radi_board = msg->data[3];
	*radi = (uint16_t)msg->data[4] << 16 | msg->data[5];
	*radi = msg->data[5]
    return true;
}
