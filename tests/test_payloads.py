import pytest

from parsley.payloads import (
    get_payload_type,
    Payload,
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
    SENSOR_2D_ANALOG24,
    SENSOR_3D_ANALOG16,
    GPS_TIMESTAMP,
    GPS_LATITUDE,
    GPS_LONGITUDE,
    GPS_ALTITUDE,
    GPS_INFO,
    STREAM_STATUS,
    STREAM_DATA,
    STREAM_RETRY,
)
from parsley.bitstring import BitString
from parsley.parse_to_object import _ParsleyParseInternal
from parsley.parsley_message import ParsleyObject


def _make_bitstring(*byte_values: int) -> BitString:
    """Helper to build a BitString from individual byte values."""
    data = bytes(byte_values)
    return BitString(data, len(data) * 8)


# ── Factory function ────────────────────────────────────────────────────────


class TestGetPayloadType:
    """Tests for the get_payload_type factory function."""

    def test_raises_for_unknown_type(self):
        with pytest.raises(ValueError, match="Unknown message type"):
            get_payload_type("UNKNOWN_TYPE")

    def test_returns_none_for_leds_on(self):
        assert get_payload_type("LEDS_ON") is None

    def test_returns_none_for_leds_off(self):
        assert get_payload_type("LEDS_OFF") is None

    def test_returns_class_for_actuator_cmd(self):
        assert get_payload_type("ACTUATOR_CMD") is ACTUATOR_CMD

    def test_returns_class_for_sensor_analog16(self):
        assert get_payload_type("SENSOR_ANALOG16") is SENSOR_ANALOG16

    def test_returns_class_for_sensor_analog32(self):
        assert get_payload_type("SENSOR_ANALOG32") is SENSOR_ANALOG32

    def test_returns_class_for_sensor_2d_analog24(self):
        assert get_payload_type("SENSOR_2D_ANALOG24") is SENSOR_2D_ANALOG24

    def test_returns_class_for_sensor_3d_analog16(self):
        assert get_payload_type("SENSOR_3D_ANALOG16") is SENSOR_3D_ANALOG16


# ── Payload dataclass tests ─────────────────────────────────────────────────


class TestGeneralBoardStatus:
    def test_nominal(self):
        # timestamp=1234ms (0x04D2), board_error_bitfield=0x00000000 (nominal)
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.234, abs=0.01)
        assert result.board_error_bitfield == 'E_NOMINAL'

    def test_with_errors(self):
        # timestamp=1000ms (0x03E8), bit 1 set (E_5V_OVER_VOLTAGE)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00, 0x02)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        assert 'E_5V_OVER_VOLTAGE' in result.board_error_bitfield

    def test_to_dict(self):
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        d = result.to_dict()
        assert 'time' in d
        assert 'board_error_bitfield' in d

    def test_frozen(self):
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        with pytest.raises(AttributeError):
            result.time = 0  # type: ignore[misc]

    def test_to_bytes_round_trip(self):
        # Use timestamp=0 to avoid float precision issues
        bs = _make_bitstring(0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        encoded = result.to_bytes()
        assert encoded == bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


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
        bs = _make_bitstring(0x00, 0x64, 0x01, 0x01, 0x00, 0x01, 0x00, 0xFF)
        result = CONFIG_SET.from_bitstring(bs)
        assert result.time == pytest.approx(0.1, abs=0.01)
        assert result.board_type_id == 'INJECTOR'
        assert result.board_inst_id == 'GROUND'
        assert result.config_id == 1
        assert result.config_value == 255


class TestConfigStatus:
    def test_basic(self):
        bs = _make_bitstring(0x00, 0x64, 0x00, 0x01, 0x00, 0x42)
        result = CONFIG_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(0.1, abs=0.01)
        assert result.config_id == 1
        assert result.config_value == 66


class TestActuatorCmd:
    def test_basic(self):
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
        # timestamp=1000ms (0x03E8), cmd_state=ACT_STATE_ON(0x00), curr_state=ACT_STATE_OFF(0x01)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01)
        result = ACTUATOR_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.cmd_state == 'ACT_STATE_ON'
        assert result.curr_state == 'ACT_STATE_OFF'


class TestAltArmCmd:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 0x01)
        result = ALT_ARM_CMD.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.alt_arm_state == 'ALT_ARM_STATE_ARMED'


class TestAltArmStatus:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x03, 0xE8, 0x07, 0xD0)
        result = ALT_ARM_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.alt_arm_state == 'ALT_ARM_STATE_DISARMED'
        assert result.drogue_v == 1000
        assert result.main_v == 2000


class TestSensorAnalog16:
    def test_basic(self):
        bs = _make_bitstring(0x01, 0xF4, 0x04, 0xD2)
        result = SENSOR_ANALOG16.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value == 1234


class TestSensorAnalog32:
    def test_basic(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x01, 0x86, 0xA0)
        result = SENSOR_ANALOG32.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value == 100000


class TestSensor2DAnalog24:
    def test_basic(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x12, 0x34, 0x00, 0x56, 0x78)
        result = SENSOR_2D_ANALOG24.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value_x == 0x001234
        assert result.value_y == 0x005678

    def test_to_dict(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x12, 0x34, 0x00, 0x56, 0x78)
        result = SENSOR_2D_ANALOG24.from_bitstring(bs)
        d = result.to_dict()
        assert set(d.keys()) == {'time', 'value_x', 'value_y'}

    def test_frozen(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x12, 0x34, 0x00, 0x56, 0x78)
        result = SENSOR_2D_ANALOG24.from_bitstring(bs)
        with pytest.raises(AttributeError):
            result.time = 0  # type: ignore[misc]


class TestSensor3DAnalog16:
    def test_basic(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x64, 0x00, 0xC8, 0x01, 0x2C)
        result = SENSOR_3D_ANALOG16.from_bitstring(bs)
        assert result.time == pytest.approx(0.5, abs=0.01)
        assert result.value_x == 100
        assert result.value_y == 200
        assert result.value_z == 300

    def test_to_dict(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x64, 0x00, 0xC8, 0x01, 0x2C)
        result = SENSOR_3D_ANALOG16.from_bitstring(bs)
        d = result.to_dict()
        assert set(d.keys()) == {'time', 'value_x', 'value_y', 'value_z'}


class TestGpsTimestamp:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 12, 30, 45, 5)
        result = GPS_TIMESTAMP.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.hrs == 12
        assert result.mins == 30
        assert result.secs == 45
        assert result.dsecs == 5


class TestGpsLatitude:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 43, 28, 0x04, 0xD2, ord('N'))
        result = GPS_LATITUDE.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.degs == 43
        assert result.mins == 28
        assert result.dmins == 1234
        assert result.direction == 'N'


class TestGpsLongitude:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 80, 31, 0x16, 0x2E, ord('W'))
        result = GPS_LONGITUDE.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.degs == 80
        assert result.mins == 31
        assert result.dmins == 5678
        assert result.direction == 'W'


class TestGpsAltitude:
    def test_basic(self):
        # altitude is now 32-bit, no unit field
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x05, 0xDC, 50)
        result = GPS_ALTITUDE.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.altitude == 1500
        assert result.daltitude == 50

    def test_large_altitude(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01, 0x86, 0xA0, 0)
        result = GPS_ALTITUDE.from_bitstring(bs)
        assert result.altitude == 100000


class TestGpsInfo:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 12, 2)
        result = GPS_INFO.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.num_sats == 12
        assert result.quality == 2


class TestStreamStatus:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 0x01, 0x00, 0x00, 0x00, 0x80, 0x00)
        result = STREAM_STATUS.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.total_size == 0x010000
        assert result.tx_size == 0x008000


class TestStreamData:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x00)
        result = STREAM_DATA.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)
        assert result.data == 'Hello'


class TestStreamRetry:
    def test_basic(self):
        bs = _make_bitstring(0x03, 0xE8)
        result = STREAM_RETRY.from_bitstring(bs)
        assert result.time == pytest.approx(1.0, abs=0.01)


# ── Interface / structural tests ────────────────────────────────────────────


class TestPayloadInterface:
    """Verify every payload class implements the Payload interface."""

    ALL_TYPES: list[type[Payload]] = [
        GENERAL_BOARD_STATUS, RESET_CMD, DEBUG_RAW, CONFIG_SET, CONFIG_STATUS,
        ACTUATOR_CMD, ACTUATOR_STATUS, ALT_ARM_CMD, ALT_ARM_STATUS,
        SENSOR_ANALOG16, SENSOR_ANALOG32, SENSOR_2D_ANALOG24, SENSOR_3D_ANALOG16,
        GPS_TIMESTAMP, GPS_LATITUDE, GPS_LONGITUDE, GPS_ALTITUDE, GPS_INFO,
        STREAM_STATUS, STREAM_DATA, STREAM_RETRY,
    ]

    def test_all_types_are_subclasses(self):
        for cls in self.ALL_TYPES:
            assert issubclass(cls, Payload), f"{cls.__name__} is not a Payload subclass"

    def test_all_types_have_fields(self):
        for cls in self.ALL_TYPES:
            assert hasattr(cls, 'FIELDS'), f"{cls.__name__} missing FIELDS"
            assert len(cls.FIELDS) > 0, f"{cls.__name__} has empty FIELDS"

    def test_all_payload_map_types_covered(self):
        """Verify every non-None entry in _PAYLOAD_MAP is in ALL_TYPES."""
        from parsley.payloads import _PAYLOAD_MAP
        for name, cls in _PAYLOAD_MAP.items():
            if cls is not None:
                assert cls in self.ALL_TYPES, f"{name} -> {cls.__name__} not in ALL_TYPES"


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

    def test_sensor_2d_analog24_consumes_all_bits(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x12, 0x34, 0x00, 0x56, 0x78)
        SENSOR_2D_ANALOG24.from_bitstring(bs)
        assert bs.length == 0

    def test_sensor_3d_analog16_consumes_all_bits(self):
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x64, 0x00, 0xC8, 0x01, 0x2C)
        SENSOR_3D_ANALOG16.from_bitstring(bs)
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
        bs = _make_bitstring(0x04, 0xD2, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert set(d.keys()) == {'time', 'board_error_bitfield'}


class TestToBytes:
    """Verify to_bytes produces correct encoding."""

    def test_actuator_cmd_to_bytes(self):
        # Use timestamp=0 to avoid float precision issues with scaled timestamps
        bs = _make_bitstring(0x00, 0x00, 0x00)
        result = ACTUATOR_CMD.from_bitstring(bs)
        encoded = result.to_bytes()
        assert encoded == bytes([0x00, 0x00, 0x00])

    def test_sensor_analog16_to_bytes(self):
        bs = _make_bitstring(0x00, 0x00, 0x04, 0xD2)
        result = SENSOR_ANALOG16.from_bitstring(bs)
        encoded = result.to_bytes()
        assert encoded == bytes([0x00, 0x00, 0x04, 0xD2])

    def test_gps_altitude_to_bytes(self):
        bs = _make_bitstring(0x00, 0x00, 0x00, 0x00, 0x05, 0xDC, 50)
        result = GPS_ALTITUDE.from_bitstring(bs)
        encoded = result.to_bytes()
        assert encoded == bytes([0x00, 0x00, 0x00, 0x00, 0x05, 0xDC, 50])

    def test_to_bytes_non_timestamp_fields_exact(self):
        """Integer-only fields encode/decode exactly."""
        bs = _make_bitstring(0x00, 0x00, 12, 30, 45, 5)
        result = GPS_TIMESTAMP.from_bitstring(bs)
        encoded = result.to_bytes()
        assert encoded[2:] == bytes([12, 30, 45, 5])


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

    def test_leds_on_returns_none(self):
        msg_sid, msg_data = self._build_msg(
            'HIGHEST', 'LEDS_ON', '0', 'INJECTOR', 'ROCKET',
            []
        )
        result = _ParsleyParseInternal.parse_to_object(msg_sid, msg_data)
        assert isinstance(result, ParsleyObject)
        assert result.data is None
