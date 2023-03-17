from parsley_definitions import *

# example of writing DEBUG_MSG (for unit test generation)
x = BitString()
x.push(*TIMESTAMP_3.encode(12345))
x.push(*Numeric("level", 4).encode(7))
x.push(*Numeric("line", 12).encode(123))
x.push(*ASCII("data", 24).encode("abc"))

# example of reading BitString formatted data
result = {}
for field in FIELDS["DEBUG_MSG"]:
    result[field.name] = field.decode(x.pop(field.length))

# example of writing SWITCH cases
y = BitString()
y.push(*TIMESTAMP_3.encode(14159))
y.push(*Enum("status", 8, mt.board_stat_hex).encode("E_BUS_OVER_CURRENT"))
y.push(*Numeric("current", 16).encode(2653))

result2 = {}
for field in FIELDS["BOARD_STATUS"]:
    data = y.pop(field.length)
    if isinstance(field, Switch):
        result2[field.name] = field.decode(data)
        nested_fields = field.get_fields(data)
        # in the actual code, probably make this recursive
        for nested_field in nested_fields:
            data = y.pop(nested_field.length)
            result2[nested_field.name] = nested_field.decode(data)
    else:
        result2[field.name] = field.decode(data)

z = BitString()
z.push(*ASCII("string", 64).encode("HeY"))

result3 = {}
for field in FIELDS["DEBUG_PRINTF"]:
    data = z.pop(field.length)
    result3[field.name] = field.decode(data)

# TODO: change field encode to retunr tuple, first is bytes second is lenght so thtat
# when you do bitstring.push(encode) you don't have to manually specify the number anymore
