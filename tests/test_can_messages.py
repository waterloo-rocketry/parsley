import parsley

from bitstring import BitString
from fields import ASCII, Enum, Numeric
from parsley_definitions import TIMESTAMP_2, TIMESTAMP_3

import message_types as mt
import utils.test_utils as test_utils

class TestParsley:
    def timestamp2(self):
        return TIMESTAMP_2.encode(0)
    
    def timestamp3(self):
        return TIMESTAMP_3.encode(0)
    
    def test_general_cmd(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_3.encode(12.345))
        msg_data.push(*Enum("command", 8, mt.gen_cmd).encode("BUS_DOWN_WARNING"))
        res = parsley.parse("GENERAL_CMD", msg_data)
        assert res["time"] == test_utils.approx(12.345)
        assert res["command"] == "BUS_DOWN_WARNING"

    def test_actuator_cmd(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("actuator", 8, mt.actuator_id).encode("VENT_VALVE"))
        msg_data.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        res = parsley.parse("ACTUATOR_CMD", msg_data)
        assert res["actuator"] == "VENT_VALVE"
        assert res["req_state"] == "ACTUATOR_CLOSED"

    def test_alt_arm_cmd(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("state", 4, mt.arm_states).encode("ARMED"))
        msg_data.push(*Numeric("altimeter", 4).encode(7))
        res = parsley.parse("ALT_ARM_CMD", msg_data)
        assert res["state"] == "ARMED"
        assert res["altimeter"] == 7

    def test_reset_cmd(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("board_id", 8, mt.board_id).encode("ALL"))
        res = parsley.parse("RESET_CMD", msg_data)
        assert res["board_id"] == "ALL"

    def test_debug_msg(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("level", 4).encode(6))
        msg_data.push(*Numeric("line", 12).encode(0x123))
        msg_data.push(*ASCII("data", 24, optional=True).encode("AC"))
        res = parsley.parse("DEBUG_MSG", msg_data)
        assert res["level"] == 6
        assert res["line"] == 0x123
        assert res["data"] == 'AC'

    def test_debug_printf(self):
        msg_data = BitString()
        msg_data.push(*ASCII("string", 64, optional=True).encode("ABCDEFGH"))
        res = parsley.parse("DEBUG_PRINTF", msg_data)
        assert res["string"] == "ABCDEFGH"

    def test_debug_radio_cmd(self):
        msg_data = BitString()
        msg_data.push(*ASCII("string", 64, optional=True).encode("RADIO"))
        res = parsley.parse("DEBUG_RADIO_CMD", msg_data)
        assert res["string"] == "RADIO"

    def test_actuator_status(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("actuator", 8, mt.actuator_id).encode("INJECTOR_VALVE"))
        msg_data.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        msg_data.push(*Enum("cur_state", 8, mt.actuator_states).encode("ACTUATOR_UNK"))
        res = parsley.parse("ACTUATOR_STATUS", msg_data)
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
        res = parsley.parse("ALT_ARM_STATUS", msg_data)
        assert res["state"] == "DISARMED"
        assert res["altimeter"] == 4
        assert res["drogue_v"] == 12345
        assert res["main_v"] == 54321

    def test_board_status_nominal(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_NOMINAL"))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_NOMINAL"

    def test_board_status_current(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_BUS_OVER_CURRENT"))
        msg_data.push(*Numeric("current", 16).encode(12345))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_BUS_OVER_CURRENT"
        assert res["current"] == 12345

    def test_board_status_voltage(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_BUS_UNDER_VOLTAGE"))
        msg_data.push(*Numeric("voltage", 16).encode(54321))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_BUS_UNDER_VOLTAGE"
        assert res["voltage"] == 54321

    def test_board_status_dead(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_BOARD_FEARED_DEAD"))
        msg_data.push(*Enum("board_id", 8, mt.board_id).encode("RADIO"))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_BOARD_FEARED_DEAD"
        assert res["board_id"] == "RADIO"

    def test_board_status_quiet(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_NO_CAN_TRAFFIC"))
        msg_data.push(*Numeric("err_time", 16).encode(54321))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_NO_CAN_TRAFFIC"
        assert res["err_time"] == 54321

    def test_board_status_sensor(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_SENSOR"))
        msg_data.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_BARO"))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_SENSOR"
        assert res["sensor_id"] == "SENSOR_BARO"

    def test_board_status_actuator(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Enum("status", 8, mt.board_status).encode("E_ACTUATOR_STATE"))
        msg_data.push(*Enum("req_state", 8, mt.actuator_states).encode("ACTUATOR_CLOSED"))
        msg_data.push(*Enum("cur_state", 8, mt.actuator_states).encode("ACTUATOR_UNK"))
        res = parsley.parse("GENERAL_BOARD_STATUS", msg_data)
        assert res["status"] == "E_ACTUATOR_STATE"
        assert res["req_state"] == "ACTUATOR_CLOSED"
        assert res["cur_state"] == "ACTUATOR_UNK"

    def test_sensor_temp(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("sensor_id", 8).encode(0x12))
        msg_data.push(*Numeric("temperature", 24, scale=1/2**10, signed=True).encode(12.5))
        res = parsley.parse("SENSOR_TEMP", msg_data)
        assert res["sensor_id"] == 0x12
        assert res["temperature"] == test_utils.approx(12.5)

    def test_sensor_altitude(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("altitude", 32, signed=True).encode(-12345))
        res = parsley.parse("SENSOR_ALTITUDE", msg_data)
        assert res["altitude"] == -12345

    def test_sensor_acc(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_2.encode(54.321))
        msg_data.push(*Numeric("x", 16, scale=8/2**16, signed=True).encode(-2))
        msg_data.push(*Numeric("y", 16, scale=8/2**16, signed=True).encode(-3))
        msg_data.push(*Numeric("z", 16, scale=8/2**16, signed=True).encode(-4))
        res = parsley.parse("SENSOR_ACC", msg_data)
        assert res["time"] == test_utils.approx(54.321)
        assert res["x"] == test_utils.approx(-2)
        assert res["y"] == test_utils.approx(-3)
        assert res["z"] == test_utils.approx(-4)

    def test_sensor_gyro(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp2())
        msg_data.push(*Numeric("x", 16, scale=2000/2**16, signed=True).encode(3))
        msg_data.push(*Numeric("y", 16, scale=2000/2**16, signed=True).encode(4))
        msg_data.push(*Numeric("z", 16, scale=2000/2**16, signed=True).encode(5))
        res = parsley.parse("SENSOR_GYRO", msg_data)
        assert res["x"] == test_utils.approx(3)
        assert res["y"] == test_utils.approx(4)
        assert res["z"] == test_utils.approx(5)
    
    def test_sensor_mag(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp2())
        msg_data.push(*Numeric("x", 16, signed=True).encode(-100))
        msg_data.push(*Numeric("y", 16, signed=True).encode(-200))
        msg_data.push(*Numeric("z", 16, signed=True).encode(-300))
        res = parsley.parse("SENSOR_MAG", msg_data)
        assert res["x"] == test_utils.approx(-100)
        assert res["y"] == test_utils.approx(-200)
        assert res["z"] == test_utils.approx(-300)

    def test_sensor_analog(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp2())
        msg_data.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_BARO"))
        msg_data.push(*Numeric("value", 16).encode(54321))
        res = parsley.parse("SENSOR_ANALOG", msg_data)
        assert res["sensor_id"] == "SENSOR_BARO"
        assert res["value"] == 54321

    def test_gps_timestamp(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("hrs", 8).encode(12))
        msg_data.push(*Numeric("mins", 8).encode(23))
        msg_data.push(*Numeric("secs", 8).encode(34))
        msg_data.push(*Numeric("dsecs", 8).encode(45))
        res = parsley.parse("GPS_TIMESTAMP", msg_data)
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
        res = parsley.parse("GPS_LATITUDE", msg_data)
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
        res = parsley.parse("GPS_LONGITUDE", msg_data)
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
        res = parsley.parse("GPS_ALTITUDE", msg_data)
        assert res["altitude"] == 12345
        assert res["daltitude"] == 12
        assert res["unit"] == "m"

    def test_gps_info(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("num_sats", 8).encode(12))
        msg_data.push(*Numeric("quality", 8).encode(23))
        res = parsley.parse("GPS_INFO", msg_data)
        assert res["num_sats"] == 12
        assert res["quality"] == 23

    def test_fill_lvl(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("level", 8).encode(9))
        msg_data.push(*Enum("direction", 8, mt.fill_direction).encode("FILLING"))
        res = parsley.parse("FILL_LVL", msg_data)
        assert res["level"] == 9
        assert res["direction"] == "FILLING"

    def test_radi_value(self):
        msg_data = BitString()
        msg_data.push(*self.timestamp3())
        msg_data.push(*Numeric("radi_board", 8).encode(1))
        msg_data.push(*Numeric("radi", 16).encode(500))
        res = parsley.parse("RADI_VALUE", msg_data)
        assert res["radi_board"] == 1
        assert res["radi"] == 500

    def test_leds_on(self):
        # LED_ON message has no message body
        pass

    def test_leds_off(self):
        # LED_OFF message has no message body
        pass
