import pytest

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric
from parsley.payloads import TIMESTAMP_2

import parsley.message_types as mt
import utils as utilities
import parsley
import crc8
import struct

from parsley.parse_to_object import (
    _ParsleyParseInternal,
    _MESSAGE_PRIO,
    _MESSAGE_TYPE,
    _BOARD_TYPE_ID,
    _BOARD_INST_ID,
    _MESSAGE_METADATA,
    _MESSAGE_SID,
    ParsleyParser,
    USBDebugParser,
    LiveTelemetryParser,
    LoggerParser,
    BitstringParser,
)
from parsley.parsley_message import ParsleyError, ParsleyObject

PARSE_LOGGER_PAGE_SIZE = 4096


class TestParseToObject:
    def _to_dict(self, result):
        if isinstance(result, ParsleyError):
            return {'data': {'error': result.error, 'msg_data': result.msg_data}, 'msg_type': result.msg_type}

        dumped = result.model_dump()
        # Convert Payload data to dict for backward-compatible assertions
        if dumped['data'] is not None and hasattr(result.data, 'to_dict'):
            dumped['data'] = result.data.to_dict()
        return dumped

    def test_internal_class_cannot_be_instantiated(self):
        with pytest.raises(NotImplementedError) as e:
            _ParsleyParseInternal()
        assert "static only" in str(e.value)

    def test_parse(self):
        msg_sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'GROUND')

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(1.234))
        error_value = (1 << mt.board_error_bitfield_offset['E_5V_OVER_VOLTAGE'])
        bit_str.push(*Numeric('board_error_bitfield', 32).encode(error_value))

        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

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

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(0.133))
        bit_str.push(*ASCII('string', 48).encode('zZz'))
        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

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

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(12.345))
        bit_str.push(*Numeric('value', 16).encode(3300))
        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

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

    def test_parse_nonzero_metadata(self):
        msg_sid = utilities.create_msg_sid_from_strings('LOW', 'DEBUG_RAW', '42', 'GPS', 'ROCKET')

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(1.0))
        bit_str.push(*ASCII('string', 48).encode('abc'))
        msg_data = bit_str.pop(bit_str.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

        assert res['msg_metadata'] == 42
        assert res['msg_type'] == 'DEBUG_RAW'

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
        msg_sid = b'\xFF\xFF\xFF\xFF'
        msg_data = b'\x00\x00\x00\x00'
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error

    def test_parse_bad_board_type_id(self):
        # manually build message with invalid board_type_id
        bit_msg_sid = BitString()
        bit_msg_sid.push(*_MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*_MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(b'\x1F', _BOARD_TYPE_ID.length)  # invalid board_type
        bit_msg_sid.push(b'\x00', _BOARD_INST_ID.length)
        bit_msg_sid.push(*_MESSAGE_METADATA.encode(0))
        msg_sid = bit_msg_sid.pop(_MESSAGE_SID.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, b'')
        assert isinstance(result, ParsleyObject)
        assert str(result.board_type_id) == "0x1F"
        assert str(result.board_inst_id) == "ANY"
        assert result.msg_prio == "LOW"
        assert result.msg_type == "LEDS_ON"

    def test_parse_bad_msg_data(self):
        msg_sid = utilities.create_msg_sid_from_strings('MEDIUM', 'ALT_ARM_STATUS', '0', 'ALTIMETER', 'ANY')
        msg_data = b'\x00\x00\x01'  # truncated
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error

    def test_bad_board_instance(self):
        bit_msg_sid = BitString()
        bit_msg_sid.push(*_MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(*_MESSAGE_TYPE.encode('LEDS_ON'))
        bit_msg_sid.push(*_BOARD_TYPE_ID.encode('GPS'))
        bit_msg_sid.push(b'\x1F', _BOARD_INST_ID.length)  # invalid board instance
        bit_msg_sid.push(*_MESSAGE_METADATA.encode(0))
        msg_sid = bit_msg_sid.pop(_MESSAGE_SID.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, b'')
        assert isinstance(result, ParsleyObject)
        assert str(result.board_type_id) == "GPS"
        assert str(result.board_inst_id) == "0x1F"
        assert str(result.msg_prio) == "LOW"
        assert str(result.msg_type) == "LEDS_ON"

    def test_parse_bitstring(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 32)
        bit_str.push(b'\x9A\xBC', 16)
        result = BitstringParser().parse(bit_str)
        res = self._to_dict(result)
        assert res['msg_type'].startswith('0x')
        assert int(res['data']['msg_data'], 16) == int(b'\x00\x9a\xbc'.hex(), 16)

    def test_parse_bitstring_empty(self):
        bit_str = BitString()
        with pytest.raises(IndexError):
            BitstringParser().parse(bit_str)

    def test_parse_bitstring_small(self):
        bit_str = BitString()
        bit_str.push(b'\xFF', 8)
        with pytest.raises(IndexError):
            BitstringParser().parse(bit_str)

    def test_parse_bitstring_minimal(self):
        bit_str = BitString()
        bit_str.push(b'\x12\x34\x56\x78', 29)
        copy = BitString()
        copy.push(b'\x12\x34\x56\x78', 29)

        result = BitstringParser().parse(copy)
        res = self._to_dict(result)
        assert isinstance(res['data'], dict)
        assert res['data']['msg_data'] == '0x0'

    def test_calculate_msg_bit_length(self):
        from parsley.payloads import GENERAL_BOARD_STATUS
        # Payload fields only: time (16) + board_error_bitfield (32) = 48 bits
        bit_len = _ParsleyParseInternal.calculate_msg_bit_len(GENERAL_BOARD_STATUS.FIELDS)
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
        line = _ParsleyParseInternal.format_line(parsed_data)
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
        msg_sid, msg_data = _ParsleyParseInternal.encode_data(parsed_data)

        bit_str = BitString()
        bit_str.push(*TIMESTAMP_2.encode(5.678))
        bit_str.push(*Enum('alt_arm_state', 8, mt.alt_arm_state).encode('ALT_ARM_STATE_ARMED'))
        bit_str.push(*Numeric('drogue_v', 16).encode(4095))
        bit_str.push(*Numeric('main_v', 16).encode(2048))

        expected_msg_data = bytes(bit_str.pop(bit_str.length))
        assert msg_data == list(expected_msg_data)

    def test_encode_parse_actuator_cmd_metadata(self):
        actuator_id = mt.actuator_id['ACTUATOR_FUEL_INJECTOR_VALVE']
        parsed_data = {
            'msg_prio': 'HIGH',
            'msg_type': 'ACTUATOR_CMD',
            'board_type_id': 'INJECTOR',
            'board_inst_id': 'ROCKET',
            'msg_metadata': actuator_id,
            'time': 1.0,
            'cmd_state': 'ACT_STATE_ON',
        }
        msg_sid, msg_data = _ParsleyParseInternal.encode_data(parsed_data)
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        res = self._to_dict(result)

        assert res['msg_metadata'] == actuator_id
        assert res['msg_type'] == 'ACTUATOR_CMD'

    def test_parse_usb_debug(self):
        line = "$1234ABCD:12,34,56,78\r\n\0"
        result = USBDebugParser().parse(line)
        res = self._to_dict(result)
        assert int(res['data']['msg_data'], 16) == int(b'\x12\x34\x56\x78'.hex(), 16)

    def test_parse_usb_data_empty(self):
        line = "$ABCD1234"
        result = USBDebugParser().parse(line)
        res = self._to_dict(result)
        assert isinstance(res['data'], dict)
        assert res['data'].get('msg_data') == '0x0'

    def test_parse_usb_debug_invalid_format(self):
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
        buf = b"LOG" + b"\x00" * (PARSE_LOGGER_PAGE_SIZE - 4)
        with pytest.raises(ValueError) as e:
            list(LoggerParser().parse(buf, 0))
        assert "exactly 4096 bytes" in str(e.value)

    def test_parse_logger_wrong_signature(self):
        buf = b"BAD" + b"\x00" * 4093
        with pytest.raises(ValueError) as e:
            list(LoggerParser().parse(buf, 0))
        assert "Missing 'LOG' signature" in str(e.value)

    def test_parse_logger_wrong_page_number(self):
        buf = b"LOG\x05" + b"\x00" * 4092
        with pytest.raises(ValueError) as e:
            list(LoggerParser().parse(buf, 10))
        assert "Page number mismatch" in str(e.value)

    def test_parse_logger_empty(self):
        buf = bytearray(PARSE_LOGGER_PAGE_SIZE)
        buf[0:3] = b"LOG"
        buf[3] = 0
        buf[4:] = b"\xff" * (len(buf) - 4)
        results = list(LoggerParser().parse(bytes(buf), 0))
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

        result = LiveTelemetryParser().parse(bytes(frame))
        res = self._to_dict(result)
        expected_val = int.from_bytes(b'\xaa\xbb\xcc', 'big')
        assert res['msg_type'].startswith('0x')
        assert int(res['data']['msg_data'], 16) == expected_val

    def test_parse_live_telemetry_too_short(self):
        frame = b'\x02\x06\x12\x34'
        with pytest.raises(ValueError) as e:
            LiveTelemetryParser().parse(frame)
        assert "Incorrect frame length" in str(e.value)

    def test_parse_live_telemetry_wrong_header(self):
        frame = b'\x03\x08\x12\x34\x56\x78\xAA\x00'
        with pytest.raises(ValueError) as e:
            LiveTelemetryParser().parse(frame)
        assert "Incorrect frame header" in str(e.value)

    def test_parse_live_telemetry_bad_crc(self):
        frame = bytearray([0x02, 0x08, 0x12, 0x34, 0x56, 0x78, 0xAA, 0xFF])
        with pytest.raises(ValueError) as e:
            LiveTelemetryParser().parse(bytes(frame))
        assert "Bad checksum" in str(e.value)

    def test_parse_unknown_message_type_returns_error(self):
        """Verify that an unknown msg_type in the SID produces a ParsleyError."""
        # Build a SID with a valid priority but unknown msg_type (0x7F = max 7-bit value)
        bit_msg_sid = BitString()
        bit_msg_sid.push(*_MESSAGE_PRIO.encode('LOW'))
        bit_msg_sid.push(b'\x7F', _MESSAGE_TYPE.length)  # unknown msg_type
        bit_msg_sid.push(*_BOARD_TYPE_ID.encode('GPS'))
        bit_msg_sid.push(b'\x00', _BOARD_INST_ID.length)
        bit_msg_sid.push(*_MESSAGE_METADATA.encode(0))
        msg_sid = bit_msg_sid.pop(_MESSAGE_SID.length)

        result = _ParsleyParseInternal.parse_to_object(msg_sid, b'\x00\x00')
        assert isinstance(result, ParsleyError)
        assert 'error' in result.error
