
from parsley.message_definitions import MESSAGES
from parsley.fields import Enum, Numeric, Switch


def convert_can_common_to_c(c_file_path="./code_can_common.c"):
    constant_c_code = """#ifndef CAN_COMMON_H_
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
#define LOG_MSG(debug_macro_level, debug_macro_timestamp, debug_macro_output) \\
    do { \\
        uint8_t debug_macro_data[5] = {(debug_macro_level << 4) | ((__LINE__ >> 8) & 0xF), \\
                                       __LINE__ & 0xFF, \\
                                       0,0,0}; \\
        build_debug_msg( debug_macro_timestamp, \\
                         debug_macro_data, \\
                         &debug_macro_output); \\
    } while(0)
"""
    
    def convert_to_c_build_function(name, enums, numerics):
        enum_names = {'command': 'gen_cmd', 'actuator': 'actuator_id', 'req_state': 'actuator_states',
            'state': 'arm_states', 'board_id': 'board_id', 'status': 'board_status', 'sensor_id': 'sensor_id',
            'direction': 'fill_direction', 'cur_state': 'actuator_states'         
        }
        def renderEnums():
            enums_string = ''
            if len(enums) > 0:
                for enum in enums[1:]:
                    if enums[1:].index(enum) != 0:
                        enums_string += f'                           enum {enum_names[enum.name].upper()} {enum_names[enum.name]}, \n'
                    else:
                        enums_string += f'enum {enum_names[enum.name].upper()} {enum_names[enum.name]}, \n'
            return enums_string
        def renderNumerics():
            numerics_string = ''
            if len(numerics) > 0:
                for num in numerics[1:]:
                    if numerics[1:].index(num) != 0:
                        numerics_string += f'                           uint{num.length}_t {num.name}, \n'
                    else:
                        numerics_string += f'uint{num.length}_t {num.name}, \n'
            return numerics_string
        #print(enumVal.values)
        c_code = f'''
bool build_{name.lower()}_msg(uint32_t timestamp,
                           {renderEnums()}
                           {renderNumerics()}
                           can_msg_t *output);
'''
        return c_code
    
    with open(c_file_path, "w") as c_file:
       c_file.write(constant_c_code)
       
       for k, v in list(MESSAGES.items())[:-2]:
           enums = []
           numerics = []
           for i in v:
               if isinstance(i, Enum) or isinstance(i, Switch):
                   enums.append(i)
               elif isinstance(i, Numeric):
                   numerics.append(i)
                   
           c_file.write(convert_to_c_build_function(k, enums, numerics) + '\n')
       



#convert_can_common_to_c()
       