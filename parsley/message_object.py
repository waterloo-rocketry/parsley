
from parsley.fields import Enum, Numeric, Switch, ASCII


class Message:
    def __init__(self, name, layoutBits):
        self.name = name
        self.layoutBits = layoutBits
        self.enums = []
        self.numerics = []
        self.map_key_val = self.layoutBits[0].map_key_val
        
        for i in self.layoutBits:
               if isinstance(i, Enum) or isinstance(i, Switch):
                   self.enums.append(i)
               elif isinstance(i, Numeric):
                   self.numerics.append(i)
                   
    def renderEnums(self):
            enums_string = ''
            if len(self.enums) > 0:
                for enum in self.enums[1:]:
                    if self.enums[1:].index(enum) != 0:
                        enums_string += f'                           enum {enum.name.upper()} {enum.name}, \n'
                    else:
                        enums_string += f'enum {enum.name.upper()} {enum.name}, \n'
            return enums_string
        
    def renderNumerics(self):
            numerics_string = ''
            if len(self.numerics) > 0:
                for num in self.numerics[1:]:
                    if self.numerics[1:].index(num) != 0:
                        numerics_string += f'                           uint{num.length}_t {num.name}, \n'
                    else:
                        numerics_string += f'uint{num.length}_t {num.name}, \n'
            return numerics_string
        
        
    def convert_msg_type_to_define_msg_c(self):
        c_line = f"#define MSG_{self.name.strip().upper().replace(' ', '_'):<25} {0:#06X}\n"
        
        return c_line
    
    def convert_msg_type_to_board_msg_c(self):
        c_line = f"#define BOARD_ID_{self.name.strip().upper().replace(' ', '_'):<25} {0:#06X}\n"
        
        return c_line
    
    def convert_to_c_build_function(self, hasBody=False):
        
        endVal = ';'
        if hasBody:
            endVal = ''
        c_code = f'''
bool build_{self.name.lower()}_msg(uint32_t timestamp,
                        {self.renderEnums()}
                        {self.renderNumerics()}
                        can_msg_t *output){endVal}
'''
        return c_code
    
    def convert_to_c_build_body(self):
        def renderbodyNumericData():
            numerics_body_string = ''
            if len(self.numerics) > 0:
                for num in self.numerics[1:]:
                    if self.numerics[1:].index(num) == 0:
                        numerics_body_string += f'output->data[{self.numerics[1:].index(num)+3}] = {num.name}; \n'
                    else:
                        numerics_body_string += f'    output->data[{self.numerics[1:].index(num)+3}] = {num.name}; \n'
                        
            return numerics_body_string
        bodyCode = f'''
{'{'}
    if (!output) {'{'} return false; {'}'}

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    {renderbodyNumericData()}
    
    output->data_len = {len(self.numerics[1:])+3};

    return true;
{'}'}
        '''
        return bodyCode
    
    def convert_to_c_get_function(self, hasBody=False):
        endVal = ';'
        if hasBody:
            endVal = ''
        int_or_bool = 'int'
        if len(self.numerics) != 1:
            int_or_bool = 'bool'
        else:
            int_or_bool = 'int'
        
        c_code = f'''
{int_or_bool} get_{self.name.lower()}(const can_msg_t *msg,
                        {self.renderNumerics()}){endVal}
'''
        return c_code
    
    def convert_c_to_get_body(self):
        def renderbodyNumericData():
            numerics_body_string = ''
            if len(self.numerics) > 0:
                for num in self.numerics[1:]:
                    if self.numerics[1:].index(num) == 0:
                        numerics_body_string += f'if (!{num.name}) {"{ return false; }"} \n'
                    else:
                        numerics_body_string += f'    if (!{num.name}) {"{ return false; }"} \n'
                        
            return numerics_body_string
        bodyCode = f'''
{'{'}
    if (!msg){"{ return false; }"}
    {renderbodyNumericData()}

{'}'}
'''
        
        return bodyCode
    
    
    
        
        

