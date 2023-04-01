## Parsley
```Parsley``` is a library for transcoding between Controller Area Network (CAN) messages and human-readable text.

## Highlights
- ```bitstring.py```: Provides a custom data structure to store and read bits of arbitrary-length.
- ```fields.py```:  Defines custom data types for transcoding byte strings such as ASCII and numerical data.
- ```parsley_defintions.py```: Offers a new architecture for defining CAN messages.
- Enhanced error handling across all stages of transcoding.

## Example

``` python
import parsley
import parsley_definitions as pd
import tests.test_utils as tu
from bitstring import BitString

# Encoding a DEBUG_MSG CAN message
bit_str = BitString()
bit_str.push(*pd.TIMESTAMP_3.encode(12.345)) # 12.345 seconds
bit_str.push(*pd.Numeric("level", 4).encode(6))
bit_str.push(*pd.Numeric("line", 12).encode(0x123))
bit_str.push(*pd.ASCII("data", 24, optional=True).encode("T_T"))
"""
The data encoded in bit_str looks like:
          |=> level of 6
          |
          |    T_T encoded in ASCII
          |       |--------|
\x30\x39\x61\x23\x54\x5f\x54
|------|   |---|
|        line of 0x123
|=> 12345 milliseconds
"""

# Creating the full CAN message
msg_sid = tu.create_msg_sid_from_strings("DEBUG_MSG", "PAPA_SPARE")
msg_data = bit_str.pop(64)

# Decoding a CAN message
result = parsley.parse_raw(msg_sid, msg_data)
"""
result = {
    'msg_type' = 'DEBUG_MSG',
    'board_id' = 'PAPA_SPARE',
    'time': 12.345,
    'level': 6,
    'line': 291, 
    'data': 'T_T'
}
"""
```

## Requirements
```Python 3.10``` or newer is required and the required packages can be installed using `pip install -r requirements.txt`

<!-- TODO: Mention how to include parsley as a submodule into other projects -->
