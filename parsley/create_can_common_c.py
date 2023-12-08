
from parsley.message_definitions import MESSAGES
from parsley.fields import Enum, Numeric, Switch, ASCII

def convert_can_common_to_c(c_file_path="./gen_code_can_common.c"):
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


    with open(c_file_path, "w") as c_file:
        c_file.write(constant_c_code)
        for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.get_builder_signature(hasBody=True))
               c_file.write(v.get_builder_body())
        for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.get_builder_signature(hasBody=True))
               c_file.write(v.get_builder_body())
        for k, v in list(MESSAGES.items())[:-2]:
               c_file.write(v.getter_signature())
               c_file.write(v.get_getter_body())
               
        