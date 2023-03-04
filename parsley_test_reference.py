from parsley_definitions import *

# example of writing DEBUG_MSG (for unit test generation)
x = BitString()
x.push(TIMESTAMP_3.encode(12345), 24)
x.push(Numeric("level", 4).encode(7), 4)
x.push(Numeric("line", 12).encode(123), 12)
x.push(Ascii("data", 24).encode("abc"), 24)

# example of reading BitString formatted data
result = {}
for field in FIELDS["DEBUG_MSG"]:
    result[field.name] = field.decode(x.pop(field.length))
