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
bool build_general_cmd_msg(uint32_t timestamp,enum gen_cmd arg0_gen_cmd, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GENERAL_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);

    output->data_len = 4;

    return true;
}bool build_actuator_cmd_msg(uint32_t timestamp,enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ACTUATOR_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_alt_arm_cmd_msg(uint32_t timestamp,enum arm_states arg0_arm_states, uint8_t arg1_altimeter, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ALT_ARM_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);



    output->data_len = 3;

    return true;
}bool build_reset_cmd_msg(uint32_t timestamp,enum board_id arg0_board_id, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_RESET_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);

    output->data_len = 4;

    return true;
}bool build_debug_msg_msg(uint32_t timestamp,uint8_t arg0_level, uint16_t arg1_line, enum data arg2_data, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_DEBUG_MSG | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg1) & 0x00FF);
	output->data[4] = (uint8_t)((arg2) & 0x00FF);
	output->data[5] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2 >> 16) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_debug_printf_msg(uint32_t timestamp,, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_DEBUG_PRINTF | BOARD_UNIQUE_ID;
    write_timestamp_bytes8(timestamp, output);



    output->data_len = 8;

    return true;
}bool build_debug_radio_cmd_msg(uint32_t timestamp,, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_DEBUG_RADIO_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes8(timestamp, output);



    output->data_len = 8;

    return true;
}bool build_actuator_status_msg(uint32_t timestamp,enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, enum actuator_states arg2_actuator_states, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ACTUATOR_STATUS | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);

    output->data_len = 6;

    return true;
}bool build_alt_arm_status_msg(uint32_t timestamp,enum arm_states arg0_arm_states, uint8_t arg1_altimeter, uint16_t arg2_drogue_v, uint16_t arg3_main_v, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ALT_ARM_STATUS | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg2) & 0x00FF);
	output->data[4] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[5] = (uint8_t)((arg3) & 0x00FF);
	output->data[6] = (uint8_t)((arg3 >> 8) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_general_board_status_msg(uint32_t timestamp,enum board_status arg0_board_status, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GENERAL_BOARD_STATUS | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);

    output->data_len = 4;

    return true;
}bool build_sensor_temp_msg(uint32_t timestamp,uint8_t arg0_sensor_id, uint32_t arg1_temperature, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_TEMP | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg1 >> 16) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_sensor_altitude_msg(uint32_t timestamp,uint32_t arg0_altitude, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[5] = (uint8_t)((arg0 >> 16) & 0x00FF);
	output->data[6] = (uint8_t)((arg0 >> 24) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_sensor_acc_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ACC | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_acc2_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ACC2 | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_gyro_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_GYRO | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_mag_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_MAG | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_analog_msg(uint32_t timestamp,enum sensor_id arg0_sensor_id, uint16_t arg1_value, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ANALOG | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg1) & 0x00FF);
	output->data[4] = (uint8_t)((arg1 >> 8) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_gps_timestamp_msg(uint32_t timestamp,uint8_t arg0_hrs, uint8_t arg1_mins, uint8_t arg2_secs, uint8_t arg3_dsecs, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_TIMESTAMP | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);
	output->data[6] = (uint8_t)((arg3) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_gps_latitude_msg(uint32_t timestamp,uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_LATITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);
	output->data[6] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[7] = (uint8_t)((arg3) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_gps_longitude_msg(uint32_t timestamp,uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_LONGITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);
	output->data[6] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[7] = (uint8_t)((arg3) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_gps_altitude_msg(uint32_t timestamp,uint16_t arg0_altitude, uint8_t arg1_daltitude, enum unit arg2_unit, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[5] = (uint8_t)((arg1) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_gps_info_msg(uint32_t timestamp,uint8_t arg0_num_sats, uint8_t arg1_quality, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_INFO | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_fill_lvl_msg(uint32_t timestamp,uint8_t arg0_level, enum fill_direction arg1_fill_direction, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_FILL_LVL | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_radi_value_msg(uint32_t timestamp,uint8_t arg0_radi_board, uint16_t arg1_radi, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_RADI_VALUE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);

    output->data_len = 6;

    return true;
}bool build_general_cmd_msg(uint32_t timestamp,enum gen_cmd arg0_gen_cmd, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GENERAL_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);

    output->data_len = 4;

    return true;
}bool build_actuator_cmd_msg(uint32_t timestamp,enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ACTUATOR_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_alt_arm_cmd_msg(uint32_t timestamp,enum arm_states arg0_arm_states, uint8_t arg1_altimeter, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ALT_ARM_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);



    output->data_len = 3;

    return true;
}bool build_reset_cmd_msg(uint32_t timestamp,enum board_id arg0_board_id, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_RESET_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);

    output->data_len = 4;

    return true;
}bool build_debug_msg_msg(uint32_t timestamp,uint8_t arg0_level, uint16_t arg1_line, enum data arg2_data, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_DEBUG_MSG | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg1) & 0x00FF);
	output->data[4] = (uint8_t)((arg2) & 0x00FF);
	output->data[5] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2 >> 16) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_debug_printf_msg(uint32_t timestamp,, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_DEBUG_PRINTF | BOARD_UNIQUE_ID;
    write_timestamp_bytes8(timestamp, output);



    output->data_len = 8;

    return true;
}bool build_debug_radio_cmd_msg(uint32_t timestamp,, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_DEBUG_RADIO_CMD | BOARD_UNIQUE_ID;
    write_timestamp_bytes8(timestamp, output);



    output->data_len = 8;

    return true;
}bool build_actuator_status_msg(uint32_t timestamp,enum actuator_id arg0_actuator_id, enum actuator_states arg1_actuator_states, enum actuator_states arg2_actuator_states, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ACTUATOR_STATUS | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);

    output->data_len = 6;

    return true;
}bool build_alt_arm_status_msg(uint32_t timestamp,enum arm_states arg0_arm_states, uint8_t arg1_altimeter, uint16_t arg2_drogue_v, uint16_t arg3_main_v, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_ALT_ARM_STATUS | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg2) & 0x00FF);
	output->data[4] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[5] = (uint8_t)((arg3) & 0x00FF);
	output->data[6] = (uint8_t)((arg3 >> 8) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_general_board_status_msg(uint32_t timestamp,enum board_status arg0_board_status, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GENERAL_BOARD_STATUS | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);

    output->data_len = 4;

    return true;
}bool build_sensor_temp_msg(uint32_t timestamp,uint8_t arg0_sensor_id, uint32_t arg1_temperature, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_TEMP | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg1 >> 16) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_sensor_altitude_msg(uint32_t timestamp,uint32_t arg0_altitude, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[5] = (uint8_t)((arg0 >> 16) & 0x00FF);
	output->data[6] = (uint8_t)((arg0 >> 24) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_sensor_acc_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ACC | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_acc2_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ACC2 | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_gyro_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_GYRO | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_mag_msg(uint32_t timestamp,uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_MAG | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);
	output->data[7] = (uint8_t)((arg2 >> 8) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_sensor_analog_msg(uint32_t timestamp,enum sensor_id arg0_sensor_id, uint16_t arg1_value, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_SENSOR_ANALOG | BOARD_UNIQUE_ID;
    write_timestamp_bytes2(timestamp, output);

	output->data[2] = (uint8_t)((arg0) & 0x00FF);
	output->data[3] = (uint8_t)((arg1) & 0x00FF);
	output->data[4] = (uint8_t)((arg1 >> 8) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_gps_timestamp_msg(uint32_t timestamp,uint8_t arg0_hrs, uint8_t arg1_mins, uint8_t arg2_secs, uint8_t arg3_dsecs, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_TIMESTAMP | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);
	output->data[6] = (uint8_t)((arg3) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_gps_latitude_msg(uint32_t timestamp,uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_LATITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);
	output->data[6] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[7] = (uint8_t)((arg3) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_gps_longitude_msg(uint32_t timestamp,uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins, enum fill_direction arg3_fill_direction, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_LONGITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg2) & 0x00FF);
	output->data[6] = (uint8_t)((arg2 >> 8) & 0x00FF);
	output->data[7] = (uint8_t)((arg3) & 0x00FF);

    output->data_len = 8;

    return true;
}bool build_gps_altitude_msg(uint32_t timestamp,uint16_t arg0_altitude, uint8_t arg1_daltitude, enum unit arg2_unit, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg0 >> 8) & 0x00FF);
	output->data[5] = (uint8_t)((arg1) & 0x00FF);
	output->data[6] = (uint8_t)((arg2) & 0x00FF);

    output->data_len = 7;

    return true;
}bool build_gps_info_msg(uint32_t timestamp,uint8_t arg0_num_sats, uint8_t arg1_quality, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_GPS_INFO | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_fill_lvl_msg(uint32_t timestamp,uint8_t arg0_level, enum fill_direction arg1_fill_direction, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_FILL_LVL | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);

    output->data_len = 5;

    return true;
}bool build_radi_value_msg(uint32_t timestamp,uint8_t arg0_radi_board, uint16_t arg1_radi, can_msg_t *output);{ 
    if (!output) { return false; }

    output->sid = MSG_RADI_VALUE | BOARD_UNIQUE_ID;
    write_timestamp_bytes3(timestamp, output);

	output->data[3] = (uint8_t)((arg0) & 0x00FF);
	output->data[4] = (uint8_t)((arg1) & 0x00FF);
	output->data[5] = (uint8_t)((arg1 >> 8) & 0x00FF);

    output->data_len = 6;

    return true;
}
int get_general_cmd_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    return true;
}
int get_actuator_cmd_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    return true;
}
int get_alt_arm_cmd_msg(const can_msg_t *msg, uint8_t arg1_altimeter)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!altimeter) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *altimeter = msg->data[4];
    return true;
}
int get_reset_cmd_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    return true;
}
int get_debug_msg_msg(const can_msg_t *msg, uint8_t arg0_level, uint16_t arg1_line)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!level) { return false; }
    if (!line) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *level = msg->data[4];
    *line = msg->data[5];
    return true;
}
int get_debug_printf_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    return true;
}
int get_debug_radio_cmd_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    return true;
}
int get_actuator_status_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    return true;
}
int get_alt_arm_status_msg(const can_msg_t *msg, uint8_t arg1_altimeter, uint16_t arg2_drogue_v, uint16_t arg3_main_v)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!altimeter) { return false; }
    if (!drogue_v) { return false; }
    if (!main_v) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *altimeter = msg->data[4];
    *drogue_v = msg->data[5];
    *main_v = msg->data[6];
    return true;
}
int get_general_board_status_msg(const can_msg_t *msg, )

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    return true;
}
int get_sensor_temp_msg(const can_msg_t *msg, uint8_t arg0_sensor_id, uint32_t arg1_temperature)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!sensor_id) { return false; }
    if (!temperature) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *sensor_id = msg->data[4];
    *temperature = msg->data[5];
    return true;
}
int get_sensor_altitude_msg(const can_msg_t *msg, uint32_t arg0_altitude)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!altitude) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *altitude = msg->data[4];
    return true;
}
int get_sensor_acc_msg(const can_msg_t *msg, uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!x) { return false; }
    if (!y) { return false; }
    if (!z) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *x = msg->data[4];
    *y = msg->data[5];
    *z = msg->data[6];
    return true;
}
int get_sensor_acc2_msg(const can_msg_t *msg, uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!x) { return false; }
    if (!y) { return false; }
    if (!z) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *x = msg->data[4];
    *y = msg->data[5];
    *z = msg->data[6];
    return true;
}
int get_sensor_gyro_msg(const can_msg_t *msg, uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!x) { return false; }
    if (!y) { return false; }
    if (!z) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *x = msg->data[4];
    *y = msg->data[5];
    *z = msg->data[6];
    return true;
}
int get_sensor_mag_msg(const can_msg_t *msg, uint16_t arg0_x, uint16_t arg1_y, uint16_t arg2_z)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!x) { return false; }
    if (!y) { return false; }
    if (!z) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *x = msg->data[4];
    *y = msg->data[5];
    *z = msg->data[6];
    return true;
}
int get_sensor_analog_msg(const can_msg_t *msg, uint16_t arg1_value)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!value) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *value = msg->data[4];
    return true;
}
int get_gps_timestamp_msg(const can_msg_t *msg, uint8_t arg0_hrs, uint8_t arg1_mins, uint8_t arg2_secs, uint8_t arg3_dsecs)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!hrs) { return false; }
    if (!mins) { return false; }
    if (!secs) { return false; }
    if (!dsecs) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *hrs = msg->data[4];
    *mins = msg->data[5];
    *secs = msg->data[6];
    *dsecs = msg->data[7];
    return true;
}
int get_gps_latitude_msg(const can_msg_t *msg, uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!degs) { return false; }
    if (!mins) { return false; }
    if (!dmins) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *degs = msg->data[4];
    *mins = msg->data[5];
    *dmins = msg->data[6];
    return true;
}
int get_gps_longitude_msg(const can_msg_t *msg, uint8_t arg0_degs, uint8_t arg1_mins, uint16_t arg2_dmins)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!degs) { return false; }
    if (!mins) { return false; }
    if (!dmins) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *degs = msg->data[4];
    *mins = msg->data[5];
    *dmins = msg->data[6];
    return true;
}
int get_gps_altitude_msg(const can_msg_t *msg, uint16_t arg0_altitude, uint8_t arg1_daltitude)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!altitude) { return false; }
    if (!daltitude) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *altitude = msg->data[4];
    *daltitude = msg->data[5];
    return true;
}
int get_gps_info_msg(const can_msg_t *msg, uint8_t arg0_num_sats, uint8_t arg1_quality)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!num_sats) { return false; }
    if (!quality) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *num_sats = msg->data[4];
    *quality = msg->data[5];
    return true;
}
int get_fill_lvl_msg(const can_msg_t *msg, uint8_t arg0_level)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!level) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *level = msg->data[4];
    return true;
}
int get_radi_value_msg(const can_msg_t *msg, uint8_t arg0_radi_board, uint16_t arg1_radi)

            {
    if (!msg) { return false; }

    if (!time) { return false; }
    if (!radi_board) { return false; }
    if (!radi) { return false; }
    if (get_message_type(msg) != MSG_GPS_INFO) { return false; }
    *time = msg->data[3];
    *radi_board = msg->data[4];
    *radi = msg->data[5];
    return true;
}