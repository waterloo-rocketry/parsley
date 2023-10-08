import sys
from parsley.message_types import msg_type, board_id, gen_cmd, actuator_states, arm_states, board_status, logger_error, sensor_id, fill_direction, actuator_id
from parsley.message_definitions import MESSAGES
from parsley.fields import Enum

def convert_message_types_to_c(msg_type, board_id, gen_cmd, actuator_states, arm_states, board_status, logger_error, sensor_id, fill_direction, actuator_id):
    msg_type_lines = []
    board_id_lines = []
    gen_cmd_lines = []
    actuator_states_lines = []
    arm_states_lines = []
    board_status_lines = []
    logger_error_lines = []
    sensor_id_lines = []
    fill_direction_lines = []
    actuator_id_lines = []
    
    s1 = set()
    data_dicts = []
    
    
    
    enum_data = [
        {'lines': gen_cmd_lines, 'enum_name': 'GEN_CMD'},
        {'lines': actuator_states_lines, 'enum_name': 'ACTUATOR_STATE'},
        {'lines': arm_states_lines, 'enum_name': 'ARM_STATE'},
        {'lines': board_status_lines, 'enum_name': 'BOARD_STATUS'},
        {'lines': sensor_id_lines, 'enum_name': 'SENSOR_ID'},
        {'lines': fill_direction_lines, 'enum_name': 'FILL_DIRECTION'},
        {'lines': actuator_id_lines, 'enum_name': 'ACTUATOR_ID'}
    ]
    
    
    for k, v in MESSAGES.items():
        for f in v:
            if isinstance(f, Enum):
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
    
        
    c_file_path = "./code_genmessage_types.c"
    with open(c_file_path, "w") as c_file:
       c_file.write("#ifndef MESSAGE_TYPES_H_" + "\n")
       c_file.write("#define MESSAGE_TYPES_H_" + "\n")
       c_file.write("\n")
       
       for python_line in msg_type_lines:
            c_file.write(convert_msg_type_to_c_string(python_line,  "MSG") + "\n")

       for python_line in  board_id_lines:
            c_file.write(convert_msg_type_to_c_string(python_line, 'BOARD') + "\n")
            
       for enum_info in enum_data:
            lines = enum_info['lines']
            enum_name = enum_info['enum_name']
            
            c_file.write(f"enum {enum_name} {{\n")
            
            for idx, python_line in enumerate(lines):
                c_file.write(convert_gen_cmd_to_c_string(python_line) + "\n")
                
                if idx == len(lines) - 1:
                    c_file.write("};\n\n")
                

       c_file.write("#endif // compile guard" + "\n")
            
            
convert_message_types_to_c(msg_type, board_id, gen_cmd, actuator_states, arm_states, board_status, logger_error, sensor_id, fill_direction, actuator_id)