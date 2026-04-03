## Parsley
```Parsley``` is a library to transcode Controller Area Network (CAN) and human-readable messages.

## Highlights
- ```bitstring.py```: Provides a custom data structure to store and read bits of arbitrary-length.
- ```fields.py```:  Defines custom data types for transcoding byte strings such as ASCII and numerical data.
- ```payloads.py```: Offers typed dataclass-based CAN message payload definitions.
- Enhanced error handling across all stages of transcoding.

## Example

``` python
from parsley import BitString, TIMESTAMP_2
from parsley.fields import Numeric, ASCII
from parsley.payloads import DEBUG_RAW
from parsley.parse_to_object import USBDebugParser

# Encoding a DEBUG_RAW payload
payload = DEBUG_RAW(time=1.0, string='Hello')
encoded = payload.to_bytes()
# encoded == b'\x03\xe8Hello\x00'

# Decoding a USB debug line
parser = USBDebugParser()
result = parser.parse("$08190200:03,E8,48,65,6C,6C,6F,00")
# result.data is a DEBUG_RAW instance with .time and .string fields

```

## Using Parsley

The easiest way to include parsley is through `uv` if your project uses it. Run `uv add git+https://github.com/waterloo-rocketry/parsley` to add to your project. 

You can also include parsley as a submodule in your project with ```git submodule add https://github.com/waterloo-rocketry/parsley.git``` and to pull the submodule as a developer, you can use ```git submodule update --init --recursive```

## Requirements
**You must have the `uv` Python package manager and builder installed. Visit https://docs.astral.sh/uv/getting-started/installation/ to get started. If you don't know otherwise, choose the "Standalone Installer".**

1. Run `uv sync`
2. Source virtual environment in `.venv`
3. To build, run `uv build`
