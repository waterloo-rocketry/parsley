
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
                    if item.length % 8 == 0 and item.name != 'time':
                        body_string += f'uint{item.length}_t {item.name}, '
                        if self.layoutBits[1:].index(item) == 0:
                            body_string += '\n'

        return body_string

    def renderEnums(self):
        enums_string = ''
        if len(self.enums) > 0:
            for enum in self.enums[1:]:
                enums_string += f'\tenum {enum.name.upper()} {enum.name}, \n'
        return enums_string

    def renderNumerics(self):
        numerics_string = ''
        if len(self.numerics) > 0:
            for num in self.numerics[1:]:
                if num.length % 8 == 0:
                    numerics_string += f', uint{num.length}_t {num.name}'
        return numerics_string

    def convert_msg_type_to_define_msg_c(self):
        return f"#define MSG_{self.name.strip().upper().replace(' ', '_'):<25} {0:#06X}\n"

    def convert_msg_type_to_board_msg_c(self):
        return f"#define BOARD_ID_{self.name.strip().upper().replace(' ', '_'):<25} {0:#06X}\n"

    def convert_to_c_build_function(self, hasBody=False):

        endVal = ';'
        if hasBody:
            endVal = ''
        return (f'\n'
                f'bool build_{self.name.lower()}_msg(uint32_t timestamp, {self.renderBody()}can_msg_t *output){endVal}'
                f'\n')

    def convert_to_c_build_body(self):
        def renderBodyData():
            body_string = ''
            if len(self.layoutBits) > 0:
                for item in self.layoutBits[1:]:
                    if isinstance(item, Enum) or isinstance(item, Switch):
                        body_string += f'\toutput->data[{self.layoutBits[1:].index(item) + 2}] = (uint8_t) {item.name}; \n'
                    elif isinstance(item, Numeric) and item.name != 'time':
                            body_string += f'\toutput->data[{self.layoutBits[1:].index(item) + 2}] = {item.name}; \n'

            return body_string

        with open('Parsley/c_build_function.txt', 'r') as file:
            bodyCode = file.read().format(body=renderBodyData(), len=len(self.layoutBits[1:]) + 2)

        return bodyCode

    def convert_to_c_get_function(self, hasBody=False):
        endVal = '' if hasBody else ';'
        int_or_bool = 'bool' if len(self.numerics) != 1 else 'int'
        c_code = (f'{int_or_bool} get_{self.name.lower()}(const can_msg_t *msg'
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

        with open('Parsley/c_get_function.txt', 'r') as file:
            bodyCode = file.read().format(body_string)

        return bodyCode
