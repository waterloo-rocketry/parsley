import pytest
import parsley

from bitstring import BitString
from fields import ASCII, Enum, Numeric
from parsley_definitions import TIMESTAMP_2, TIMESTAMP_3

import message_types as mt
import test_utils as tu

class TestParsley:
    @pytest.fixture()
    def bit_string2(self, val=0):
        bit_string2 = BitString()
        bit_string2.push(*TIMESTAMP_2.encode(val))
        return bit_string2

    @pytest.fixture()
    def bit_string3(self, val=0):
        bit_string3 = BitString()
        bit_string3.push(*TIMESTAMP_3.encode(val))
        return bit_string3

    def test_general_cmd(self, bit_string3):
        bit_string3.push(*Enum("command", 8, mt.gen_cmd).encode("BUS_DOWN_WARNING"))
        res = parsley.parse("GENERAL_CMD", bit_string3)
        assert res["command"] == "BUS_DOWN_WARNING"

    def test_actuator_cmd(self, bit_string3):
        bit_string3.push(*Enum("actuator", 8, mt.actuator_id).encode("VENT_VALVE"))
        bit_string3.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        res = parsley.parse("ACTUATOR_CMD", bit_string3)
        assert res["actuator"] == "VENT_VALVE"
        assert res["req_state"] == "ACTUATOR_CLOSED"

    def test_alt_arm_cmd(self, bit_string3):
        bit_string3.push(*Enum("state", 4, mt.arm_states).encode("ARMED"))
        bit_string3.push(*Numeric("altimeter", 4).encode(7))
        res = parsley.parse("ALT_ARM_CMD", bit_string3)
        assert res["state"] == "ARMED"
        assert res["altimeter"] == 7

    def test_reset_cmd(self, bit_string3):
        bit_string3.push(*Enum("board_id", 8, mt.board_id).encode("ANY"))
        res = parsley.parse("RESET_CMD", bit_string3)
        assert res["board_id"] == "ANY"

    def test_debug_msg(self, bit_string3):
        bit_string3.push(*Numeric("level", 4).encode(6))
        bit_string3.push(*Numeric("line", 12).encode(0x123))
        bit_string3.push(*ASCII("data", 24, optional=True).encode("AC"))
        res = parsley.parse("DEBUG_MSG", bit_string3)
        assert res["level"] == 6
        assert res["line"] == 0x123
        assert res["data"] == 'AC'

    def test_debug_printf(self):
        bit_string3 = BitString()
        bit_string3.push(*ASCII("string", 64, optional=True).encode("ABCDEFGH"))
        res = parsley.parse("DEBUG_PRINTF", bit_string3)
        assert res["string"] == "ABCDEFGH"

    def test_debug_radio_cmd(self):
        bit_string3 = BitString()
        bit_string3.push(*ASCII("string", 64, optional=True).encode("RADIO"))
        res = parsley.parse("DEBUG_RADIO_CMD", bit_string3)
        assert res["string"] == "RADIO"

    def test_actuator_status(self, bit_string3):
        bit_string3.push(*Enum("actuator", 8, mt.actuator_id).encode("INJECTOR_VALVE"))
        bit_string3.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        bit_string3.push(*Enum("cur_state", 8, mt.actuator_states).encode("ACTUATOR_UNK"))
        res = parsley.parse("ACTUATOR_STATUS", bit_string3)
        assert res["actuator"] == "INJECTOR_VALVE"
        assert res["req_state"] == "ACTUATOR_CLOSED"
        assert res["cur_state"] == "ACTUATOR_UNK"

    def test_alt_arm_status(self, bit_string3):
        bit_string3.push(*Enum("state", 4, mt.arm_states).encode("DISARMED"))
        bit_string3.push(*Numeric("altimeter", 4).encode(4))
        bit_string3.push(*Numeric("drogue_v", 16).encode(12345))
        bit_string3.push(*Numeric("main_v", 16).encode(54321))
        res = parsley.parse("ALT_ARM_STATUS", bit_string3)
        assert res["state"] == "DISARMED"
        assert res["altimeter"] == 4
        assert res["drogue_v"] == 12345
        assert res["main_v"] == 54321

    def test_board_status_nominal(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_NOMINAL"))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_NOMINAL"

    def test_board_status_current(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_BUS_OVER_CURRENT"))
        bit_string3.push(*Numeric("current", 16).encode(12345))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_BUS_OVER_CURRENT"
        assert res["current"] == 12345

    def test_board_status_voltage(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_BUS_UNDER_VOLTAGE"))
        bit_string3.push(*Numeric("voltage", 16).encode(54321))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_BUS_UNDER_VOLTAGE"
        assert res["voltage"] == 54321

    def test_board_status_dead(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_BOARD_FEARED_DEAD"))
        bit_string3.push(*Enum("board_id", 8, mt.board_id).encode("RADIO"))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_BOARD_FEARED_DEAD"
        assert res["board_id"] == "RADIO"

    def test_board_status_quiet(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_NO_CAN_TRAFFIC"))
        bit_string3.push(*Numeric("err_time", 16).encode(54321))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_NO_CAN_TRAFFIC"
        assert res["err_time"] == 54321

    def test_board_status_sensor(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_SENSOR"))
        bit_string3.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_BARO"))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_SENSOR"
        assert res["sensor_id"] == "SENSOR_BARO"

    def test_board_status_actuator(self, bit_string3):
        bit_string3.push(*Enum("status", 8, mt.board_status).encode("E_ACTUATOR_STATE"))
        bit_string3.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        bit_string3.push(*Enum("cur_state", 8, mt.actuator_states).encode("ACTUATOR_UNK"))
        res = parsley.parse("GENERAL_BOARD_STATUS", bit_string3)
        assert res["status"] == "E_ACTUATOR_STATE"
        assert res["req_state"] == "ACTUATOR_CLOSED"
        assert res["cur_state"] == "ACTUATOR_UNK"

    def test_sensor_temp(self, bit_string3):
        bit_string3.push(*Numeric("sensor_id", 8).encode(0x12))
        bit_string3.push(*Numeric("temperature", 24, scale=1/2**10, signed=True).encode(12.5))
        res = parsley.parse("SENSOR_TEMP", bit_string3)
        assert res["sensor_id"] == 0x12
        assert res["temperature"] == tu.approx(12.5)

    def test_sensor_altitude(self, bit_string3):
        bit_string3.push(*Numeric("altitude", 32, signed=True).encode(-12345))
        res = parsley.parse("SENSOR_ALTITUDE", bit_string3)
        assert res["altitude"] == -12345

    def test_sensor_acc(self, bit_string2):
        bit_string2.push(*Numeric("x", 16, scale=8/2**16, signed=True).encode(-2))
        bit_string2.push(*Numeric("y", 16, scale=8/2**16, signed=True).encode(-3))
        bit_string2.push(*Numeric("z", 16, scale=8/2**16, signed=True).encode(-4))
        res = parsley.parse("SENSOR_ACC", bit_string2)
        assert res["x"] == tu.approx(-2)
        assert res["y"] == tu.approx(-3)
        assert res["z"] == tu.approx(-4)

    def test_sensor_gyro(self, bit_string2):
        bit_string2.push(*Numeric("x", 16, scale=2000/2**16, signed=True).encode(3))
        bit_string2.push(*Numeric("y", 16, scale=2000/2**16, signed=True).encode(4))
        bit_string2.push(*Numeric("z", 16, scale=2000/2**16, signed=True).encode(5))
        res = parsley.parse("SENSOR_GYRO", bit_string2)
        assert res["x"] == tu.approx(3)
        assert res["y"] == tu.approx(4)
        assert res["z"] == tu.approx(5)
    
    def test_sensor_mag(self, bit_string2):
        bit_string2.push(*Numeric("x", 16, signed=True).encode(-100))
        bit_string2.push(*Numeric("y", 16, signed=True).encode(-200))
        bit_string2.push(*Numeric("z", 16, signed=True).encode(-300))
        res = parsley.parse("SENSOR_MAG", bit_string2)
        assert res["x"] == tu.approx(-100)
        assert res["y"] == tu.approx(-200)
        assert res["z"] == tu.approx(-300)

    def test_sensor_analog(self, bit_string2):
        bit_string2.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_BARO"))
        bit_string2.push(*Numeric("value", 16).encode(54321))
        res = parsley.parse("SENSOR_ANALOG", bit_string2)
        assert res["sensor_id"] == "SENSOR_BARO"
        assert res["value"] == 54321

    def test_gps_timestamp(self, bit_string3):
        bit_string3.push(*Numeric("hrs", 8).encode(12))
        bit_string3.push(*Numeric("mins", 8).encode(23))
        bit_string3.push(*Numeric("secs", 8).encode(34))
        bit_string3.push(*Numeric("dsecs", 8).encode(45))
        res = parsley.parse("GPS_TIMESTAMP", bit_string3)
        assert res["hrs"] == 12
        assert res["mins"] == 23
        assert res["secs"] == 34
        assert res["dsecs"] == 45

    def test_gps_latitude(self, bit_string3):
        bit_string3.push(*Numeric("degs", 8).encode(12))
        bit_string3.push(*Numeric("mins", 8).encode(23))
        bit_string3.push(*Numeric("dmins", 16).encode(12345))
        bit_string3.push(*ASCII("direction", 8).encode("N"))
        res = parsley.parse("GPS_LATITUDE", bit_string3)
        assert res["degs"] == 12
        assert res["mins"] == 23
        assert res["dmins"] == 12345
        assert res["direction"] == "N"

    def test_gps_longitude(self, bit_string3):
        bit_string3.push(*Numeric("degs", 8).encode(12))
        bit_string3.push(*Numeric("mins", 8).encode(23))
        bit_string3.push(*Numeric("dmins", 16).encode(12345))
        bit_string3.push(*ASCII("direction", 8).encode("W"))
        res = parsley.parse("GPS_LONGITUDE", bit_string3)
        assert res["degs"] == 12
        assert res["mins"] == 23
        assert res["dmins"] == 12345
        assert res["direction"] == "W"

    def test_gps_altitude(self, bit_string3):
        bit_string3.push(*Numeric("altitude", 16).encode(12345))
        bit_string3.push(*Numeric("daltitude", 8).encode(12))
        bit_string3.push(*ASCII("unit", 8).encode("m"))
        res = parsley.parse("GPS_ALTITUDE", bit_string3)
        assert res["altitude"] == 12345
        assert res["daltitude"] == 12
        assert res["unit"] == "m"

    def test_gps_info(self, bit_string3):
        bit_string3.push(*Numeric("num_sats", 8).encode(12))
        bit_string3.push(*Numeric("quality", 8).encode(23))
        res = parsley.parse("GPS_INFO", bit_string3)
        assert res["num_sats"] == 12
        assert res["quality"] == 23

    def test_fill_lvl(self, bit_string3):
        bit_string3.push(*Numeric("level", 8).encode(9))
        bit_string3.push(*Enum("direction", 8, mt.fill_direction).encode("FILLING"))
        res = parsley.parse("FILL_LVL", bit_string3)
        assert res["level"] == 9
        assert res["direction"] == "FILLING"

    def test_radi_value(self, bit_string3):
        bit_string3.push(*Numeric("radi_board", 8).encode(1))
        bit_string3.push(*Numeric("radi", 16).encode(500))
        res = parsley.parse("RADI_VALUE", bit_string3)
        assert res["radi_board"] == 1
        assert res["radi"] == 500

    def test_leds_on(self):
        # LED_ON message has no message body
        pass

    def test_leds_off(self):
        # LED_OFF message has no message body
        pass

    def test_timestamp3(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_3.encode(12.345))
        msg_data.push(*Enum("command", 8, mt.gen_cmd).encode("BUS_DOWN_WARNING"))
        res = parsley.parse("GENERAL_CMD", msg_data)
        assert res["time"] == tu.approx(12.345)
        assert res["command"] == "BUS_DOWN_WARNING"

    def test_timestamp2(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_2.encode(1.234))
        msg_data.push(*Numeric("x", 16, scale=8/2**16, signed=True).encode(-2))
        msg_data.push(*Numeric("y", 16, scale=8/2**16, signed=True).encode(-3))
        msg_data.push(*Numeric("z", 16, scale=8/2**16, signed=True).encode(-4))
        res = parsley.parse("SENSOR_ACC", msg_data)
        assert res["time"] == tu.approx(1.234)
        assert res["x"] == tu.approx(-2)
        assert res["y"] == tu.approx(-3)
        assert res["z"] == tu.approx(-4)