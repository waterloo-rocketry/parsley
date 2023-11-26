from parsley.fields import Enum, Numeric, Switch, ASCII, Field


class Message:
    name : str
    field_layout : list[Field]

    def __init__(self, name : str, layoutBits : list[Field]):
        self.name = name
        self.field_layout = layoutBits
        self.enums = []
        self.numerics = []
        self.map_key_val = self.field_layout[0].map_key_val
        
        for i in self.field_layout:
               if isinstance(i, Enum) or isinstance(i, Switch):
                   self.enums.append(i)
               elif isinstance(i, Numeric):
                   self.numerics.append(i)

    @staticmethod
    def render_enum_arg(item : Field, idx : int):
        return f'enum {item.name()} arg{idx}_{item.name}'
    
    @staticmethod
    def render_numeric_arg(item : Numeric, idx : int):
        length = 8 if (item.length <=8) else 16 if (item.length <=16) else 32
        return f'uint{length}_t arg{idx}_{item.name}'
                   
    def render_arguments(self):
        args = [
            (Message.render_numeric_arg(f, idx) if isinstance(f, Numeric) else Message.render_enum_arg(f, idx))
            for idx, f in enumerate(self.field_layout[2:]) # crop out board id and timestamp
        ]
        return ', '.join(args)
    
    def get_builder_signature(self, hasBody=False):
        c_code = f"bool build_{self.name.lower()}_msg(uint32_t timestamp,{self.render_arguments()}, can_msg_t *output){';' if hasBody else ''}"
        return c_code
    
    def get_builder_body(self):
        def renderBodyData():
            body_string = ''
            if len(self.field_layout) > 0:
                for item in self.field_layout[1:]:
                    if isinstance(item, Enum) or isinstance(item, Switch):
                        if self.field_layout[1:].index(item) == 0:
                            body_string += f'output->data[{self.field_layout[1:].index(item)+2}] = (uint8_t) {item.name}; \n'
                        else:
                            body_string += f'    output->data[{self.field_layout[1:].index(item)+2}] = (uint8_t) {item.name}; \n'
                    elif isinstance(item, Numeric):
                        if item.name != 'time':
                            if self.field_layout[1:].index(item) == 0:
                                body_string += f'output->data[{self.field_layout[1:].index(item)+2}] = {item.name}; \n'
                            else:
                                body_string += f'    output->data[{self.field_layout[1:].index(item)+2}] = {item.name}; \n'
                        
            return body_string
        bodyCode = f'''
{'{'}
    if (!output) {'{'} return false; {'}'}

    output->sid = MSG_GPS_ALTITUDE | BOARD_UNIQUE_ID;
    write_timestamp_3bytes(timestamp, output);        
    
    {renderBodyData()}
    
    output->data_len = {len(self.field_layout[1:])+2};

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
    
    
    
        
        

