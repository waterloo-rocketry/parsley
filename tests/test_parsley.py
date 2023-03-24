from bitstring import BitString
from fields import ASCII, Enum, Numeric
from parsley_definitions import *

import message_types as mt
import parsley
import test_utils

class TestParse:
    def test_parse(self):
        (msg_type_bits, _) = MESSAGE_TYPE.encode("GENERAL_BOARD_STATUS")
        (board_id_bits, _) = BOARD_ID.encode("PAPA_SPARE")
        msg_sid = test_utils.create_msg_sid_from_bytes(msg_type_bits, board_id_bits)
        """
                        |----| => 0001 0100 = 0x14 = PAPA_SPARE
           ____ _101 0011 0100
                 |-----| => 0101 0010 = 0x52 = GENERAL_BARD_STATUS
        """
        assert msg_sid == b'\x05\x34'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_3.encode(0.005)) # 0x005
        bit_str.push(*Enum("status", 8, mt.board_status).encode("E_SENSOR")) # 0x0F
        bit_str.push(*Enum("sensor_id", 8, mt.sensor_id).encode("SENSOR_PRESSURE_PNEUMATICS")) # 0x0F
        msg_data = bit_str.pop(40)
        assert msg_data == b'\x00\x00\x05\x0F\x0F'

        res = parsley.parse(msg_sid, msg_data)
        expected_res = {
            "msg_type": "GENERAL_BOARD_STATUS",
            "board_id": "PAPA_SPARE",
            "time": 0.005,
            "status": "E_SENSOR",
            "sensor_id": "SENSOR_PRESSURE_PNEUMATICS"
        }
        assert res == expected_res

    def test_parse_partial_byte(self):
        (msg_type_bits, _) = MESSAGE_TYPE.encode("DEBUG_MSG")
        (board_id_bits, _) = BOARD_ID.encode("ROCKET_PI")
        msg_sid = test_utils.create_msg_sid_from_bytes(msg_type_bits, board_id_bits)
        """
                        |----| => 0001 0101 = 0x15 = ROCKET_PI
           ____ _001 1001 0101
                 |-----| => 0001 1000 = 0x18 = DEBUG_MSG
        """
        assert msg_sid == b'\x01\x95'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_3.encode(0.133)) # 0x85
        bit_str.push(*Numeric("level", 4).encode(15)) # 0xF
        bit_str.push(*Numeric("line", 12).encode(3873)) # 0xF21
        bit_str.push(*ASCII("data", 24, optional=True).encode("zZz"))
        msg_data = bit_str.pop(64)
        assert msg_data == b'\x00\x00\x85\xFF\x21zZz'

        res = parsley.parse(msg_sid, msg_data)
        expected_res = {
            "msg_type": "DEBUG_MSG",
            "board_id": "ROCKET_PI",
            "time": 0.133,
            "level": 15,
            "line": 3873,
            "data": "zZz"
        }
        assert res == expected_res
