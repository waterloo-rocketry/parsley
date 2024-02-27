
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
                   
                   
    def renderBody(self):
        body_string = ''
        if len(self.layoutBits) > 0:
            for item in self.layoutBits[1:]:
                if isinstance(item, Enum) or isinstance(item, Switch):
                    
                        body_string += f'enum {item.name.upper()} {item.name}, '
                elif isinstance(item, Numeric):
                   if item.length % 8 == 0:
                        if item.name != 'time':
                            if self.layoutBits[1:].index(item) != 0:
                                body_string += f'uint{item.length}_t {item.name}, '
                            else:
                                body_string += f'uint{item.length}_t {item.name}, \n'
        return body_string
    
    def renderEnums(self):
            enums_string = ''
            if len(self.enums) > 0:
                for enum in self.enums[1:]:
                    if self.enums[1:].index(enum) != 0:
                        enums_string += f'\tenum {enum.name.upper()} {enum.name}, \n'
                    else:
                        enums_string += f'\tenum {enum.name.upper()} {enum.name}, \n'
            return enums_string
        
    def renderNumerics(self):
            numerics_string = ''
            if len(self.numerics) > 0:
                for num in self.numerics[1:]:
                    if num.length % 8 == 0:
                        if self.numerics[1:].index(num) != 0:
                            numerics_string += f'\tuint{num.length}_t {num.name}, \n'
                        else:
                            numerics_string += f'\tuint{num.length}_t {num.name}, \n'
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
bool build_{self.name.lower()}_msg(uint32_t timestamp, {self.renderBody()}can_msg_t *output){endVal}
'''
        return c_code
    
    def convert_to_c_build_body(self):
        def renderBodyData():
            body_string = ''
            if len(self.layoutBits) > 0:
                for item in self.layoutBits[1:]:
                    if isinstance(item, Enum) or isinstance(item, Switch):
                        if self.layoutBits[1:].index(item) == 0:
                            body_string += f'\toutput->data[{self.layoutBits[1:].index(item)+2}] = (uint8_t) {item.name}; \n'
                        else:
                            body_string += f'\toutput->data[{self.layoutBits[1:].index(item)+2}] = (uint8_t) {item.name}; \n'
                    elif isinstance(item, Numeric):
                        if item.name != 'time':
                            if self.layoutBits[1:].index(item) == 0:
                                body_string += f'\toutput->data[{self.layoutBits[1:].index(item)+2}] = {item.name}; \n'
                            else:
                                body_string += f'\toutput->data[{self.layoutBits[1:].index(item)+2}] = {item.name}; \n'
                        
            return body_string
        bodyCode = f'''
{'{'}
    if (!output) {'{'} return false; {'}'}

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
{renderBodyData()}
    output->data_len = {len(self.layoutBits[1:])+2};

    return true;
{'}'}
        '''
        return bodyCode

    def convert_to_c_get_function(self, hasBody=False):
        endVal = '' if hasBody else ';'
        int_or_bool = 'bool' if len(self.numerics) != 1 else 'int'
        c_code = (f''
                  f'{int_or_bool} get_{self.name.lower()}(const can_msg_t *msg,'
                  f'{self.renderNumerics()}){endVal}')
        if self.renderNumerics() == '': c_code = c_code.replace(',', '')
        return c_code

    def convert_to_c_get_body(self):
        body_string = ''

        if len(self.numerics) > 0:
            for num in self.numerics[1:]:
                body_string += f'\tif (!{num.name}) {"{ return false; }"}\n'

        body_string += f'\tif (get_message_type(msg) != MSG_{self.name}) {"{"}return false;{"}"}\n'
        body_string += '\n'

        if len(self.numerics) > 0:
            for num in self.numerics:
                if num.name != 'time':
                    if isinstance(num, Numeric) and num.length > 8:
                        for i in range(1, int(num.length / 8) + 1):
                            body_string += f'\t*{num.name} = (uint{num.length}_t)msg->data[{self.layoutBits[1:].index(num) + i + 1}] << {int(num.length / i)} | msg->data[{self.layoutBits[1:].index(num) + i + 2}];\n'
                    else:
                        body_string += f'\t*{num.name} = msg->data[{self.layoutBits[1:].index(num) + 2}];\n'

        bodyCode = (f'\n'
                    f'{"{"}\n'
                    f'\tif (!msg) {"{ return false; }"}\n'
                    f'{body_string}\n'
                    f'\treturn true;\n'
                    f'{"}"}\n')

        return bodyCode
    
    
    
        
        

