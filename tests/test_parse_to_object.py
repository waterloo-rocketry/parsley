import pytest

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric
from parsley.message_definitions import MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID, MESSAGE_PRIO, TIMESTAMP_2, CAN_MESSAGE

import parsley.message_types as mt
import utils as utilities
import parsley
import crc8 #cyclic redundancy check
import struct

PARSE_LOGGER_PAGE_SIZE = 4096 

from parsley.parse_to_object import _ParsleyParseInternal, ParsleyParser, USBDebugParser, LiveTelemetryParser, LoggerParser, BitstringParser
from parsley.parsley_message import ParsleyError, ParsleyObject

class TestParseToObject:
    def _to_dict(self, result):
        if isinstance(result, ParsleyError):
            return {'data': {'error': result.error, 'msg_data': result.msg_data}, 'msg_type': result.msg_type}
        
        return result.model_dump() # ParsleyObject -> dict

    def test_internal_class_cannot_be_instantiated(self):
        with pytest.raises(NotImplementedError) as e:
            _ParsleyParseInternal()
        assert "static only" in str(e.value)

    def test_parse(self):
        msg_sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'PRIMARY')

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(1.234))
        general_status_value = (1 << mt.general_board_status_offset['E_5V_OVER_VOLTAGE'])
        bit_str.push(*Numeric('general_board_status', 32).encode(general_status_value))
        board_error_value = (1 << mt.board_specific_status_offset['E_5V_EFUSE_FAULT'])
        bit_str.push(*Numeric('board_error_bitfield', 16).encode(board_error_value))

        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

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
        msg_sid = utilities.create_msg_sid_from_strings('LOW', 'DEBUG_RAW', '0', 'GPS', 'PAYLOAD')

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(0.133))
        bit_str.push(*ASCII('string', 48).encode('zZz'))
        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

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
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'SENSOR_ANALOG', '0', 'PAY_SENSOR', 'ANY')

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(12.345)) 
        bit_str.push(*Enum('sensor_id', 8, mt.analog_sensor_id).encode('SENSOR_RA_BATT_VOLT_1'))
        bit_str.push(*Numeric('value', 16).encode(3300)) 
        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

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
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error

    def test_parse_empty(self):
        msg_sid = b''
        msg_data = b''
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error

    def test_parse_messed_up_SID(self):
        msg_sid = b'\xFF\xFF\xFF\xFF'  # Invalid SID
        msg_data = b'\x00\x00\x00\x00'  # Dummy data
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error

    def test_parse_bad_board_type_id(self):
        # manually build message since using BOARD_TYPE_ID from message_definitions will throw an error for b'\x1F' as it is invalid
        bit_msg_sid = BitString()
        bit_msg_sid.push(*MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x00', 2)
        
        bit_msg_sid.push(b'\x1F', BOARD_TYPE_ID.length)  # invalid board_type
        bit_msg_sid.push(b'\x00', BOARD_INST_ID.length)  # dummy board instance
        msg_sid = bit_msg_sid.pop(MESSAGE_SID.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, b'')
        assert isinstance(result, ParsleyObject)
        assert str(result.board_type_id) == "0x1F"
        assert str(result.board_inst_id) == "ANY"
        assert result.msg_prio == "LOW"
        assert result.msg_type == "LEDS_ON"

    def test_parse_bad_msg_data(self):
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'ALT_ARM_STATUS', '0', 'ALTIMETER', 'PRIMARY')

        msg_data = b'\x00\x00\x01\x10\x04'  # missing main_v

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error

    def test_bad_board_instance(self):
        bit_msg_sid = BitString()
        bit_msg_sid.push(*MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x00', 2)
        bit_msg_sid.push(*BOARD_TYPE_ID.encode('GPS'))  # valid board type
        bit_msg_sid.push(b'\x1F', BOARD_INST_ID.length)  # invalid board instance
        msg_sid = bit_msg_sid.pop(MESSAGE_SID.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, b'')
        assert isinstance(result, ParsleyObject)
        assert str(result.board_type_id) == "GPS"
        assert str(result.board_inst_id) == "0x1F"
        assert str(result.msg_prio) == "LOW"
        assert str(result.msg_type) == "LEDS_ON"

    def test_parse_bitstring(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 32)  # 32 bits of data
        bit_str.push(b'\x9A\xBC', 16)          # 16 bits of data
        result = BitstringParser().parse(bit_str)
        res = self._to_dict(result)
        # First 29 bits of 0x123456789ABC = 0x02468ACF
        # Remaining 19 bits = 0x9ABC -> message data should be 0x009abc when hexified
        assert res['msg_type'].startswith('0x')
        # convert to int for comparison to avoid issues with leading zeros in hex strings
        assert int(res['data']['msg_data'], 16) == int(b'\x00\x9a\xbc'.hex(), 16)
        
    def test_parse_bitstring_empty(self):
        bit_str = BitString() #just an empty bitstring
        with pytest.raises(IndexError) as e:
            BitstringParser().parse(bit_str)
        # message content is not asserted as an index error is expected
        
    def test_parse_bitstring_small(self):
        bit_str = BitString()
        bit_str.push(b'\xFF', 8) # only 8 bits, less than required 29 bits for SID
        with pytest.raises(IndexError) as e:
            BitstringParser().parse(bit_str)
        # message content is not asserted as an index error is expected
        
    def test_parse_bitstring_minimal(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 29)  # Exactly 29 bits for SID
        copy = BitString() #need a copy so that parse_bitstring can consume the copy
        copy.push(b'\x12\x34\x56\x78', 29)
        
        result = BitstringParser().parse(copy)
        res = self._to_dict(result)

        # object with empty data.
        assert isinstance(res['data'], dict)
        assert res['data']['msg_data'] == '0x0'
        
        
    def test_calculate_msg_bit_length(self):
        msg = CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')
        bit_len = _ParsleyParseInternal.calculate_msg_bit_len(msg)
        # GENERAL_BOARD_STATUS fields: msg_prio (2) + board_type_id (8) + board_inst_id (8) + time (16) + general_board_status (32) + board_error_bitfield (16) = 82 bits
        assert bit_len == 82
        
    def test_format_line(self):
        parsed_data = {
            'msg_prio': 'HIGH',
            'msg_type': 'GENERAL_BOARD_STATUS',
            'board_type_id': 'RLCS_RELAY',
            'board_inst_id': 'PRIMARY',
            'data': {
                'time': 1.234,
                'general_board_status': 'E_5V_OVER_VOLTAGE',
                'board_error_bitfield': 'E_5V_EFUSE_FAULT'
            }
        }
        line = _ParsleyParseInternal.format_line(parsed_data)
        # format_line uses padding so gotta put padding here too
        expected_line = '[ HIGH    GENERAL_BOARD_STATUS RLCS_RELAY   PRIMARY  ] time: 1.234 general_board_status: E_5V_OVER_VOLTAGE board_error_bitfield: E_5V_EFUSE_FAULT'
        assert line == expected_line
        
    def test_encode_data(self):
        parsed_data = {
            'msg_prio': 'MEDIUM',
            'msg_type': 'ALT_ARM_STATUS',
            'board_type_id': 'ALTIMETER',
            'board_inst_id': 'PAYLOAD',
            'time': 5.678,
            'alt_id': 'ALTIMETER_PAYLOAD_RAVEN',
            'alt_arm_state': 'ALT_ARM_STATE_ARMED',
            'drogue_v': 4095,
            'main_v': 2048
        }
        msg_sid, msg_data = _ParsleyParseInternal.encode_data(parsed_data)
        
        # MEDIUM = 0x2, ALT_ARM_STATUS = 0x00A, ALTIMETER = 0x0A, PAYLOAD = 0x03
        assert msg_sid == int.from_bytes(b'\x10\x28\x0a\x03', byteorder='big')
        
        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(5.678))
        bit_str.push(*Enum('alt_id', 8, mt.altimeter_id).encode('ALTIMETER_PAYLOAD_RAVEN'))
        bit_str.push(*Enum('alt_arm_state', 8, mt.alt_arm_state).encode('ALT_ARM_STATE_ARMED'))
        bit_str.push(*Numeric('drogue_v', 16).encode(4095))
        bit_str.push(*Numeric('main_v', 16).encode(2048))
        
        expected_msg_data = bytes(bit_str.pop(bit_str.length))
        assert msg_data == list(expected_msg_data)
    
    def test_parse_usb_debug(self):
        line = "$1234ABCD:12,34,56,78\r\n\0"
        #you get \x12\x34\xAB\xCD as SID and \x12\x34\x56\x78 as data (first part vs second part)
        result = USBDebugParser().parse(line)
        res = self._to_dict(result)
        # msg_data should be hexified in the parsed result
        assert int(res['data']['msg_data'], 16) == int(b'\x12\x34\x56\x78'.hex(), 16)
        
    def test_parse_usb_data_empty(self):
        line = "$ABCD1234"
        result = USBDebugParser().parse(line)
        res = self._to_dict(result)
       
        assert isinstance(res['data'], dict)
        assert(res['data'].get('msg_data') == '0x0')
        
    def test_parse_usb_debug_invalid_format(self): # need a $ at start 
        line = "1234:AA,BB"
        with pytest.raises(ValueError) as e:
            USBDebugParser().parse(line)
        assert "Incorrect line format" in str(e.value)
            
    def test_parse_usb_debug_empty_line(self):
        line = ""
        with pytest.raises(ValueError) as e:
            USBDebugParser().parse(line)
        assert "Incorrect line format" in str(e.value)
        
    def test_parse_logger(self):
        buf = bytearray(PARSE_LOGGER_PAGE_SIZE)
        
        log_header = b"LOG" # correct LOG_MAGIC bytes
        sequence_number = 0x64 #page number of data | 100 in decimal

        buf[0:3] = log_header
        buf[3] = sequence_number

        header_length = len(log_header) + 1  # 4 bytes: 3 for "LOG" + 1 for sequence number
        offset = header_length
        
        messages = [
            (0x111, 0x222, [0x01, 0x02]),
            (0x333, 0x444, [0x03, 0x04, 0x05]),
            (0x555, 0x666, [0x06])
        ]
        
        CAN_MSG_HEADER_SIZE = 9  # 4 bytes SID + 4 bytes timestamp + 1 byte DLC
        for sid, timestamp, data in messages:
            data_length_code = len(data) # number of data bytes
            struct.pack_into("<IIB", buf, offset, sid, timestamp, data_length_code)
            offset += CAN_MSG_HEADER_SIZE
            buf[offset:offset+data_length_code] = data
            offset += data_length_code

        # Fill unused bytes after last message with 0xff
        buf[offset:] = b"\xff" * (len(buf) - offset)
        
        results = list(LoggerParser().parse(bytes(buf), 0x64))
        assert len(results) == 3

        r0 = self._to_dict(results[0])
        r1 = self._to_dict(results[1])
        r2 = self._to_dict(results[2])

        assert r0['msg_type'].startswith('0x')
        assert int(r0['data']['msg_data'], 16) == int(b'\x01\x02'.hex(), 16)
        
        assert r1['msg_type'].startswith('0x')
        assert int(r1['data']['msg_data'], 16) == int(b'\x03\x04\x05'.hex(), 16)
        
        assert r2['msg_type'].startswith('0x')
        assert int(r2['data']['msg_data'], 16) == int(b'\x06'.hex(), 16)
        
        
    def test_parse_logger_wrong_size(self):
        buf = b"LOG" + b"\x00" * (PARSE_LOGGER_PAGE_SIZE - 4)  # only 4095 bytes (3 for 'LOG', 1 for sequence)

        assert len(buf) < PARSE_LOGGER_PAGE_SIZE

        with pytest.raises(ValueError) as e:
            list(LoggerParser().parse(buf, 0))
        assert "exactly 4096 bytes" in str(e.value)
            
    def test_parse_logger_wrong_signature(self): # wrong LOG_MAGIC bytes
        buf = b"BAD" + b"\x00" * 4093
        with pytest.raises(ValueError) as e:
            list(LoggerParser().parse(buf, 0))
        assert "Missing 'LOG' signature" in str(e.value)
            
    def test_parse_logger_wrong_page_number(self):
        buf = b"LOG\x05" + b"\x00" * 4092  # Page 5 in buffer
        with pytest.raises(ValueError) as e:
            list(LoggerParser().parse(buf, 10))  # Expect page 10
        assert "Page number mismatch" in str(e.value)

    def test_parse_logger_empty(self):
        buf = bytearray(PARSE_LOGGER_PAGE_SIZE)
        buf[0:3] = b"LOG"
        buf[3] = 0
        
        buf[4:] = b"\xff" * (len(buf) - 4) # Fill unused bytes with 0xff

        results = list(LoggerParser().parse(bytes(buf), 0))
        assert len(results) == 0
    
    def test_parse_live_telemetry_basic(self):
        frame = bytearray()
        frame.append(0x02) #header must be 0x02
        frame.append(10) #frame length
        
        sid = 0x12345678
        frame.append((sid >> 24) & 0x1F) #first 5 bits of SID
        frame.append((sid >> 16) & 0xFF) #next 8 bits of SID
        frame.append((sid >> 8) & 0xFF) #next 8 bits of SID
        frame.append(sid & 0xFF) #last 8 bits of SID

        frame.extend([0xAA, 0xBB, 0xCC]) #payload data
    
        frame[1] = len(frame) + 1  #makes length +1 cause cyclic redundancy check byte
        
        crc = crc8.crc8(frame).digest()[0]
        frame.append(crc) #actually adds the crc byte

        result = LiveTelemetryParser().parse(bytes(frame))
        res = self._to_dict(result)
        expected_val = int.from_bytes(b'\xaa\xbb\xcc', 'big')
        assert res['msg_type'].startswith('0x')
        assert int(res['data']['msg_data'], 16) == expected_val
        
    def test_parse_live_telemetry_too_short(self):
        frame = b'\x02\x06\x12\x34'  #4 bytes, need at least 7
        with pytest.raises(ValueError) as e:
            LiveTelemetryParser().parse(frame)
        assert "Incorrect frame length" in str(e.value)
            
    def test_parse_live_telemetry_wrong_header(self):
        frame = b'\x03\x08\x12\x34\x56\x78\xAA\x00'  #header = 0x03 instead of 0x02
        with pytest.raises(ValueError) as e:
            LiveTelemetryParser().parse(frame)
        assert "Incorrect frame header" in str(e.value)
            
    def test_parse_live_telemetry_bad_crc(self):
        
        frame = bytearray([0x02, 0x08, 0x12, 0x34, 0x56, 0x78, 0xAA, 0xFF])  # wrong CRC
        
        with pytest.raises(ValueError) as e:
            LiveTelemetryParser().parse(bytes(frame))
        assert "Bad checksum" in str(e.value)