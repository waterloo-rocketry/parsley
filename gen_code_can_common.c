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
    
        output->data[3] = (uint8_t) gen_cmd; 

    
    output->data_len = 4;

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
    
        output->data[3] = (uint8_t) actuator_id; 
    output->data[4] = (uint8_t) actuator_states; 

    
    output->data_len = 5;

    return true;
}
        
bool build_alt_arm_cmd_msg(uint32_t timestamp,
                               enum ARM_STATES arm_states, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
        output->data[3] = (uint8_t) arm_states; 
    output->data[4] = altimeter; 

    
    output->data_len = 5;

    return true;
}
        
bool build_reset_cmd_msg(uint32_t timestamp,
                               enum BOARD_ID board_id, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
        output->data[3] = (uint8_t) board_id; 

    
    output->data_len = 4;

    return true;
}
        
bool build_debug_msg_msg(uint32_t timestamp,
                        
                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
        output->data[3] = level; 
    output->data[4] = line; 

    
    output->data_len = 6;

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
    
        output->data[3] = (uint8_t) actuator_id; 
    output->data[4] = (uint8_t) actuator_states; 
    output->data[5] = (uint8_t) actuator_states; 

    
    output->data_len = 6;

    return true;
}
        
bool build_alt_arm_status_msg(uint32_t timestamp,
                               enum ARM_STATES arm_states, 
                           uint16_t drogue_v, 
                           uint16_t main_v, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
        output->data[3] = (uint8_t) arm_states; 
    output->data[4] = altimeter; 
    output->data[5] = drogue_v; 
    output->data[6] = main_v; 

    
    output->data_len = 7;

    return true;
}
        
bool build_general_board_status_msg(uint32_t timestamp,
                               enum BOARD_STATUS board_status, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
        output->data[3] = (uint8_t) board_status; 

    
    output->data_len = 4;

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
    
        output->data[3] = (uint8_t) sensor_id; 
    output->data[4] = value; 

    
    output->data_len = 5;

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

    
    output->data_len = 7;

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

    
    output->data_len = 7;

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

    
    output->data_len = 6;

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
                                                   uint8_t level, 
       enum FILL_DIRECTION fill_direction, 

                        can_msg_t *output)

{
    if (!output) { return false; }

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
        output->data[3] = level; 
    output->data[4] = (uint8_t) fill_direction; 

    
    output->data_len = 5;

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
        
int get_general_cmd(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

int get_actuator_cmd(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

bool get_alt_arm_cmd(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    if (!altimeter) { return false; } 


}

int get_reset_cmd(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

bool get_debug_msg(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    if (!level) { return false; } 
    if (!line) { return false; } 


}

bool get_debug_printf(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

bool get_debug_radio_cmd(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

int get_actuator_status(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

bool get_alt_arm_status(const can_msg_t *msg,
                                                   uint16_t drogue_v, 
                           uint16_t main_v, 
)

{
    if (!msg){ return false; }
    if (!altimeter) { return false; } 
    if (!drogue_v) { return false; } 
    if (!main_v) { return false; } 


}

int get_general_board_status(const can_msg_t *msg,
                        )

{
    if (!msg){ return false; }
    

}

bool get_sensor_temp(const can_msg_t *msg,
                        uint8_t sensor_id, 
                           uint24_t temperature, 
)

{
    if (!msg){ return false; }
    if (!sensor_id) { return false; } 
    if (!temperature) { return false; } 


}

bool get_sensor_altitude(const can_msg_t *msg,
                        uint32_t altitude, 
)

{
    if (!msg){ return false; }
    if (!altitude) { return false; } 


}

bool get_sensor_acc(const can_msg_t *msg,
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 
)

{
    if (!msg){ return false; }
    if (!x) { return false; } 
    if (!y) { return false; } 
    if (!z) { return false; } 


}

bool get_sensor_acc2(const can_msg_t *msg,
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 
)

{
    if (!msg){ return false; }
    if (!x) { return false; } 
    if (!y) { return false; } 
    if (!z) { return false; } 


}

bool get_sensor_gyro(const can_msg_t *msg,
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 
)

{
    if (!msg){ return false; }
    if (!x) { return false; } 
    if (!y) { return false; } 
    if (!z) { return false; } 


}

bool get_sensor_mag(const can_msg_t *msg,
                        uint16_t x, 
                           uint16_t y, 
                           uint16_t z, 
)

{
    if (!msg){ return false; }
    if (!x) { return false; } 
    if (!y) { return false; } 
    if (!z) { return false; } 


}

bool get_sensor_analog(const can_msg_t *msg,
                        uint16_t value, 
)

{
    if (!msg){ return false; }
    if (!value) { return false; } 


}

bool get_gps_timestamp(const can_msg_t *msg,
                        uint8_t hrs, 
                           uint8_t mins, 
                           uint8_t secs, 
                           uint8_t dsecs, 
)

{
    if (!msg){ return false; }
    if (!hrs) { return false; } 
    if (!mins) { return false; } 
    if (!secs) { return false; } 
    if (!dsecs) { return false; } 


}

bool get_gps_latitude(const can_msg_t *msg,
                        uint8_t degs, 
                           uint8_t mins, 
                           uint16_t dmins, 
)

{
    if (!msg){ return false; }
    if (!degs) { return false; } 
    if (!mins) { return false; } 
    if (!dmins) { return false; } 


}

bool get_gps_longitude(const can_msg_t *msg,
                        uint8_t degs, 
                           uint8_t mins, 
                           uint16_t dmins, 
)

{
    if (!msg){ return false; }
    if (!degs) { return false; } 
    if (!mins) { return false; } 
    if (!dmins) { return false; } 


}

bool get_gps_altitude(const can_msg_t *msg,
                        uint16_t altitude, 
                           uint8_t daltitude, 
)

{
    if (!msg){ return false; }
    if (!altitude) { return false; } 
    if (!daltitude) { return false; } 


}

bool get_gps_info(const can_msg_t *msg,
                        uint8_t num_sats, 
                           uint8_t quality, 
)

{
    if (!msg){ return false; }
    if (!num_sats) { return false; } 
    if (!quality) { return false; } 


}

bool get_fill_lvl(const can_msg_t *msg,
                        uint8_t level, 
)

{
    if (!msg){ return false; }
    if (!level) { return false; } 


}

bool get_radi_value(const can_msg_t *msg,
                        uint8_t radi_board, 
                           uint16_t radi, 
)

{
    if (!msg){ return false; }
    if (!radi_board) { return false; } 
    if (!radi) { return false; } 


}