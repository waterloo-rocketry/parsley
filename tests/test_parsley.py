import parsley
import pytest

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric
from parsley.payloads import TIMESTAMP_2

import parsley.message_types as mt
import utils as utilities
import crc8
import struct

from parsley.parse_to_object import (
    _MESSAGE_PRIO,
    _MESSAGE_TYPE,
    _BOARD_TYPE_ID,
    _BOARD_INST_ID,
    _MESSAGE_METADATA,
    _MESSAGE_SID,
)

PARSE_LOGGER_PAGE_SIZE = 4096


class TestParsley:
    def test_parse(self):
        msg_sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'GROUND')

        """
        HIGH = 0x1, GENERAL_BOARD_STATUS = 0x001, RLCS_RELAY = 0x0C, GROUND = 0x01, metadata = 0x00
        prio:  01
        type:  0000001
        btype: 001100
        binst: 000001
        meta:  00000000
        padded to 32 bits: 000 01000 00010011 00000001 00000000 = 0x08130100
        """
        assert msg_sid == b'\x08\x13\x01\x00'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(1.234))
        error_value = (1 << mt.board_error_bitfield_offset['E_5V_OVER_VOLTAGE'])
        bit_str.push(*Numeric('board_error_bitfield', 32).encode(error_value))

        msg_data = bit_str.pop(bit_str.length)

        res = parsley.parse(msg_sid, msg_data)

        expected_res = {
            'msg_type': 'GENERAL_BOARD_STATUS',
            'board_type_id': 'RLCS_RELAY',
            'board_inst_id': 'GROUND',
            'msg_prio': 'HIGH',
            'msg_metadata': 0,
            'data': {
                'time': utilities.approx(1.234),
                'board_error_bitfield': 'E_5V_OVER_VOLTAGE',
            }
        }

        assert res == expected_res

    def test_parse_partial_byte_fields(self):
        msg_sid = utilities.create_msg_sid_from_strings('LOW', 'DEBUG_RAW', '0', 'GPS', 'ROCKET')

        """
        LOW = 0x3, DEBUG_RAW = 0x003, GPS = 0x07, ROCKET = 0x02, metadata = 0x00
        prio:  11
        type:  0000011
        btype: 000111
        binst: 000010
        meta:  00000000
        padded to 32 bits: 000 11000 00110001 11000010 00000000 = 0x1831C200
        """
        assert msg_sid == b'\x18\x31\xC2\x00'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(0.133))
        bit_str.push(*ASCII('string', 48).encode('zZz'))
        msg_data = bit_str.pop(bit_str.length)

        res = parsley.parse(msg_sid, msg_data)

        expected_res = {
            'msg_type': 'DEBUG_RAW',
            'board_type_id': 'GPS',
            'board_inst_id': 'ROCKET',
            'msg_prio': 'LOW',
            'msg_metadata': 0,
            'data': {
                'time': utilities.approx(0.133),
                'string': 'zZz'
            }
        }

        assert res == expected_res

    def test_parse_sensor_analog(self):
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'SENSOR_ANALOG16', '0', 'PAYLOAD', 'ANY')

        """
        MEDIUM = 0x2, SENSOR_ANALOG16 = 0x00A, PAYLOAD(type) = 0x0A, ANY = 0x00, metadata = 0x00
        prio:  10
        type:  0001010
        btype: 001010
        binst: 000000
        meta:  00000000
        padded to 32 bits: 000 10000 10100010 10000000 00000000 = 0x10A28000
        """
        assert msg_sid == b'\x10\xA2\x80\x00'

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(12.345))
        bit_str.push(*Numeric('value', 16).encode(3300))
        msg_data = bit_str.pop(bit_str.length)

        res = parsley.parse(msg_sid, msg_data)

        expected_res = {
            'msg_type': 'SENSOR_ANALOG16',
            'board_type_id': 'PAYLOAD',
            'board_inst_id': 'ANY',
            'msg_prio': 'MEDIUM',
            'msg_metadata': 0,
            'data': {
                'time': utilities.approx(12.345),
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
        msg_sid = b'\xFF\xFF\xFF\xFF'
        msg_data = b'\x00\x00\x00\x00'
        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data']

    def test_parse_bad_board_type_id(self):
        # manually build message with invalid board_type_id
        bit_msg_sid = BitString()
        bit_msg_sid.push(*_MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*_MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x1F', _BOARD_TYPE_ID.length)  # invalid board_type
        bit_msg_sid.push(b'\x00', _BOARD_INST_ID.length)
        bit_msg_sid.push(*_MESSAGE_METADATA.encode(0))
        msg_sid = bit_msg_sid.pop(_MESSAGE_SID.length)

        res = parsley.parse(msg_sid, b'')
        assert '0x' in res['board_type_id']

    def test_parse_bad_msg_data(self):
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'ALT_ARM_STATUS', '0', 'ALTIMETER', 'ANY')
        msg_data = b'\x00\x00\x01'  # truncated
        res = parsley.parse(msg_sid, msg_data)
        assert 'error' in res['data']

    def test_bad_board_instance(self):
        bit_msg_sid = BitString()
        bit_msg_sid.push(*_MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*_MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(*_BOARD_TYPE_ID.encode('GPS'))
        bit_msg_sid.push(b'\x1F', _BOARD_INST_ID.length)  # invalid board instance
        bit_msg_sid.push(*_MESSAGE_METADATA.encode(0))
        msg_sid = bit_msg_sid.pop(_MESSAGE_SID.length)

        res = parsley.parse(msg_sid, b'')
        assert '0x' in res['board_inst_id']

    def test_parse_bitstring(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 32)
        bit_str.push(b'\x9A\xBC', 16)
        msg_sid, msg_data = parsley.parse_bitstring(bit_str)

        assert msg_sid == b'\x02\x46\x8a\xcf'
        assert msg_data == b'\x00\x9a\xbc'

    def test_parse_bitstring_empty(self):
        bit_str = BitString()
        with pytest.raises(IndexError):
            parsley.parse_bitstring(bit_str)

    def test_parse_bitstring_small(self):
        bit_str = BitString()
        bit_str.push(b'\xFF', 8)
        with pytest.raises(IndexError):
            parsley.parse_bitstring(bit_str)

    def test_parse_bitstring_minimal(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 29)
        copy = BitString()
        copy.push(b'\x12\x34\x56\x78', 29)

        msg_sid, msg_data = parsley.parse_bitstring(copy)

        assert len(msg_data) == 0
        assert isinstance(msg_sid, bytes)
        assert len(msg_sid) == 4
        assert BitString(msg_sid, 29).data == bit_str.data

    def test_calculate_msg_bit_length(self):
        from parsley.payloads import GENERAL_BOARD_STATUS
        bit_len = parsley.calculate_msg_bit_len(GENERAL_BOARD_STATUS.FIELDS)
        # Payload fields: time (16) + board_error_bitfield (32) = 48 bits
        assert bit_len == 48

    def test_format_line(self):
        parsed_data = {
            'msg_prio': 'HIGH',
            'msg_type': 'GENERAL_BOARD_STATUS',
            'board_type_id': 'RLCS_RELAY',
            'board_inst_id': 'ROCKET',
            'data': {
                'time': 1.234,
                'board_error_bitfield': 'E_5V_OVER_VOLTAGE',
            }
        }
        line = parsley.format_line(parsed_data)
        assert 'HIGH' in line
        assert 'GENERAL_BOARD_STATUS' in line
        assert 'RLCS_RELAY' in line
        assert 'ROCKET' in line
        assert '1.234' in line
        assert 'E_5V_OVER_VOLTAGE' in line

    def test_encode_data(self):
        parsed_data = {
            'msg_prio': 'MEDIUM',
            'msg_type': 'ALT_ARM_STATUS',
            'board_type_id': 'ALTIMETER',
            'board_inst_id': 'SIDE_LOOKING',
            'msg_metadata': 0,
            'time': 5.678,
            'alt_arm_state': 'ALT_ARM_STATE_ARMED',
            'drogue_v': 4095,
            'main_v': 2048
        }
        msg_sid, msg_data = parsley.encode_data(parsed_data)

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(5.678))
        bit_str.push(*Enum('alt_arm_state', 8, mt.alt_arm_state).encode('ALT_ARM_STATE_ARMED'))
        bit_str.push(*Numeric('drogue_v', 16).encode(4095))
        bit_str.push(*Numeric('main_v', 16).encode(2048))

        expected_msg_data = bytes(bit_str.pop(bit_str.length))
        assert msg_data == list(expected_msg_data)

    def test_parse_usb_debug(self):
        line = "$1234ABCD:12,34,56,78\r\n\0"
        msg_sid, msg_data = parsley.parse_usb_debug(line)
        assert msg_sid == b'\x12\x34\xab\xcd'
        assert msg_data == b'\x12\x34\x56\x78'

    def test_parse_usb_data_empty(self):
        line = "$ABCD1234"
        msg_sid, msg_data = parsley.parse_usb_debug(line)
        assert msg_sid == b'\xab\xcd\x12\x34'
        assert msg_data == b''

    def test_parse_usb_debug_invalid_format(self):
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
        buf[0:3] = b"LOG"
        buf[3] = 0x64

        offset = 4
        messages = [
            (0x111, 0x222, [0x01, 0x02]),
            (0x333, 0x444, [0x03, 0x04, 0x05]),
            (0x555, 0x666, [0x06])
        ]

        for sid, timestamp, data in messages:
            struct.pack_into("<IIB", buf, offset, sid, timestamp, len(data))
            offset += 9
            buf[offset:offset + len(data)] = data
            offset += len(data)

        buf[offset:] = b"\xff" * (len(buf) - offset)

        results = list(parsley.parse_logger(bytes(buf), 0x64))
        assert len(results) == 3

        msg_sid, msg_data = results[0]
        assert msg_sid == b'\x01\x11'
        assert msg_data == b'\x01\x02'

        msg_sid, msg_data = results[1]
        assert msg_sid == b'\x03\x33'
        assert msg_data == b'\x03\x04\x05'

        msg_sid, msg_data = results[2]
        assert msg_sid == b'\x05\x55'
        assert msg_data == b'\x06'

    def test_parse_logger_wrong_size(self):
        buf = b"LOG" + b"\x00" * (PARSE_LOGGER_PAGE_SIZE - 4)
        with pytest.raises(ValueError) as e:
            list(parsley.parse_logger(buf, 0))
        assert "exactly 4096 bytes" in str(e.value)

    def test_parse_logger_wrong_signature(self):
        buf = b"BAD" + b"\x00" * 4093
        with pytest.raises(ValueError) as e:
            list(parsley.parse_logger(buf, 0))
        assert "Missing 'LOG' signature" in str(e.value)

    def test_parse_logger_wrong_page_number(self):
        buf = b"LOG\x05" + b"\x00" * 4092
        with pytest.raises(ValueError) as e:
            list(parsley.parse_logger(buf, 10))
        assert "Page number mismatch" in str(e.value)

    def test_parse_logger_empty(self):
        buf = bytearray(PARSE_LOGGER_PAGE_SIZE)
        buf[0:3] = b"LOG"
        buf[3] = 0
        buf[4:] = b"\xff" * (len(buf) - 4)
        results = list(parsley.parse_logger(bytes(buf), 0))
        assert len(results) == 0

    def test_parse_live_telemetry_basic(self):
        frame = bytearray()
        frame.append(0x02)
        frame.append(10)
        sid = 0x12345678
        frame.append((sid >> 24) & 0x1F)
        frame.append((sid >> 16) & 0xFF)
        frame.append((sid >> 8) & 0xFF)
        frame.append(sid & 0xFF)
        frame.extend([0xAA, 0xBB, 0xCC])
        frame[1] = len(frame) + 1
        crc_val = crc8.crc8(frame).digest()[0]
        frame.append(crc_val)

        msg_sid, msg_data = parsley.parse_live_telemetry(bytes(frame))

        expected_sid = 0x12345678 & 0x1FFFFFFF
        assert msg_sid == expected_sid.to_bytes((expected_sid.bit_length() + 7) // 8, 'big')
        assert msg_data == b'\xaa\xbb\xcc'

    def test_parse_live_telemetry_too_short(self):
        frame = b'\x02\x06\x12\x34'
        with pytest.raises(ValueError) as e:
            parsley.parse_live_telemetry(frame)
        assert "Incorrect frame length" in str(e.value)

    def test_parse_live_telemetry_wrong_header(self):
        frame = b'\x03\x08\x12\x34\x56\x78\xAA\x00'
        with pytest.raises(ValueError) as e:
            parsley.parse_live_telemetry(frame)
        assert "Incorrect frame header" in str(e.value)

    def test_parse_live_telemetry_bad_crc(self):
        frame = bytearray([0x02, 0x08, 0x12, 0x34, 0x56, 0x78, 0xAA, 0xFF])
        with pytest.raises(ValueError) as e:
            parsley.parse_live_telemetry(bytes(frame))
        assert "Bad checksum" in str(e.value)
