import pytest

from parsley.types import (
    parse_payload,
    ParsleyDataPayload,
    GENERAL_BOARD_STATUS,
    RESET_CMD,
    DEBUG_RAW,
    CONFIG_SET,
    CONFIG_STATUS,
    ACTUATOR_CMD,
    ACTUATOR_STATUS,
    ALT_ARM_CMD,
    ALT_ARM_STATUS,
    SENSOR_ANALOG16,
    SENSOR_ANALOG32,
    SENSOR_DEM_ANALOG16,
    GPS_TIMESTAMP,
    GPS_LATITUDE,
    GPS_LONGITUDE,
    GPS_ALTITUDE,
    GPS_INFO,
    STREAM_STATUS,
    STREAM_DATA,
    STREAM_RETRY,
    MESSAGES,
    _SID_HEADER,
)
from parsley.bitstring import BitString
from parsley import message_types as mt
from parsley.parse_to_object import _ParsleyParseInternal
from parsley.parsley_message import ParsleyObject


def _make_bitstring(*byte_values: int) -> BitString:
    """Helper to build a BitString from individual byte values."""
    data = bytes(byte_values)
    return BitString(data, len(data) * 8)


# ── Factory function ────────────────────────────────────────────────────────

class TestParsePayloadFactory:
    """Tests for the parse_payload factory function."""

    def test_returns_none_for_unknown_type(self):
        bs = BitString(b'\x00\x00', 16)
        result = parse_payload("UNKNOWN_TYPE", bs)
        assert result is None

    def test_returns_none_for_leds_on(self):
        bs = BitString(b'', 0)
        result = parse_payload("LEDS_ON", bs)
        assert result is None

    def test_returns_none_for_leds_off(self):
        bs = BitString(b'', 0)
        result = parse_payload("LEDS_OFF", bs)
        assert result is None

    def test_dispatches_actuator_cmd(self):
        # timestamp=1000ms (0x03E8), state=ACT_STATE_ON (0x00)
        bs = _make_bitstring(0x03, 0xE8, 0x00)
        result = parse_payload("ACTUATOR_CMD", bs)
        assert isinstance(result, ACTUATOR_CMD)

    def test_dispatches_sensor_analog16(self):
        # timestamp=500 (0x01F4), value=100 (0x0064)
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x64)
        result = parse_payload("SENSOR_ANALOG16", bs)
        assert isinstance(result, SENSOR_ANALOG16)

    def test_dispatches_sensor_analog32(self):
        # timestamp=500 (0x01F4), value=100000 (0x000186A0)
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x01, 0x86, 0xA0)
        result = parse_payload("SENSOR_ANALOG32", bs)
        assert isinstance(result, SENSOR_ANALOG32)


# ── Payload dataclass tests ─────────────────────────────────────────────────

class TestGeneralBoardStatus:
    def test_nominal(self):
        # timestamp=1234ms (0x04D2), status=0x00000000 (nominal), error=0x0000 (nominal)
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.234, abs=0.01)
        assert result.general_board_status == 'E_NOMINAL'
        assert result.board_error_bitfield == 'E_NOMINAL'

    def test_with_errors(self):
        # timestamp=1000ms (0x03E8), status bit 1 set (E_5V_OVER_VOLTAGE), error bit 1 set (E_5V_EFUSE_FAULT)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00, 0x02, 0x00, 0x02)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        assert 'E_5V_OVER_VOLTAGE' in result.general_board_status
        assert 'E_5V_EFUSE_FAULT' in result.board_error_bitfield

    def test_to_dict(self):
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        d = result.to_dict()
        assert 'time' in d
        assert 'general_board_status' in d
        assert 'board_error_bitfield' in d

    def test_frozen(self):
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        with pytest.raises(AttributeError):
            result.time = 0  # type: ignore[misc]


class TestResetCmd:
    def test_basic(self):
        # timestamp=500ms (0x01F4), board_type=INJECTOR(1), board_inst=GROUND(1)
        bs = _make_bitstring(0x01, 0xF4, 0x01, 0x01)
        result = RESET_CMD.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.board_type_id == 'INJECTOR'
        assert result.board_inst_id == 'GROUND'


class TestDebugRaw:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), 6 ASCII chars "Hello\x00"
        bs = _make_bitstring(0x03, 0xE8, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x00)
        result = DEBUG_RAW.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.string == 'Hello'

    def test_short_string(self):
        bs = _make_bitstring(0x03, 0xE8, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = DEBUG_RAW.from_bitstring(bs)
        assert result.string == 'A'


class TestConfigSet:
    def test_basic(self):
        # timestamp=100ms (0x0064), board_type=INJECTOR(1), board_inst=GROUND(1), config_id=0x0001, config_value=0x00FF
        bs = _make_bitstring(0x00, 0x64, 0x01, 0x01, 0x00, 0x01, 0x00, 0xFF)
        result = CONFIG_SET.from_bitstring(bs)
        assert result.time == pytest.approx(0.1, abs=0.01)
        assert result.board_type_id == 'INJECTOR'
        assert result.board_inst_id == 'GROUND'
        assert result.config_id == 1
        assert result.config_value == 255


class TestConfigStatus:
    def test_basic(self):
        # timestamp=100ms (0x0064), config_id=0x0001, config_value=0x0042
        bs = _make_bitstring(0x00, 0x64, 0x00, 0x01, 0x00, 0x42)
        result = CONFIG_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(0.1, abs=0.01)
        assert result.config_id == 1
        assert result.config_value == 66


class TestActuatorCmd:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), cmd_state=ACT_STATE_ON(0x00)
        bs = _make_bitstring(0x03, 0xE8, 0x00)
        result = ACTUATOR_CMD.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.cmd_state == 'ACT_STATE_ON'

    def test_off_state(self):
        bs = _make_bitstring(0x03, 0xE8, 0x01)
        result = ACTUATOR_CMD.from_bitstring(bs)
        assert result.cmd_state == 'ACT_STATE_OFF'

    def test_to_dict(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00)
        result = ACTUATOR_CMD.from_bitstring(bs)
        d = result.to_dict()
        assert d == {'time': pytest.approx(1.0, abs=0.01), 'cmd_state': 'ACT_STATE_ON'}


class TestActuatorStatus:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), curr_state=ACT_STATE_ON(0x00), cmd_state=ACT_STATE_OFF(0x01)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01)
        result = ACTUATOR_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.curr_state == 'ACT_STATE_ON'
        assert result.cmd_state == 'ACT_STATE_OFF'


class TestAltArmCmd:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), alt_arm_state=ALT_ARM_STATE_ARMED(0x01)
        bs = _make_bitstring(0x03, 0xE8, 0x01)
        result = ALT_ARM_CMD.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.alt_arm_state == 'ALT_ARM_STATE_ARMED'


class TestAltArmStatus:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), alt_arm_state=ALT_ARM_STATE_DISARMED(0x00),
        # drogue_v=1000 (0x03E8), main_v=2000 (0x07D0)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x03, 0xE8, 0x07, 0xD0)
        result = ALT_ARM_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.alt_arm_state == 'ALT_ARM_STATE_DISARMED'
        assert result.drogue_v == 1000
        assert result.main_v == 2000


class TestSensorAnalog16:
    def test_basic(self):
        # timestamp=500ms (0x01F4), value=1234 (0x04D2)
        bs = _make_bitstring(0x01, 0xF4, 0x04, 0xD2)
        result = SENSOR_ANALOG16.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value == 1234


class TestSensorAnalog32:
    def test_basic(self):
        # timestamp=500ms (0x01F4), value=100000 (0x000186A0)
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x01, 0x86, 0xA0)
        result = SENSOR_ANALOG32.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value == 100000


class TestSensorDemAnalog16:
    def test_basic(self):
        # timestamp=500ms (0x01F4), value_x=100 (0x0064), value_y=200 (0x00C8), value_z=300 (0x012C)
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x64, 0x00, 0xC8, 0x01, 0x2C)
        result = SENSOR_DEM_ANALOG16.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value_x == 100
        assert result.value_y == 200
        assert result.value_z == 300


class TestGpsTimestamp:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), hrs=12, mins=30, secs=45, dsecs=5
        bs = _make_bitstring(0x03, 0xE8, 12, 30, 45, 5)
        result = GPS_TIMESTAMP.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.hrs == 12
        assert result.mins == 30
        assert result.secs == 45
        assert result.dsecs == 5


class TestGpsLatitude:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), degs=43, mins=28, dmins=1234 (0x04D2), direction='N'
        bs = _make_bitstring(0x03, 0xE8, 43, 28, 0x04, 0xD2, ord('N'))
        result = GPS_LATITUDE.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.degs == 43
        assert result.mins == 28
        assert result.dmins == 1234
        assert result.direction == 'N'


class TestGpsLongitude:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), degs=80, mins=31, dmins=5678 (0x162E), direction='W'
        bs = _make_bitstring(0x03, 0xE8, 80, 31, 0x16, 0x2E, ord('W'))
        result = GPS_LONGITUDE.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.degs == 80
        assert result.mins == 31
        assert result.dmins == 5678
        assert result.direction == 'W'


class TestGpsAltitude:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), altitude=1500 (0x05DC), daltitude=50, unit='M'
        bs = _make_bitstring(0x03, 0xE8, 0x05, 0xDC, 50, ord('M'))
        result = GPS_ALTITUDE.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.altitude == 1500
        assert result.daltitude == 50
        assert result.unit == 'M'


class TestGpsInfo:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), num_sats=12, quality=2
        bs = _make_bitstring(0x03, 0xE8, 12, 2)
        result = GPS_INFO.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.num_sats == 12
        assert result.quality == 2


class TestStreamStatus:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), total_size=0x010000, tx_size=0x008000
        bs = _make_bitstring(0x03, 0xE8, 0x01, 0x00, 0x00, 0x00, 0x80, 0x00)
        result = STREAM_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.total_size == 0x010000
        assert result.tx_size == 0x008000


class TestStreamData:
    def test_basic(self):
        # timestamp=1000ms (0x03E8), data="Hello\x00" (48 bits = 6 bytes)
        bs = _make_bitstring(0x03, 0xE8, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x00)
        result = STREAM_DATA.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.data == 'Hello'


class TestStreamRetry:
    def test_basic(self):
        # timestamp=1000ms (0x03E8)
        bs = _make_bitstring(0x03, 0xE8)
        result = STREAM_RETRY.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)


# ── Interface / structural tests ────────────────────────────────────────────

class TestPayloadInterface:
    """Verify every payload class implements the ParsleyDataPayload interface."""

    ALL_TYPES = [
        GENERAL_BOARD_STATUS, RESET_CMD, DEBUG_RAW, CONFIG_SET, CONFIG_STATUS,
        ACTUATOR_CMD, ACTUATOR_STATUS, ALT_ARM_CMD, ALT_ARM_STATUS,
        SENSOR_ANALOG16, SENSOR_ANALOG32, SENSOR_DEM_ANALOG16,
        GPS_TIMESTAMP, GPS_LATITUDE, GPS_LONGITUDE, GPS_ALTITUDE, GPS_INFO,
        STREAM_STATUS, STREAM_DATA, STREAM_RETRY,
    ]

    def test_all_types_are_subclasses(self):
        for cls in self.ALL_TYPES:
            assert issubclass(cls, ParsleyDataPayload), f"{cls.__name__} is not a ParsleyDataPayload subclass"

    def test_all_types_have_fields(self):
        for cls in self.ALL_TYPES:
            assert hasattr(cls, 'FIELDS'), f"{cls.__name__} missing FIELDS"
            assert len(cls.FIELDS) > 0, f"{cls.__name__} has empty FIELDS"

    def test_fields_match_messages_dict(self):
        """Verify MESSAGES dict is built correctly from FIELDS."""
        sid_len = len(_SID_HEADER)
        for msg_type, fields in MESSAGES.items():
            if msg_type in ('LEDS_ON', 'LEDS_OFF'):
                assert len(fields) == sid_len
                continue
            payload_fields = fields[sid_len:]
            # Find the payload class for this msg_type
            result = parse_payload(msg_type, _make_bitstring(*([0] * 8)))
            if result is not None:
                assert payload_fields == type(result).FIELDS


class TestRoundTrip:
    """Verify from_bitstring consumes the expected number of bits."""

    def test_actuator_cmd_consumes_all_bits(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00)
        ACTUATOR_CMD.from_bitstring(bs)
        assert bs.length == 0

    def test_gps_info_consumes_all_bits(self):
        bs = _make_bitstring(0x03, 0xE8, 12, 2)
        GPS_INFO.from_bitstring(bs)
        assert bs.length == 0

    def test_stream_retry_consumes_all_bits(self):
        bs = _make_bitstring(0x03, 0xE8)
        STREAM_RETRY.from_bitstring(bs)
        assert bs.length == 0


class TestToDictRoundTrip:
    """Verify to_dict produces the expected dict structure."""

    def test_actuator_cmd_to_dict(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00)
        result = ACTUATOR_CMD.from_bitstring(bs)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert set(d.keys()) == {'time', 'cmd_state'}
        assert d['cmd_state'] == 'ACT_STATE_ON'

    def test_general_board_status_to_dict(self):
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert set(d.keys()) == {'time', 'general_board_status', 'board_error_bitfield'}


class TestParseToObjectIntegration:
    """Verify parse_to_object stores typed payloads in ParsleyObject.data."""

    def _build_msg(self, prio, msg_type, metadata, board_type, board_inst, data_bytes):
        import utils as utilities
        msg_sid = utilities.create_msg_sid_from_strings(prio, msg_type, metadata, board_type, board_inst)
        msg_data = bytes(data_bytes)
        return msg_sid, msg_data

    def test_typed_payload_in_data(self):
        msg_sid, msg_data = self._build_msg(
            'HIGHEST', 'ACTUATOR_CMD', '0', 'INJECTOR', 'ROCKET',
            [0x03, 0xE8, 0x00]
        )
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyObject)
        assert isinstance(result.data, ACTUATOR_CMD)
        assert result.data.cmd_state == 'ACT_STATE_ON'

    def test_legacy_model_dump_still_works(self):
        msg_sid, msg_data = self._build_msg(
            'HIGHEST', 'ACTUATOR_CMD', '0', 'INJECTOR', 'ROCKET',
            [0x03, 0xE8, 0x00]
        )
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyObject)
        dumped = result.model_dump(mode='json')
        assert dumped['data'] == {'time': pytest.approx(1.0, abs=0.01), 'cmd_state': 'ACT_STATE_ON'}

    def test_leds_on_returns_empty_dict(self):
        msg_sid, msg_data = self._build_msg(
            'HIGHEST', 'LEDS_ON', '0', 'INJECTOR', 'ROCKET',
            []
        )
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyObject)
        assert result.data == {}
