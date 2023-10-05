import sys
sys.path.append('./parsley')
from message_types import msg_type, board_id, gen_cmd, actuator_states, arm_states, board_status, logger_error, sensor_id, fill_direction, actuator_id

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
    
    
    def convert_msg_type_to_c_string(python_line):

        key = python_line[0]
        value = python_line[1]
        c_line = f"#define MSG_{key.strip().upper().replace(' ', '_'):<25} {value:#06X}\n"
        

        return c_line
    
    def convert_board_id_to_c_string(python_line):

        key = python_line[0]
        value = python_line[1]
        c_line = f"#define BOARD_ID_{key.strip().upper().replace(' ', '_'):<25} {value:#06X}\n"
        

        return c_line

    
    for key, value in msg_type.items():
        msg_type_lines.append((key, value))
        
    for key, value in board_id.items():
        board_id_lines.append((key, value))
    
    for key, value in gen_cmd.items():
        gen_cmd_lines.append((key, value))
    
    for key, value in actuator_states.items():
        actuator_states_lines.append((key, value))
        
    for key, value in arm_states.items():
        arm_states_lines.append((key, value))
        
    for key, value in board_status.items():
        board_status_lines.append((key, value))
        
    for key, value in logger_error.items():
        logger_error_lines.append((key, value))
        
    for key, value in sensor_id.items():
        sensor_id_lines.append((key, value))
        
    for key, value in fill_direction.items():
        fill_direction_lines.append((key, value))
        
    for key, value in actuator_id.items():
        actuator_id_lines.append((key, value))
        
            
    c_file_path = "./code_genmessage_types.c"
    with open(c_file_path, "w") as c_file:
       
       for python_line in msg_type_lines:

            c_file.write(convert_msg_type_to_c_string(python_line) + "\n")

       for python_line in  board_id_lines:

            c_file.write(convert_board_id_to_c_string(python_line) + "\n")
            
        
            
        
convert_message_types_to_c(msg_type, board_id, gen_cmd, actuator_states, arm_states, board_status, logger_error, sensor_id, fill_direction, actuator_id)