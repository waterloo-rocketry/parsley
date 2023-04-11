import parsley

from bitstring import BitString
from fields import ASCII, Enum, Numeric
from message_definitions import MESSAGE_TYPE, BOARD_ID, MSG_SID, TIMESTAMP_3

import message_types as mt
import test_utils as tu

class TestParsley:
    def test_parse(self):
        msg_sid = tu.create_msg_sid_from_strings("GENERAL_BOARD_STATUS", "RLCS")
        """
                     |----| => ___1 0100 = 0x14 = RLCS
        ____ _101 0011 0100
              |-----| => _101 0010 = 0x52 = GENERAL_BARD_STATUS
        """
        assert msg_sid == b'\x05\x34'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_3.encode(0.005)) # 0x005
        bit_str.push(*Enum("status", 8, mt.board_status).encode("E_SENSOR")) # 0x11
        bit_str.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_PRESSURE_PNEUMATICS")) # 0x07
        msg_data = bit_str.pop(40)
        assert msg_data == b'\x00\x00\x05\x11\x07'

        res = parsley.parse(msg_sid, msg_data)
        expected_res = {
            "board_id": "RLCS",
            "msg_type": "GENERAL_BOARD_STATUS",
            "data": {
                "time": 0.005,
                "status": "E_SENSOR",
                "sensor_id": "SENSOR_PRESSURE_PNEUMATICS"
            }
        }
        assert res == expected_res

    def test_parse_partial_byte_fields(self):
        msg_sid = tu.create_msg_sid_from_strings("DEBUG_MSG", "GPS")
        """
                     |----| => ___0 1011 = 0x0B = GPS
        ____ _001 1000 1011
              |-----| => _001 1000 = 0x18 = DEBUG_MSG
        """
        assert msg_sid == b'\x01\x8B'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_3.encode(0.133)) # 0x85
        bit_str.push(*Numeric("level", 4).encode(15)) # 0xF
        bit_str.push(*Numeric("line", 12).encode(3873)) # 0xF21
        bit_str.push(*ASCII("data", 24, optional=True).encode("zZz"))
        msg_data = bit_str.pop(64)
        assert msg_data == b'\x00\x00\x85\xFF\x21zZz'

        res = parsley.parse(msg_sid, msg_data)
        expected_res = {
            "board_id": "GPS",
            "msg_type": "DEBUG_MSG",
            "data": {
                "time": 0.133,
                "level": 15,
                "line": 3873,
                "data": "zZz"
            }
        }
        assert res == expected_res

    def test_parse_bad_msg_type(self):
        msg_sid = b'\x00\x00'
        msg_data = b'\xAB\xCD\xEF\x00'
        res = parsley.parse(msg_sid, msg_data)
        assert "error" in res['data']

    # until we eventually use up all the board ids, continue testing this functionality
    def test_parse_bad_board_id(self):
        # we need to manually build this message since BOARD_ID.encode() will throw an error for b'\x1F'
        bit_msg_sid = BitString()
        bit_msg_sid.push(*MESSAGE_TYPE.encode("LEDS_ON"))
        bit_msg_sid.push(b'\x1F', BOARD_ID.length)
        msg_sid = bit_msg_sid.pop(MSG_SID.length)

        res = parsley.parse(msg_sid, b'')
        assert "0x" in res['board_id'] # when board_id throws, just display the hexadecimal string

    def test_parse_bad_msg_data(self):
        msg_sid = tu.create_msg_sid_from_strings("ALT_ARM_STATUS", "USB")
        """
                     |----| => ___1 0011 = 0x13 = USB
        ____ _100 0101 0011
              |-----| => _100 0100 = 0x44 = ALT_ARM_STATUS
        """
        assert msg_sid == b'\x04\x53'

        msg_data = b'\x98\x76\x54\x32\x1F'
        res = parsley.parse(msg_sid, msg_data)
        assert "error" in res['data']
