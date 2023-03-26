import pytest

from fields import ASCII, Enum, Numeric, Switch

import message_types as mt
import utils.test_utils as test_utils


class TestASCII:
    def test_ASCII(self):
        ascii = ASCII("string", 32)
        (data, length) = ascii.encode('aBcD')
        assert data == b'\x61\x42\x63\x44'
        assert length == 32
        data = ascii.decode(b'\x4C\x4D\x41\x4F')
        assert data == 'LMAO'

    def test_ASCII_leading_spaces(self):
        ascii = ASCII("string", 32)
        assert ascii.decode(b'\x57') == 'W'

    def test_ASCII_decode_encode(self):
        ascii = ASCII("string", 32)
        assert ascii.decode(ascii.encode('1234')[0]) == '1234' # TODO: make a note of not seeing ny better way of decode encode

    def test_ASCII_error_not_str(self):
        ascii = ASCII("string", 16)
        with pytest.raises(ValueError): # TODO: make a note that one with pytest.raises only catches first error
            ascii.encode(b'12')
        with pytest.raises(ValueError):
            ascii.encode(12)

    def test_ASCII_error_not_ASCII(self):
        ascii = ASCII("string", 16)
        with pytest.raises(ValueError):
            ascii.encode('😎')

    def test_ASCII_error_length(self):
        ascii = ASCII("string", 16)
        with pytest.raises(ValueError):
            ascii.encode("xdd")

class TestEnum:
    def test_enum(self):
        enum = Enum("enum", 8, mt.board_id)
        (data, length) = enum.encode("INJECTOR")
        assert data == b'\x01'
        assert length == 8
        data = enum.decode(b'\x13')
        assert data == "PAPA"

    def test_enum_decode_encode(self):
        map = { "a": 1, "b": 10, "c": 100 }
        enum = Enum("enum", 8, map)
        assert enum.decode(enum.encode("a")[0]) == "a"

    def test_enum_error_bijective(self):
        map = { "a": -1, "b": 0, "c": -1 }
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

    def test_numeric_scale_impercision(self):
        num = Numeric("time", 24, scale=1/1000)
        (data, _) = num.encode(54.321)
        converted_data = num.decode(data)
        assert 54.321 == test_utils.approx(converted_data)

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
        enum_map = {
            "a": 0x01,
            "b": 0x02,
            "c": 0x03
        }
        map = {
            "a": [0, 1],
            "b": [1, 2],
            "c": [2, 3]
        }
        switch = Switch(Enum("status", 8, enum_map), map)
        (data, length) = switch.encode("a")
        assert data == b'\x01'
        assert length == 8
        assert switch.get_fields(data) == [0, 1]
        assert switch.decode(data) == "a"