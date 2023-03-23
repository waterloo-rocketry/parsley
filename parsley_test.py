import pytest
from bitstring import BitString
from parsley_definitions import *
import message_types as mt

import parsley

TOLERANCE = 0.01
def approx(value):
    return pytest.approx(value, TOLERANCE)

class TestParsley:


    def timestamp2(self):
        return TIMESTAMP_2.encode(0)
    
    def timestamp3(self):
        return TIMESTAMP_3.encode(0)
    
    def test_general_cmd(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_3.encode(12.345))
        msg_data.push(*Enum("command", 8, mt.gen_cmd).encode("BUS_DOWN_WARNING"))
        res = parsley.parse_cmd("GENERAL_CMD", msg_data)
        assert res["time"] == approx(12.345)
        assert res["command"] == "BUS_DOWN_WARNING"

    def test_actuator_cmd(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("actuator", 8, mt.actuator_id).encode("VENT_VALVE"))
        msg_data.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        res = parsley.parse_cmd("ACTUATOR_CMD", msg_data)
        assert res["actuator"] == "VENT_VALVE"
        assert res["req_state"] == "ACTUATOR_CLOSED"

    def test_alt_arm_cmd(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("state", 4, mt.arm_states).encode("ARMED"))
        msg_data.push(*Numeric("altimeter", 4).encode(7))
        res = parsley.parse_cmd("ALT_ARM_CMD", msg_data)
        assert res["state"] == "ARMED"
        assert res["altimeter"] == 7

    def test_reset_cmd(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("board_id", 8, mt.board_id).encode("ALL"))
        res = parsley.parse_cmd("RESET_CMD", msg_data)
        assert res["board_id"] == "ALL"

    def test_debug_msg(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("level", 4).encode(6))
        msg_data.push(*Numeric("line", 12).encode(0x123))
        msg_data.push(*ASCII("data", 24, optional=True).encode("AC"))
        res = parsley.parse_cmd("DEBUG_MSG", msg_data)
        assert res["level"] == 6
        assert res["line"] == 0x123
        assert res["data"] == 'AC'

    def test_debug_printf(self):
        msg_data = BitString()
        msg_data.push(*ASCII("string", 64, optional=True).encode("ABCDEFGH"))
        res = parsley.parse_cmd("DEBUG_PRINTF", msg_data)
        assert res["string"] == "ABCDEFGH"

    def test_debug_radio_cmd(self):
        msg_data = BitString()
        msg_data.push(*ASCII("string", 64, optional=True).encode("RADIO"))
        res = parsley.parse_cmd("DEBUG_RADIO_CMD", msg_data)
        assert res["string"] == "RADIO"

    def test_actuator_status(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("actuator", 8, mt.actuator_id).encode("INJECTOR_VALVE"))
        msg_data.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        msg_data.push(*Enum("cur_state", 8, mt.actuator_states).encode("ACTUATOR_UNK"))
        res = parsley.parse_cmd("ACTUATOR_STATUS", msg_data)
        assert res["actuator"] == "INJECTOR_VALVE"
        assert res["req_state"] == "ACTUATOR_CLOSED"
        assert res["cur_state"] == "ACTUATOR_UNK"

    def test_alt_arm_status(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("state", 4, mt.arm_states).encode("DISARMED"))
        msg_data.push(*Numeric("altimeter", 4).encode(4))
        msg_data.push(*Numeric("drogue_v", 16).encode(12345))
        msg_data.push(*Numeric("main_v", 16).encode(54321))
        res = parsley.parse_cmd("ALT_ARM_STATUS", msg_data)
        assert res["state"] == "DISARMED"
        assert res["altimeter"] == 4
        assert res["drogue_v"] == 12345
        assert res["main_v"] == 54321

    def test_board_status_nominal(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_NOMINAL"))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_NOMINAL"

    def test_board_status_current(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_BUS_OVER_CURRENT"))
        msg_data.push(*Numeric("current", 16).encode(12345))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_BUS_OVER_CURRENT"
        assert res["current"] == 12345

    def test_board_status_voltage(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_BUS_UNDER_VOLTAGE"))
        msg_data.push(*Numeric("voltage", 16).encode(54321))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_BUS_UNDER_VOLTAGE"
        assert res["voltage"] == 54321

    def test_board_status_dead(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_BOARD_FEARED_DEAD"))
        msg_data.push(*Enum("board_id", 8, mt.board_id).encode("RADIO"))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_BOARD_FEARED_DEAD"
        assert res["board_id"] == "RADIO"

    def test_board_status_quiet(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_NO_CAN_TRAFFIC"))
        msg_data.push(*Numeric("err_time", 16).encode(54321))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_NO_CAN_TRAFFIC"
        assert res["err_time"] == 54321

    def test_board_status_sensor(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_SENSOR"))
        msg_data.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_BARO"))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_SENSOR"
        assert res["sensor_id"] == "SENSOR_BARO"

    def test_board_status_actuator(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_ACTUATOR_STATE"))
        msg_data.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        msg_data.push(*Enum("cur_state", 8, mt.actuator_states).encode("ACTUATOR_UNK"))
        res = parsley.parse_cmd("BOARD_STATUS", msg_data)
        assert res["status"] == "E_ACTUATOR_STATE"
        assert res["req_state"] == "ACTUATOR_CLOSED"
        assert res["cur_state"] == "ACTUATOR_UNK"

    def test_sensor_temp(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("sensor_id", 8).encode(0x12))
        msg_data.push(*Numeric("temperature", 24, scale=1/2**10, signed=True).encode(12.5))
        res = parsley.parse_cmd("SENSOR_TEMP", msg_data)
        assert res["sensor_id"] == 0x12
        assert res["temperature"] == approx(12.5)

    def test_sensor_altitude(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("altitude", 32, signed=True).encode(-12345))
        res = parsley.parse_cmd("SENSOR_ALTITUDE", msg_data)
        assert res["altitude"] == -12345

    def test_sensor_acc(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_2.encode(54.321))
        msg_data.push(*Numeric("x", 16, scale=8/2**16, signed=True).encode(-2))
        msg_data.push(*Numeric("y", 16, scale=8/2**16, signed=True).encode(-3))
        msg_data.push(*Numeric("z", 16, scale=8/2**16, signed=True).encode(-4))
        res = parsley.parse_cmd("SENSOR_ACC", msg_data)
        assert res["time"] == approx(54.321)
        assert res["x"] == approx(-2)
        assert res["y"] == approx(-3)
        assert res["z"] == approx(-4)

    def test_sensor_gyro(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp2())
        msg_data.push(*Numeric("x", 16, scale=2000/2**16, signed=True).encode(3))
        msg_data.push(*Numeric("y", 16, scale=2000/2**16, signed=True).encode(4))
        msg_data.push(*Numeric("z", 16, scale=2000/2**16, signed=True).encode(5))
        res = parsley.parse_cmd("SENSOR_GYRO", msg_data)
        assert res["x"] == approx(3)
        assert res["y"] == approx(4)
        assert res["z"] == approx(5)
    
    def test_sensor_mag(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp2())
        msg_data.push(*Numeric("x", 16, signed=True).encode(-100))
        msg_data.push(*Numeric("y", 16, signed=True).encode(-200))
        msg_data.push(*Numeric("z", 16, signed=True).encode(-300))
        res = parsley.parse_cmd("SENSOR_MAG", msg_data)
        assert res["x"] == approx(-100)
        assert res["y"] == approx(-200)
        assert res["z"] == approx(-300)

    def test_sensor_analog(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp2())
        msg_data.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_BARO"))
        msg_data.push(*Numeric("value", 16).encode(54321))
        res = parsley.parse_cmd("SENSOR_ANALOG", msg_data)
        assert res["sensor_id"] == "SENSOR_BARO"
        assert res["value"] == 54321

    def test_gps_timestamp(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("hrs", 8).encode(12))
        msg_data.push(*Numeric("mins", 8).encode(23))
        msg_data.push(*Numeric("secs", 8).encode(34))
        msg_data.push(*Numeric("dsecs", 8).encode(45))
        res = parsley.parse_cmd("GPS_TIMESTAMP", msg_data)
        assert res["hrs"] == 12
        assert res["mins"] == 23
        assert res["secs"] == 34
        assert res["dsecs"] == 45

    def test_gps_latitude(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("degs", 8).encode(12))
        msg_data.push(*Numeric("mins", 8).encode(23))
        msg_data.push(*Numeric("dmins", 16).encode(12345))
        msg_data.push(*ASCII("direction", 8).encode("N"))
        res = parsley.parse_cmd("GPS_LATITUDE", msg_data)
        assert res["degs"] == 12
        assert res["mins"] == 23
        assert res["dmins"] == 12345
        assert res["direction"] == "N"

    def test_gps_longitude(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("degs", 8).encode(12))
        msg_data.push(*Numeric("mins", 8).encode(23))
        msg_data.push(*Numeric("dmins", 16).encode(12345))
        msg_data.push(*ASCII("direction", 8).encode("W"))
        res = parsley.parse_cmd("GPS_LONGITUDE", msg_data)
        assert res["degs"] == 12
        assert res["mins"] == 23
        assert res["dmins"] == 12345
        assert res["direction"] == "W"

    def test_gps_altitude(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("altitude", 16).encode(12345))
        msg_data.push(*Numeric("daltitude", 8).encode(12))
        msg_data.push(*ASCII("unit", 8).encode("m"))
        res = parsley.parse_cmd("GPS_ALTITUDE", msg_data)
        assert res["altitude"] == 12345
        assert res["daltitude"] == 12
        assert res["unit"] == "m"

    def test_gps_info(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("num_sats", 8).encode(12))
        msg_data.push(*Numeric("quality", 8).encode(23))
        res = parsley.parse_cmd("GPS_INFO", msg_data)
        assert res["num_sats"] == 12
        assert res["quality"] == 23

    def test_fill_lvl(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("level", 8).encode(9))
        msg_data.push(*Enum("direction", 8, mt.fill_direction).encode("FILLING"))
        res = parsley.parse_cmd("FILL_LVL", msg_data)
        assert res["level"] == 9
        assert res["direction"] == "FILLING"

    def test_radi_value(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("radi_board", 8).encode(1))
        msg_data.push(*Numeric("radi", 16).encode(500))
        res = parsley.parse_cmd("RADI_VALUE", msg_data)
        assert res["radi_board"] == 1
        assert res["radi"] == 500

    def test_leds_on(self):
        # LED_ON message has no message body
        pass

    def test_leds_off(self):
        # LED_OFF message has no message body
        pass

class TestBitString:
    def test_bitstring(self):
        bit_str = BitString()
        bit_str.push(b'\xAA', 8)
        bit_str.push(b'\xBB', 8)
        bit_str.push(b'\xCC', 8)
        assert bit_str.pop(24) == b'\xAA\xBB\xCC'

    def test_bitstring_init(self):
        bit_str = BitString(b'\x31\x41')
        assert bit_str.pop(16) == b'\x31\x41'

    def test_bitstring_empty(self):
        bit_str = BitString()
        assert bit_str.pop(0) == b''

    def test_bitstring_LSB(self):
        bit_str = BitString()
        bit_str.push(b'\x00\x10', 16)
        assert bit_str.pop(8) == b'\x00'
        assert bit_str.pop(8) == b'\x10'

    def test_bitstring_non_octet(self):
        bit_str = BitString()
        bit_str.push(b'\x15', 5) # ___1 0101
        bit_str.push(b'\x03', 2) #      __11
        bit_str.push(b'\x01', 2) #      __01
        assert bit_str.pop(9) == b'\x01\x5D' #0001 0101 1101

    def test_bitstring_padding(self):
        bit_str = BitString()
        bit_str.push(b'\xFF', 32)
        assert bit_str.pop(24) == b'\x00\x00\x00'
        assert bit_str.pop(8) == b'\xFF'

    def test_bitstring_push_pop_push(self): # not recommended behaviour
        bit_str = BitString()
        bit_str.push(b'\x81', 8) # 1000 0001
        assert bit_str.pop(6) == b'\x20' # __10 0000
        bit_str.push(b'\x3C', 6) # __11 1100
        assert bit_str.pop(8) == b'\x7C' # 0111 11000

    def test_bitstring_error(self):
        bit_str = BitString()
        bit_str.push(b'\x12', 8)
        with pytest.raises(IndexError):
            bit_str.pop(16)

class TestASCII:
    def test_ASCII(self):
        ascii = ASCII("string", 32)
        (data, length) = ascii.encode('aBcD') # I'm not a huge fan of this coupling, open to ideas
        assert data == b'\x61\x42\x63\x44'
        assert length == 32
        data = ascii.decode(b'\x4C\x4D\x41\x4F')
        assert data == 'LMAO'

    def test_ASCII_leading_spaces(self):
        ascii = ASCII("string", 32)
        assert ascii.decode(b'\x57') == 'W'

    def test_ASCII_decode_encode(self):
        ascii = ASCII("string", 32)
        assert ascii.decode(ascii.encode('1234')[0]) == '1234' # opening a tuple, *gross*, open to ideas

    def test_ASCII_error_not_str(self):
        ascii = ASCII("string", 16)
        with pytest.raises(ValueError): # i don't think it catches the second if the first fails, even if you trying catching a tuple of errors
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
        (data, length) = enum.encode("INJECTOR") # i don't like this coupling with message_types, but it shows the inteded usage
        assert data == b'\x01'
        assert length == 8
        data = enum.decode(b'\x13')
        assert data == "PAPA"

    def test_enum_decode_encode(self):
        map = { "a": 1, "b": 10, "c": 100 }
        enum = Enum("enum", 8, map)
        assert enum.decode(enum.encode("a")[0]) == "a" # opening a tuple, *gross*, open to ideas

    def test_enum_error_injective(self):
        map = { "a": -1, "b": 0, "c": -1 }
        with pytest.raises(ValueError):
            enum = Enum("enum", 8, map)

    def test_enum_error_init_neg(self):
        map = { "a": -1, "b": 0, "c": 1 }
        with pytest.raises(ValueError):
            enum = Enum("enum", 8, map)

    def test_enum_error_length(self):
        map = { "max": 0x3f3f3f3f }
        with pytest.raises(ValueError):
            enum = Enum("enum", 8, map)

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

    # note that for more precise scale values, there will be imprecision after conversion
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
        assert 54.321 == approx(converted_data)

    def test_numeric_decode_encode(self):
        num = Numeric("num", 8)
        assert num.decode(num.encode(255)[0]) == 255 # opening a tuple, *gross*, open to ideas

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
        (data, _) = switch.encode("a")
        assert data == b'\x01'
        assert switch.get_fields(data) == [0, 1]

        assert switch.decode(data) == "a"

# TODO: look into the parse/usb/logger parsing functions
