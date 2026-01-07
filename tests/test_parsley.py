import parsley
import pytest

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric
from parsley.message_definitions import MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID, MESSAGE_PRIO, TIMESTAMP_2, CAN_MESSAGE

import parsley.message_types as mt
import utils as utilities
import crc8 #cyclic redundancy check
import struct

PARSE_LOGGER_PAGE_SIZE = 4096 

class TestParsley:
    def test_parse(self):
        msg_sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'PRIMARY')
        
        """
        HIGH = 0x1, GENERAL_BOARD_STATUS = 0x001, RLCS_RELAY = 0x81, PRIMARY = 0x04
        """
        assert msg_sid == b'\x08\x04\x81\x04'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(1.234))
        general_status_value = (1 << mt.general_board_status_offset['E_5V_OVER_VOLTAGE'])
        bit_str.push(*Numeric('general_board_status', 32).encode(general_status_value))
        board_error_value = (1 << mt.board_specific_status_offset['E_5V_EFUSE_FAULT'])
        bit_str.push(*Numeric('board_error_bitfield', 16).encode(board_error_value))

        msg_data = bit_str.pop(bit_str.length)

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
        msg_sid = utilities.create_msg_sid_from_strings('LOW', 'DEBUG_RAW', '0', 'GPS', 'PAYLOAD')
        
        """
        LOW = 0x3, DEBUG_RAW = 0x003, GPS = 0x08, PAYLOAD = 0x03
        """
        assert msg_sid == b'\x18\x0c\x08\x03'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(0.133))
        bit_str.push(*ASCII('string', 48).encode('zZz'))
        msg_data = bit_str.pop(bit_str.length)

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
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'SENSOR_ANALOG', '0', 'PAY_SENSOR', 'ANY')
        
        """
        MEDIUM = 0x2, SENSOR_ANALOG = 0x013, PAY_SENSOR = 0x40, ANY = 0x00
        """
        assert msg_sid == b'\x10\x4c\x40\x00'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(12.345)) 
        bit_str.push(*Enum('sensor_id', 8, mt.analog_sensor_id).encode('SENSOR_RA_BATT_VOLT_1'))  # 8-bit sensor ID
        bit_str.push(*Numeric('value', 16).encode(3300)) 
        msg_data = bit_str.pop(bit_str.length)

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
    
    def test_parse_empty(self):
        msg_sid = b''
        msg_data = b''
        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data'] 
        
    def test_parse_messed_up_SID(self):
        msg_sid = b'\xFF\xFF\xFF\xFF'  # Invalid SID
        msg_data = b'\x00\x00\x00\x00'  # Dummy data
        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data']
        
    def test_parse_bad_board_type_id(self):
        # manually build message since using BOARD_TYPE_ID from message_definitions will throw an error for b'\x1F' as it is invalid
        bit_msg_sid = BitString()
        bit_msg_sid.push(*MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x00', 2)
        
        bit_msg_sid.push(b'\x1F', BOARD_TYPE_ID.length)  # invalid board_type
        bit_msg_sid.push(b'\x00', BOARD_INST_ID.length)  # dummy board instance
        msg_sid = bit_msg_sid.pop(MESSAGE_SID.length)

        res = parsley.parse(msg_sid, b'')
        assert '0x' in res['board_type_id']

    def test_parse_bad_msg_data(self):
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'ALT_ARM_STATUS', '0', 'ALTIMETER', 'PRIMARY')

        # Expects: timestamp + alt_id + alt_arm_state + drogue_v + main_v
        msg_data = b'\x00\x00\x01\x10\x04'  # missing main_v

        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data']
        
    def test_bad_board_instance(self):
        # manually build message since BOARD_INST_ID.encode() will throw an error for b'\x1F'
        bit_msg_sid = BitString()
        bit_msg_sid.push(*MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x00', 2)
        bit_msg_sid.push(*BOARD_TYPE_ID.encode('GPS'))  # valid board type
        bit_msg_sid.push(b'\x1F', BOARD_INST_ID.length)  # invalid board instance
        msg_sid = bit_msg_sid.pop(MESSAGE_SID.length)

        res = parsley.parse(msg_sid, b'')
        assert '0x' in res['board_inst_id']
        
    def test_parse_bitstring(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 32)  # 32 bits of data
        bit_str.push(b'\x9A\xBC', 16)          # 16 bits of data
        msg_sid, msg_data = parsley.parse_bitstring(bit_str)
        
        # First 29 bits of 0x123456789ABC = 0x02468ACF
        # Remaining 19 bits = 0x9ABC
        assert msg_sid == b'\x02\x46\x8a\xcf'
        assert msg_data == b'\x00\x9a\xbc'
        
    def test_parse_bitstring_empty(self):
        bit_str = BitString() #just an empty bitstring
        with pytest.raises(IndexError) as e:
            parsley.parse_bitstring(bit_str)
        # message content is not asserted as an index error is expected
        
    def test_parse_bitstring_small(self):
        bit_str = BitString()
        bit_str.push(b'\xFF', 8) # only 8 bits, less than required 29 bits for SID
        with pytest.raises(IndexError) as e:
            parsley.parse_bitstring(bit_str)
        # message content is not asserted as an index error is expected
        
    def test_parse_bitstring_minimal(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 29)  # Exactly 29 bits for SID
        copy = BitString() #need a copy so that parse_bitstring can consume the copy
        copy.push(b'\x12\x34\x56\x78', 29)
        
        msg_sid, msg_data = parsley.parse_bitstring(copy) 

        print(msg_sid)
        print(msg_data)

        # Should get all 29 bits as SID, no remaining data
        assert len(msg_data) == 0
        # The SID should be the 29-bit value properly encoded
        assert isinstance(msg_sid, bytes)
        assert len(msg_sid) == 4  # 29 bits requires 4 bytes
        assert BitString(msg_sid, 29).data == bit_str.data
        
    def test_calculate_msg_bit_length(self):
        msg = CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')
        bit_len = parsley.calculate_msg_bit_len(msg)
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
        line = parsley.format_line(parsed_data)
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
        msg_sid, msg_data = parsley.encode_data(parsed_data)
        
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
        
        msg_sid, msg_data = parsley.parse_usb_debug(line)
        
        assert msg_sid == b'\x12\x34\xab\xcd' 
        assert msg_data == b'\x12\x34\x56\x78' 
        
    def test_parse_usb_data_empty(self):
        line = "$ABCD1234"
        msg_sid, msg_data = parsley.parse_usb_debug(line)
        
        assert msg_sid == b'\xab\xcd\x12\x34' 
        assert msg_data == b''
        
    def test_parse_usb_debug_invalid_format(self): # need a $ at start 
        line = "1234:AA,BB"
        with pytest.raises(ValueError) as e:
            parsley.parse_usb_debug(line)
        assert "Incorrect line format" in str(e.value)
            
    def test_parse_usb_debug_empty_line(self):
        line = ""
        with pytest.raises(ValueError) as e:
            parsley.parse_usb_debug(line)
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
        
        results = list(parsley.parse_logger(bytes(buf), 0x64))
        
        assert len(results) == 3

        msg_sid, msg_data = results[0]
        assert msg_sid == b'\x01\x11'  # Only uses bytes needed for 0x111
        assert msg_data == b'\x01\x02'
        
        msg_sid, msg_data = results[1]
        assert msg_sid == b'\x03\x33'
        assert msg_data == b'\x03\x04\x05'  
        
        msg_sid, msg_data = results[2]
        assert msg_sid == b'\x05\x55' 
        assert msg_data == b'\x06'
        
    def test_parse_logger_wrong_size(self):
        buf = b"LOG" + b"\x00" * (PARSE_LOGGER_PAGE_SIZE - 4)  # only 4095 bytes (3 for 'LOG', 1 for sequence)

        assert len(buf) < PARSE_LOGGER_PAGE_SIZE

        with pytest.raises(ValueError) as e:
            list(parsley.parse_logger(buf, 0))
        assert "exactly 4096 bytes" in str(e.value)
            
    def test_parse_logger_wrong_signature(self): # wrong LOG_MAGIC bytes
        buf = b"BAD" + b"\x00" * 4093
        with pytest.raises(ValueError) as e:
            list(parsley.parse_logger(buf, 0))
        assert "Missing 'LOG' signature" in str(e.value)
            
    def test_parse_logger_wrong_page_number(self):
        buf = b"LOG\x05" + b"\x00" * 4092  # Page 5 in buffer
        with pytest.raises(ValueError) as e:
            list(parsley.parse_logger(buf, 10))  # Expect page 10
        assert "Page number mismatch" in str(e.value)

    def test_parse_logger_empty(self):
        buf = bytearray(PARSE_LOGGER_PAGE_SIZE)
        buf[0:3] = b"LOG"
        buf[3] = 0
        
        buf[4:] = b"\xff" * (len(buf) - 4) # Fill unused bytes with 0xff

        results = list(parsley.parse_logger(bytes(buf), 0))
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

        msg_sid, msg_data = parsley.parse_live_telemetry(bytes(frame))
        
        expected_sid = 0x12345678 & 0x1FFFFFFF #29-bit mask
        assert msg_sid == expected_sid.to_bytes((expected_sid.bit_length() + 7) // 8, 'big')
        assert msg_data == b'\xaa\xbb\xcc'
        
    def test_parse_live_telemetry_too_short(self):
        frame = b'\x02\x06\x12\x34'  #4 bytes, need at least 7
        with pytest.raises(ValueError) as e:
            parsley.parse_live_telemetry(frame)
        assert "Incorrect frame length" in str(e.value)
            
    def test_parse_live_telemetry_wrong_header(self):
        frame = b'\x03\x08\x12\x34\x56\x78\xAA\x00'  #header = 0x03 instead of 0x02
        with pytest.raises(ValueError) as e:
            parsley.parse_live_telemetry(frame)
        assert "Incorrect frame header" in str(e.value)
            
    def test_parse_live_telemetry_bad_crc(self):
        
        frame = bytearray([0x02, 0x08, 0x12, 0x34, 0x56, 0x78, 0xAA, 0xFF])  # wrong CRC
        
        with pytest.raises(ValueError) as e:
            parsley.parse_live_telemetry(bytes(frame))
        assert "Bad checksum" in str(e.value)
