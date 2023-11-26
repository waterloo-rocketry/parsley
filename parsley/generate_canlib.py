from parsley.message_definitions import MESSAGES, MESSAGE_TYPE
from parsley.fields import Enum, Numeric, Switch, ASCII

def generate_canlib(output_directory='parsley\canlib'):
    constant_c_code = """#include "can_common.h"
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
"""


    with open(output_directory+'\gen_code_can_common.c', "w") as c_file:
        c_file.write(constant_c_code)
        for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.convert_to_c_build_function(hasBody=True))
               c_file.write(v.convert_to_c_build_body())
        for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.convert_to_c_get_function(hasBody=True))
               c_file.write(v.convert_c_to_get_body())
               
               
    constant_c_common_code = """#ifndef CAN_COMMON_H_
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
    
    
    
    with open(output_directory+'\gen_code_can_common.h', "w") as c_file:
       c_file.write(constant_c_common_code)
       for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.convert_to_c_build_function())
               
       for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.convert_to_c_get_function())
               
       
      
       c_file.write('#endif // compile guard')
       
    s1 = set(['board_id'])
    data_dicts = []
    define_type_dicts = []
    
    define_type_dicts.append({'data_dict':MESSAGE_TYPE.map_key_val, 'lines_list':[], 'enum_name': MESSAGE_TYPE.name})

    for k, v in MESSAGES.items():
        print(v.field_layout[0].map_key_val)
        for f in v.field_layout:
            if isinstance(f, Enum):
                if f.name == 'board_id':
                    define_type_dicts.append({'data_dict':f.map_key_val, 'lines_list':[], 'enum_name': f.name})
                     
                if f.name not in s1:
                    s1.add(f.name)
                    data_dicts.append({'data_dict':f.map_key_val, 'lines_list':[], 'enum_name': f.name})
    
    
    def convert_msg_type_to_c_string(python_line, type):

        key = python_line[0]
        value = python_line[1]
        if type == 'MSG':
            c_line = f"#define MSG_{key.strip().upper().replace(' ', '_'):<25} {value:#06X}\n"
        else:
            c_line = f"#define BOARD_ID_{key.strip().upper().replace(' ', '_'):<25} {value:#06X}\n"
        
        return c_line
    
    
    def convert_gen_cmd_to_c_string(python_line):

        key = python_line[0]
        value = python_line[1]
        
        if value == 0:    
            c_line = f"    {key} = {value},"
        else:
            c_line = f"    {key},"
        
        return c_line
    
    for data_entry in data_dicts:
        for key, value in data_entry['data_dict'].items():
            data_entry['lines_list'].append((key, value))
    
        
    with open(output_directory+'\gen_message_types.h', "w") as c_file:
       c_file.write("#ifndef MESSAGE_TYPES_H_" + "\n")
       c_file.write("#define MESSAGE_TYPES_H_" + "\n")
       c_file.write("\n")
       

       
       for dict in range(len(define_type_dicts)):

        for key, value in define_type_dicts[dict]['data_dict'].items():
            if dict == 0:
                c_file.write(convert_msg_type_to_c_string((key, value),  "MSG") + "\n")
            elif dict == 1:
                c_file.write(convert_msg_type_to_c_string((key, value), 'BOARD') + "\n")
            
       for enum_info in data_dicts:
            lines = enum_info['lines_list']
            enum_name = enum_info['enum_name']
            
            c_file.write(f"enum {enum_name} {{\n")
            
            for idx, python_line in enumerate(lines):
                c_file.write(convert_gen_cmd_to_c_string(python_line) + "\n")
                
                if idx == len(lines) - 1:
                    c_file.write("};\n\n")
                
       c_file.write("#endif // compile guard" + "\n")
               
               