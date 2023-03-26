## Parsley
```Parsley``` is a library for transcoding between raw Controller Area Network (CAN) messages and human-readable text.

## Features
- ```bitstring.py```: Provides a custom data structure for storing and reading bits of arbitrary-length.
- ```fields.py```: Introduces data types for transcoding byte strings, such as ASCII and Numeric.
- ```parsley_defintions.py```: Offers a new architecture for defining CAN messages

## Requirements
```Python 3.10``` or newer is required and the required packages can be installed using `pip install -r requirements.txt`

## Examples

``` python
import parsley
import message_types as mt

# Encoding a GENERAL_CMD CAN message
msg_data = BitString()
msg_data.push(*TIMESTAMP_3.encode(12.345)) #12.345 minutes
msg_data.push(*Enum("command", 8, mt.gen_cmd).encode("BUS_DOWN_WARNING"))

# Decoding a CAN message
result = parsley.parse("GENERAL_CMD", msg_data)

```

## Testing

<!-- TODO: Add how to include parsley as a submodule into other libraries -->

<!-- TODO: I remember the guy who added Omnibus's parsley needed to do some license thing -->