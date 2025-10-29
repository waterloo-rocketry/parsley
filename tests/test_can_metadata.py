import pytest
import parsley

from parsley.bitstring import BitString
from parsley.fields import Enum, Numeric
from parsley.message_definitions import TIMESTAMP_2, CAN_MESSAGE

import parsley.message_types as mt
import utils as tu

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
        TIMESTAMP_2.encode(30.2312)
            
    def test_timestamp2_message(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_2.encode(1.234))
        msg_data.push(*Enum('imu_id', 8, mt.imu_id).encode('IMU_PROC_LSM6DSO32'))
        msg_data.push(*Numeric('linear_accel', 16).encode(1234))
        msg_data.push(*Numeric('angular_velocity', 16).encode(5678))

        res = parsley.parse_fields(msg_data, CAN_MESSAGE.get_fields('SENSOR_IMU_Y')[3:]) # skip first 3 fields (MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID)
        assert res['time'] == tu.approx(1.234)
        assert res['imu_id'] == 'IMU_PROC_LSM6DSO32'
        assert res['linear_accel'] == 1234
        assert res['angular_velocity'] == 5678
        
    def test_timestamp2_second(self):
        msg_data = BitString()
        msg_data.push(*TIMESTAMP_2.encode(1.234))
        msg_data.push(*Enum('actuator', 8, mt.actuator_id).encode('ACTUATOR_5V_RAIL_PAYLOAD'))
        msg_data.push(*Enum('cmd_state', 8, mt.actuator_state).encode('ACT_STATE_ON'))

        res = parsley.parse_fields(msg_data, CAN_MESSAGE.get_fields('ACTUATOR_CMD')[3:]) # skip first 3 fields (MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID)
        assert res['time'] == tu.approx(1.234)
        assert res['actuator'] == 'ACTUATOR_5V_RAIL_PAYLOAD'
        assert res['cmd_state'] == 'ACT_STATE_ON'
       