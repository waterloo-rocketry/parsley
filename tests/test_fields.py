import pytest

from fields import ASCII, Enum, Numeric, Switch

import message_types as mt
import test_utils as tu

class TestASCII:
    def test_ASCII(self):
        a = ASCII("string", 32)
        (data, length) = a.encode('aBcD')
        assert data == b'\x61\x42\x63\x44'
        assert length == 32
        data = a.decode(b'\x4C\x4D\x41\x4F')
        assert data == 'LMAO'

    def test_ASCII_spaces(self):
        a = ASCII("string", 32)
        assert a.decode(b'\x20\x20\x57\x20') == '  W '

    def test_ASCII_front_padding(self):
        a = ASCII("string", 32)
        assert a.decode(b'\x57') == 'W'

    # there is an interesting behaviour when encoding partial ASCII data:
    # we want the text to be left-aligned (instead of the normal right-aligned seen everywhere else)
    def test_ASCII_partial(self):
        a = ASCII("string", 32)
        (data, _) = a.encode("a")
        assert data == b'a\x00\x00\x00'

    def test_ASCII_decode_encode(self):
        a = ASCII("string", 32)
        assert a.decode(a.encode('1234')[0]) == '1234'

    def test_ASCII_empty(self):
        a = ASCII("string", 32, optional=True)
        assert a.encode("")[0] == b'\x00\x00\x00\x00'

    def test_ASCII_error_empty(self):
        a = ASCII("string", 32)
        with pytest.raises(ValueError):
            a.encode("")

    def test_ASCII_error_not_str(self):
        a = ASCII("string", 16)
        with pytest.raises(ValueError):
            a.encode(b'12')
        with pytest.raises(ValueError):
            a.encode(12)

    def test_ASCII_error_not_ASCII(self):
        a = ASCII("string", 16)
        with pytest.raises(ValueError):
            a.encode('😎')

    def test_ASCII_error_length(self):
        a = ASCII("string", 16)
        with pytest.raises(ValueError):
            a.encode("xdd")

class TestEnum:
    def test_enum(self):
        enum = Enum("enum", 8, mt.board_id)
        (data, length) = enum.encode("ACTUATOR_INJ")
        assert data == b'\x01'
        assert length == 8
        data = enum.decode(b'\x13')
        assert data == "USB"

    def test_enum_decode_encode(self):
        map = { "a": 1, "b": 10, "c": 100 }
        enum = Enum("enum", 8, map)
        assert enum.decode(enum.encode("a")[0]) == "a"

    def test_enum_error_bijective(self):
        map = { "a": 1, "b": 0, "c": 1 }
        with pytest.raises(ValueError):
            Enum("enum", 8, map)

    def test_enum_error_init_neg(self):
        map = { "a": -1, "b": 0, "c": 1 }
        with pytest.raises(ValueError):
            Enum("enum", 8, map)

    def test_enum_error_length(self):
        map = { "max": 0x3f3f3f3f }
        with pytest.raises(ValueError):
            Enum("enum", 8, map)

    def test_enum_error_contains(self):
        map = { "a": 1, "b": 2, "c": 3 }
        enum = Enum("enum", 8, map)
        with pytest.raises(ValueError):
            enum.encode("d")

class TestNumeric:
    def test_numeric(self):
        num = Numeric("num", 8)
        (data, length) = num.encode(250)
        assert data == b'\xFA'
        assert length == 8
        data = num.decode(b'\x21')
        assert data == 33

    def test_numeric_scale(self):
        num = Numeric("time", 8, scale=2)
        (data, _) = num.encode(12)
        assert data == b'\x06'

        num = Numeric("time", 8, scale=1/2)
        (data, _) = num.encode(12)
        assert data == b'\x18'

    def test_numeric_scale_imprecision(self):
        num = Numeric("time", 24, scale=1/1000)
        (data, _) = num.encode(54.321)
        converted_data = num.decode(data)
        assert 54.321 == tu.approx(converted_data)

    def test_numeric_decode_encode(self):
        num = Numeric("num", 8)
        assert num.decode(num.encode(255)[0]) == 255

    def test_numeric_error_not_num(self):
        num = Numeric("num", 8)
        with pytest.raises(ValueError):
            num.encode(b'12')
        with pytest.raises(ValueError):
            num.encode("12")

    def test_numeric_error_unsigned(self):
        num = Numeric("num", 8)
        num.encode(0)
        num.encode(255)
        with pytest.raises(ValueError):
            num.encode(-1)
        with pytest.raises(ValueError):
            num.encode(256)
    
    def test_numeric_error_signed(self):
        num = Numeric("num", 8, signed=True)
        num.encode(-128)
        num.encode(0)
        num.encode(127)
        with pytest.raises(ValueError):
            num.encode(-129)
        with pytest.raises(ValueError):
            num.encode(128)

    def test_numeric_error_scale_bounds(self):
        num = Numeric("num", 8, scale=1/4)
        num.encode(0)
        num.encode(63)
        with pytest.raises(ValueError):
            num.encode(-1)
        with pytest.raises(ValueError):
            num.encode(64)

        num = Numeric("num", 8, signed=True, scale=1/4)
        num.encode(-32)
        num.encode(0)
        num.encode(31)
        with pytest.raises(ValueError):
            num.encode(-33)
        with pytest.raises(ValueError):
            num.encode(32)

    def test_numeric_error_neg_scale(self):
        num = Numeric("num", 8, scale=-1/2)
        num.encode(-5)
        with pytest.raises(ValueError):
            num.encode(5)

class TestSwitch:
    def test_switch(self):
        enum = {
            "a": 0x01,
            "b": 0x02,
            "c": 0x03
        }
        map_key_enum = {
            "a": [0, 1],
            "b": [1, 2],
            "c": [2, 3]
        }
        switch = Switch(Enum("status", 8, enum), map_key_enum)
        (data, length) = switch.encode("a")
        assert data == b'\x01'
        assert length == 8
        decoded_data = switch.decode(data)
        assert decoded_data == "a"
        assert switch.get_fields(decoded_data) == [0, 1]
