import parsley

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric
from parsley.message_definitions import MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID, MESSAGE_PRIO
from parsley.parsley import format_can_message

import parsley.message_types as mt
import utils as utilities

class TestParsley:
    def test_parse(self):
        parsed_data = {
            'msg_type': 'GENERAL_BOARD_STATUS',
            'msg_prio': 'HIGH',
            'board_type_id': 'RLCS_RELAY',
            'board_inst_id': 'PRIMARY',
            'time': 1.234,
            'general_board_status': (1 << mt.general_board_status_offset['E_5V_OVER_VOLTAGE']).to_bytes(4, byteorder='big'),
            'board_error_bitfield': (1 << mt.board_specific_status_offset['E_5V_EFUSE_FAULT']).to_bytes(2, byteorder='big')
        }

        msg_sid, msg_data = format_can_message(*parsley.encode_data(parsed_data)) # turns parsed_data into (msg_sid, msg_data) to avoid hardcoding bits in tests

        helper_sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'PRIMARY')
        assert msg_sid == helper_sid

        res = parsley.parse(msg_sid, msg_data)

        expected_res = {
            'msg_type': 'GENERAL_BOARD_STATUS',
            'board_type_id': 'RLCS_RELAY',
            'board_inst_id': 'PRIMARY',
            'msg_prio': 'HIGH',
            'data': {
                'time': utilities.approx(1.234),
                'general_board_status': 'E_5V_OVER_VOLTAGE',
                'board_error_bitfield': 'E_5V_EFUSE_FAULT'
            }
        }

        assert res == expected_res
        
    def test_parse_partial_byte_fields(self):
        parsed_data = {
            'msg_type': 'DEBUG_RAW',
            'msg_prio': 'LOW',
            'board_type_id': 'GPS',
            'board_inst_id': 'PAYLOAD',
            'time': 0.133,
            'string': 'zZz'
        }

        msg_sid, msg_data = format_can_message(*parsley.encode_data(parsed_data))

        helper_sid = utilities.create_msg_sid_from_strings('LOW', 'DEBUG_RAW', '0', 'GPS', 'PAYLOAD')
        assert msg_sid == helper_sid

        res = parsley.parse(msg_sid, msg_data)

        expected_res = {
            'msg_type': 'DEBUG_RAW',
            'board_type_id': 'GPS',
            'board_inst_id': 'PAYLOAD',
            'msg_prio': 'LOW',
            'data': {
                'time': utilities.approx(0.133),
                'string': 'zZz'
            }
        }

        assert res == expected_res
        
    def test_parse_sensor_analog(self):
        parsed_data = {
            'msg_type': 'SENSOR_ANALOG',
            'msg_prio': 'MEDIUM',
            'board_type_id': 'PAY_SENSOR',
            'board_inst_id': 'ANY',
            'time': 12.345,
            'sensor_id': 'SENSOR_RA_BATT_VOLT_1',
            'value': 3300
        }

        msg_sid, msg_data = format_can_message(*parsley.encode_data(parsed_data))

        helper_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'SENSOR_ANALOG', '0', 'PAY_SENSOR', 'ANY')
        assert msg_sid == helper_sid

        res = parsley.parse(msg_sid, msg_data)

        expected_res = {
            'msg_type': 'SENSOR_ANALOG',
            'board_type_id': 'PAY_SENSOR',
            'board_inst_id': 'ANY',
            'msg_prio': 'MEDIUM',
            'data': {
                'time': utilities.approx(12.345),
                'sensor_id': 'SENSOR_RA_BATT_VOLT_1',
                'value': 3300
            }
        }

        assert res == expected_res
        
    def test_parse_bad_msg_type(self):
        msg_sid = b'\x00\x00'
        msg_data = b'\xAB\xCD\xEF\x00'
        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data']
        
    def test_parse_bad_board_id(self):
        # we need to manually build this message since BOARD_ID.encode() will throw an error for b'\x1F'
        bit_msg_sid = BitString()
        bit_msg_sid.push(*MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x00', 2)  # reserved bits (always zero)
        
        # push the invalid board_type byte separately so BOARD_TYPE_ID.decode() will raise
        bit_msg_sid.push(b'\x1F', BOARD_TYPE_ID.length)  # invalid board_type
        bit_msg_sid.push(b'\x00', BOARD_INST_ID.length)  # dummy board instance
        msg_sid = bit_msg_sid.pop(MESSAGE_SID.length)

        res = parsley.parse(msg_sid, b'')
        assert '0x' in res['board_type_id'] # when board_id throws, just display the hexadecimal string
    
    def test_parse_bad_msg_data(self):
        # Build a valid SID for ALT_ARM_STATUS but give malformed (incomplete) msg_data
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'ALT_ARM_STATUS', '0', 'ALTIMETER', 'PRIMARY')

        # ALT_ARM_STATUS normally expects timestamp + alt_id + alt_arm_state + drogue_v + main_v
        # Provide a short payload (missing main_v) to trigger parse error handling
        msg_data = b'\x00\x00\x01\x10\x04'  # intentionally incomplete

        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data']

#ADD MORE CASES TO GET STUFF UP BABY!!!
#python3 -m pytest --cov=parsley tests/test_parsley.py --cov-report=term-missing --cov-report=html