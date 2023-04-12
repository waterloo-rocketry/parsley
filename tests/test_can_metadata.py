import pytest
import parsley

from bitstring import BitString
from fields import Enum, Numeric
from message_definitions import TIMESTAMP_2, TIMESTAMP_3, CAN_MSG

import message_types as mt
import test_utils as tu

class TestCANMetadata:
    # our TIMESTAMP_2 can store ~65.5 seconds
    def test_timestamp2(self):
        TIMESTAMP_2.encode(0)
        TIMESTAMP_2.encode(65)
        TIMESTAMP_2.encode(65.535)
        with pytest.raises(ValueError):
            TIMESTAMP_2.encode(-1)
        with pytest.raises(ValueError):
            TIMESTAMP_2.encode(65.536)
        with pytest.raises(ValueError):
            TIMESTAMP_2.encode(66)

    # our TIMESTAMP_3 can store ~4.66 hours
    def test_timestamp3(self):
        TIMESTAMP_3.encode(0)
        TIMESTAMP_3.encode(16777)
        TIMESTAMP_3.encode(16777.215)
        with pytest.raises(ValueError):
            TIMESTAMP_3.encode(-1)
        with pytest.raises(ValueError):
            TIMESTAMP_3.encode(16777.216)
        with pytest.raises(ValueError):
            TIMESTAMP_3.encode(16778)

    def test_timestamp2_message(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_2.encode(1.234))
        msg_data.push(*Numeric('x', 16, scale=8/2**16, signed=True).encode(-2))
        msg_data.push(*Numeric('y', 16, scale=8/2**16, signed=True).encode(-3))
        msg_data.push(*Numeric('z', 16, scale=8/2**16, signed=True).encode(-4))
        res = parsley.parse_fields(msg_data, CAN_MSG.get_fields('SENSOR_ACC')[1:])
        assert res['time'] == tu.approx(1.234)
        assert res['x'] == tu.approx(-2)
        assert res['y'] == tu.approx(-3)
        assert res['z'] == tu.approx(-4)

    def test_timestamp3_message(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_3.encode(12.345))
        msg_data.push(*Enum('command', 8, mt.gen_cmd).encode('BUS_DOWN_WARNING'))
        res = parsley.parse_fields(msg_data, CAN_MSG.get_fields('GENERAL_CMD')[1:])
        assert res['time'] == tu.approx(12.345)
        assert res['command'] == 'BUS_DOWN_WARNING'
