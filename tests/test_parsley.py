import parsley

from bitstring import BitString
from fields import ASCII, Enum, Numeric
from parsley_definitions import MESSAGE_TYPE, TIMESTAMP_3

import message_types as mt
import test_utils as tu

class TestParsley:
    def test_parse(self):
        msg_sid = tu.create_msg_sid_from_strings("GENERAL_BOARD_STATUS", "PAPA_SPARE")
        """
                     |----| => ___1 0100 = 0x14 = PAPA_SPARE
        ____ _101 0011 0100
              |-----| => _101 0010 = 0x52 = GENERAL_BARD_STATUS
        """
        assert msg_sid == b'\x05\x34'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_3.encode(0.005)) # 0x005
        bit_str.push(*Enum("status", 8, mt.board_status).encode("E_SENSOR")) # 0x0F
        bit_str.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_PRESSURE_PNEUMATICS")) # 0x0F
        msg_data = bit_str.pop(40)
        assert msg_data == b'\x00\x00\x05\x0F\x0F'

        res = parsley.parse_raw(msg_sid, msg_data)
        expected_res = {
            "msg_type": "GENERAL_BOARD_STATUS",
            "board_id": "PAPA_SPARE",
            "time": 0.005,
            "status": "E_SENSOR",
            "sensor_id": "SENSOR_PRESSURE_PNEUMATICS"
        }
        assert res == expected_res

    def test_parse_partial_byte_fields(self):
        msg_sid = tu.create_msg_sid_from_strings("DEBUG_MSG", "ROCKET_PI")
        """
                     |----| => ___1 0101 = 0x15 = ROCKET_PI
        ____ _001 1001 0101
              |-----| => _001 1000 = 0x18 = DEBUG_MSG
        """
        assert msg_sid == b'\x01\x95'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_3.encode(0.133)) # 0x85
        bit_str.push(*Numeric("level", 4).encode(15)) # 0xF
        bit_str.push(*Numeric("line", 12).encode(3873)) # 0xF21
        bit_str.push(*ASCII("data", 24, optional=True).encode("zZz"))
        msg_data = bit_str.pop(64)
        assert msg_data == b'\x00\x00\x85\xFF\x21zZz'

        res = parsley.parse_raw(msg_sid, msg_data)
        expected_res = {
            "msg_type": "DEBUG_MSG",
            "board_id": "ROCKET_PI",
            "time": 0.133,
            "level": 15,
            "line": 3873,
            "data": "zZz"
        }
        assert res == expected_res

    def test_parse_bad_msg_type(self):
        msg_sid = b'\x00\x00'
        msg_data = b'\xAB\xCD\xEF\x00'
        res = parsley.parse_raw(msg_sid, msg_data)
        assert "error" in res

    # there will soon be no-bad-boards but for now, we're suppose to continue parsing.
    # When the day arrives and this UT fails, please modify parsley's parse_raw so that
    # BOARD_ID.decode is contianed in the same try except as MESSAGE_TYPE.decode
    def test_parse_bad_board_id(self):
        (msg_type_bits, _) = MESSAGE_TYPE.encode("LEDS_ON")
        board_id = b'\x1F'
        # need to manually build this message since BOARD_ID.encode() will currently throw an error for b'\x1F'
        msg_type_int = int.from_bytes(msg_type_bits, byteorder='big', signed=False)
        board_id_int = int.from_bytes(board_id, byteorder='big', signed=False)
        msg_sid_int = msg_type_int | board_id_int
        msg_sid = msg_sid_int.to_bytes(2, byteorder='big')

        res = parsley.parse_raw(msg_sid, b'')
        assert "unknown" in res['board_id']

    def test_parse_bad_msg_data(self):
        msg_sid = tu.create_msg_sid_from_strings("ALT_ARM_STATUS", "USB")
        """
                     |----| => ___0 0101 = 0x09 = USB
        ____ _100 0100 1001
              |-----| => _100 0100 = 0x44 = ALT_ARM_STATUS
        """
        assert msg_sid == b'\x04\x49'

        msg_data = b'\x98\x76\x54\x32\x10'
        res = parsley.parse_raw(msg_sid, msg_data)
        assert "error" in res
