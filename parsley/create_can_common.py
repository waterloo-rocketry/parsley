
from parsley.message_definitions import MESSAGES
from parsley.fields import Enum, Numeric, Switch, ASCII


def convert_can_common_to_h(c_file_path="./gen_code_can_common.h"):
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
    
    
    
    with open(c_file_path, "w") as c_file:
       c_file.write(constant_c_code)
       for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.get_builder_signature())
               
       for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.convert_to_c_get_function())
               
       
      
       c_file.write('#endif // compile guard')
       



#convert_can_common_to_c()
       