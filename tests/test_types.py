import pytest
import struct

from parsley.types import (
    parse_payload,
    ParsleyDataPayload,
    GENERAL_BOARD_STATUS,
    RESET_CMD,
    DEBUG_RAW,
    CONFIG_SET,
    CONFIG_STATUS,
    ACTUATOR_CMD,
    ACTUATOR_ANALOG_CMD,
    ACTUATOR_STATUS,
    ALT_ARM_CMD,
    ALT_ARM_STATUS,
    SENSOR_ALTITUDE,
    SENSOR_IMU,
    SENSOR_MAG,
    SENSOR_BARO,
    SENSOR_ANALOG,
    GPS_TIMESTAMP,
    GPS_LATITUDE,
    GPS_LONGITUDE,
    GPS_ALTITUDE,
    GPS_INFO,
    STATE_EST_DATA,
    STREAM_STATUS,
    STREAM_DATA,
    STREAM_RETRY,
)
from parsley.bitstring import BitString
from parsley import message_types as mt


def _make_bitstring(*byte_values: int) -> BitString:
    """Helper to build a BitString from individual byte values."""
    data = bytes(byte_values)
    return BitString(data, len(data) * 8)


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
        # timestamp=1000 (0x03E8), actuator=ACTUATOR_OX_INJECTOR_VALVE (0x00), state=ACT_STATE_ON (0x00)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00)
        result = parse_payload("ACTUATOR_CMD", bs)
        assert isinstance(result, ACTUATOR_CMD)

    def test_dispatches_sensor_imu_x(self):
        # timestamp=500 (0x01F4), imu_id=IMU_PROC_ALTIMU10 (0x00), accel=100 (0x0064), vel=200 (0x00C8)
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x00, 0x64, 0x00, 0xC8)
        result = parse_payload("SENSOR_IMU_X", bs)
        assert isinstance(result, SENSOR_IMU)

    def test_dispatches_sensor_mag_y(self):
        # timestamp=500 (0x01F4), imu_id=IMU_PROC_ALTIMU10 (0x00), mag=42 (0x002A)
        bs = _make_bitstring(0x01, 0xF4, 0x00, 0x00, 0x2A)
        result = parse_payload("SENSOR_MAG_Y", bs)
        assert isinstance(result, SENSOR_MAG)


class TestGeneralBoardStatus:
    def test_nominal(self):
        # timestamp=1000 (0x03E8), board_status=0x00000000 (nominal), error_bitfield=0x0000 (nominal)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        assert result.time == 1.0
        assert result.general_board_status == "E_NOMINAL"
        assert result.board_error_bitfield == "E_NOMINAL"
        assert result.get_identifier() is None
        assert result.get_time() == 1.0

    def test_with_errors(self):
        # timestamp=2000, board_status=0x00000001 (E_5V_OVER_CURRENT), error=0x0000
        bs = _make_bitstring(0x07, 0xD0, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        assert result.time == 2.0
        assert "E_5V_OVER_CURRENT" in result.general_board_status

    def test_get_data_dict(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        d = result.get_data_dict()
        assert "general_board_status" in d
        assert "board_error_bitfield" in d

    def test_frozen(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
        result = GENERAL_BOARD_STATUS.from_bitstring(bs)
        with pytest.raises(AttributeError):
            result.time = 2.0


class TestResetCmd:
    def test_basic(self):
        # timestamp=500 (0x01F4), board_type=INJ_SENSOR (0x01), board_inst=GROUND (0x01)
        bs = _make_bitstring(0x01, 0xF4, 0x01, 0x01)
        result = RESET_CMD.from_bitstring(bs)
        assert result.time == 0.5
        assert result.board_type_id == "INJ_SENSOR"
        assert result.board_inst_id == "GROUND"
        assert result.get_identifier() is None


class TestDebugRaw:
    def test_basic(self):
        # timestamp=1000 (0x03E8), string="Hello!" (6 bytes = 48 bits)
        bs = _make_bitstring(0x03, 0xE8, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x21)
        result = DEBUG_RAW.from_bitstring(bs)
        assert result.time == 1.0
        assert result.string == "Hello!"

    def test_short_string(self):
        # timestamp=1000, string="Hi" with null padding
        bs = _make_bitstring(0x03, 0xE8, 0x48, 0x69, 0x00, 0x00, 0x00, 0x00)
        result = DEBUG_RAW.from_bitstring(bs)
        assert result.string == "Hi"


class TestConfigSet:
    def test_basic(self):
        # timestamp=1000, board_type=ANY (0x00), board_inst=ANY (0x00), config_id=0x0001, config_value=0x00FF
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00, 0x01, 0x00, 0xFF)
        result = CONFIG_SET.from_bitstring(bs)
        assert result.time == 1.0
        assert result.board_type_id == "ANY"
        assert result.board_inst_id == "ANY"
        assert result.config_id == 1
        assert result.config_value == 255


class TestConfigStatus:
    def test_basic(self):
        # timestamp=1000, config_id=0x0002, config_value=0x0064
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x02, 0x00, 0x64)
        result = CONFIG_STATUS.from_bitstring(bs)
        assert result.time == 1.0
        assert result.config_id == 2
        assert result.config_value == 100


class TestActuatorCmd:
    def test_basic(self):
        # timestamp=1000, actuator=ACTUATOR_OX_INJECTOR_VALVE (0x00), state=ACT_STATE_ON (0x00)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00)
        result = ACTUATOR_CMD.from_bitstring(bs)
        assert result.time == 1.0
        assert result.actuator == "ACTUATOR_OX_INJECTOR_VALVE"
        assert result.cmd_state == "ACT_STATE_ON"
        assert result.get_identifier() == "ACTUATOR_OX_INJECTOR_VALVE"

    def test_off_state(self):
        # timestamp=2000, actuator=ACTUATOR_FUEL_INJECTOR_VALVE (0x01), state=ACT_STATE_OFF (0x01)
        bs = _make_bitstring(0x07, 0xD0, 0x01, 0x01)
        result = ACTUATOR_CMD.from_bitstring(bs)
        assert result.actuator == "ACTUATOR_FUEL_INJECTOR_VALVE"
        assert result.cmd_state == "ACT_STATE_OFF"

    def test_data_dict(self):
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00)
        result = ACTUATOR_CMD.from_bitstring(bs)
        d = result.get_data_dict()
        assert d == {"actuator": "ACTUATOR_OX_INJECTOR_VALVE", "cmd_state": "ACT_STATE_ON"}


class TestActuatorAnalogCmd:
    def test_basic(self):
        # timestamp=1000, actuator=ACTUATOR_CANARD_ANGLE (0x11), cmd_state=0x0100
        bs = _make_bitstring(0x03, 0xE8, 0x11, 0x01, 0x00)
        result = ACTUATOR_ANALOG_CMD.from_bitstring(bs)
        assert result.time == 1.0
        assert result.actuator == "ACTUATOR_CANARD_ANGLE"
        assert result.cmd_state == 256
        assert result.get_identifier() == "ACTUATOR_CANARD_ANGLE"


class TestActuatorStatus:
    def test_basic(self):
        # timestamp=1000, actuator=ACTUATOR_OX_INJECTOR_VALVE (0x00),
        # curr_state=ACT_STATE_ON (0x00), cmd_state=ACT_STATE_ON (0x00)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x00)
        result = ACTUATOR_STATUS.from_bitstring(bs)
        assert result.time == 1.0
        assert result.actuator == "ACTUATOR_OX_INJECTOR_VALVE"
        assert result.curr_state == "ACT_STATE_ON"
        assert result.cmd_state == "ACT_STATE_ON"


class TestAltArmCmd:
    def test_basic(self):
        # timestamp=1000, alt_id=ALTIMETER_ROCKET_RAVEN (0x00), alt_arm_state=ALT_ARM_STATE_ARMED (0x01)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01)
        result = ALT_ARM_CMD.from_bitstring(bs)
        assert result.time == 1.0
        assert result.alt_id == "ALTIMETER_ROCKET_RAVEN"
        assert result.alt_arm_state == "ALT_ARM_STATE_ARMED"
        assert result.get_identifier() == "ALTIMETER_ROCKET_RAVEN"


class TestAltArmStatus:
    def test_basic(self):
        # timestamp=1000, alt_id=ALTIMETER_ROCKET_RAVEN (0x00), arm_state=ARMED (0x01),
        # drogue_v=0x0064 (100), main_v=0x00C8 (200)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01, 0x00, 0x64, 0x00, 0xC8)
        result = ALT_ARM_STATUS.from_bitstring(bs)
        assert result.time == 1.0
        assert result.alt_id == "ALTIMETER_ROCKET_RAVEN"
        assert result.alt_arm_state == "ALT_ARM_STATE_ARMED"
        assert result.drogue_v == 100
        assert result.main_v == 200


class TestSensorAltitude:
    def test_basic(self):
        # timestamp=1000, altitude=1000 (0x000003E8), apogee_state=APOGEE_NOT_REACHED (0x01)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x03, 0xE8, 0x01)
        result = SENSOR_ALTITUDE.from_bitstring(bs)
        assert result.time == 1.0
        assert result.altitude == 1000
        assert result.apogee_state == "APOGEE_NOT_REACHED"

    def test_negative_altitude(self):
        # timestamp=1000, altitude=-1 (0xFFFFFFFF signed), apogee_state=APOGEE_UNKNOWN (0x00)
        bs = _make_bitstring(0x03, 0xE8, 0xFF, 0xFF, 0xFF, 0xFF, 0x00)
        result = SENSOR_ALTITUDE.from_bitstring(bs)
        assert result.altitude == -1


class TestSensorImu:
    def test_basic(self):
        # timestamp=1000, imu_id=IMU_PROC_ALTIMU10 (0x00), linear_accel=100, angular_velocity=200
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x00, 0x64, 0x00, 0xC8)
        result = SENSOR_IMU.from_bitstring(bs)
        assert result.time == 1.0
        assert result.imu_id == "IMU_PROC_ALTIMU10"
        assert result.linear_accel == 100
        assert result.angular_velocity == 200
        assert result.get_identifier() == "IMU_PROC_ALTIMU10"


class TestSensorMag:
    def test_basic(self):
        # timestamp=1000, imu_id=IMU_PROC_MTI630 (0x01), mag=42
        bs = _make_bitstring(0x03, 0xE8, 0x01, 0x00, 0x2A)
        result = SENSOR_MAG.from_bitstring(bs)
        assert result.time == 1.0
        assert result.imu_id == "IMU_PROC_MTI630"
        assert result.mag == 42


class TestSensorBaro:
    def test_basic(self):
        # timestamp=1000, imu_id=IMU_PROC_ALTIMU10 (0x00), pressure=0x0186A0 (100000), temp=0x0019 (25)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01, 0x86, 0xA0, 0x00, 0x19)
        result = SENSOR_BARO.from_bitstring(bs)
        assert result.time == 1.0
        assert result.imu_id == "IMU_PROC_ALTIMU10"
        assert result.pressure == 100000
        assert result.temp == 25


class TestSensorAnalog:
    def test_basic(self):
        # timestamp=1000, sensor_id=SENSOR_5V_VOLT (0x00), value=0x0FFF (4095)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x0F, 0xFF)
        result = SENSOR_ANALOG.from_bitstring(bs)
        assert result.time == 1.0
        assert result.sensor_id == "SENSOR_5V_VOLT"
        assert result.value == 4095
        assert result.get_identifier() == "SENSOR_5V_VOLT"


class TestGpsTimestamp:
    def test_basic(self):
        # timestamp=1000, hrs=12, mins=30, secs=45, dsecs=5
        bs = _make_bitstring(0x03, 0xE8, 12, 30, 45, 5)
        result = GPS_TIMESTAMP.from_bitstring(bs)
        assert result.time == 1.0
        assert result.hrs == 12
        assert result.mins == 30
        assert result.secs == 45
        assert result.dsecs == 5
        assert result.get_identifier() is None


class TestGpsLatitude:
    def test_basic(self):
        # timestamp=1000, degs=43, mins=28, dmins=0x1234, direction='N'
        bs = _make_bitstring(0x03, 0xE8, 43, 28, 0x12, 0x34, ord('N'))
        result = GPS_LATITUDE.from_bitstring(bs)
        assert result.time == 1.0
        assert result.degs == 43
        assert result.mins == 28
        assert result.dmins == 0x1234
        assert result.direction == "N"


class TestGpsLongitude:
    def test_basic(self):
        # timestamp=1000, degs=80, mins=31, dmins=0x5678, direction='W'
        bs = _make_bitstring(0x03, 0xE8, 80, 31, 0x56, 0x78, ord('W'))
        result = GPS_LONGITUDE.from_bitstring(bs)
        assert result.time == 1.0
        assert result.degs == 80
        assert result.mins == 31
        assert result.dmins == 0x5678
        assert result.direction == "W"


class TestGpsAltitude:
    def test_basic(self):
        # timestamp=1000, altitude=0x0064 (100), daltitude=0x05 (5), unit='m'
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x64, 0x05, ord('m'))
        result = GPS_ALTITUDE.from_bitstring(bs)
        assert result.time == 1.0
        assert result.altitude == 100
        assert result.daltitude == 5
        assert result.unit == "m"


class TestGpsInfo:
    def test_basic(self):
        # timestamp=1000, num_sats=8, quality=1
        bs = _make_bitstring(0x03, 0xE8, 8, 1)
        result = GPS_INFO.from_bitstring(bs)
        assert result.time == 1.0
        assert result.num_sats == 8
        assert result.quality == 1


class TestStateEstData:
    def test_basic(self):
        # timestamp=1000, state_id=STATE_ID_ALT (0x0A), data=9.8125 (IEEE 754 big-endian)
        float_bytes = struct.pack('>f', 9.8125)
        bs = _make_bitstring(0x03, 0xE8, 0x0A, *float_bytes)
        result = STATE_EST_DATA.from_bitstring(bs)
        assert result.time == 1.0
        assert result.state_id == "STATE_ID_ALT"
        assert result.data == pytest.approx(9.8125)
        assert result.get_identifier() == "STATE_ID_ALT"


class TestStreamStatus:
    def test_basic(self):
        # timestamp=1000, total_size=0x000100 (256), tx_size=0x000080 (128)
        bs = _make_bitstring(0x03, 0xE8, 0x00, 0x01, 0x00, 0x00, 0x00, 0x80)
        result = STREAM_STATUS.from_bitstring(bs)
        assert result.time == 1.0
        assert result.total_size == 256
        assert result.tx_size == 128


class TestStreamData:
    def test_basic(self):
        # timestamp=1000, seq_id=1, data="Hello" (5 bytes = 40 bits)
        bs = _make_bitstring(0x03, 0xE8, 0x01, 0x48, 0x65, 0x6C, 0x6C, 0x6F)
        result = STREAM_DATA.from_bitstring(bs)
        assert result.time == 1.0
        assert result.seq_id == 1
        assert result.data == "Hello"


class TestStreamRetry:
    def test_basic(self):
        # timestamp=1000, seq_id=5
        bs = _make_bitstring(0x03, 0xE8, 0x05)
        result = STREAM_RETRY.from_bitstring(bs)
        assert result.time == 1.0
        assert result.seq_id == 5
        assert result.get_identifier() is None


class TestPayloadInterface:
    """Test that all payload types properly implement the ParsleyDataPayload interface."""

    def test_all_types_are_subclasses(self):
        payload_classes = [
            GENERAL_BOARD_STATUS, RESET_CMD, DEBUG_RAW, CONFIG_SET, CONFIG_STATUS,
            ACTUATOR_CMD, ACTUATOR_ANALOG_CMD, ACTUATOR_STATUS,
            ALT_ARM_CMD, ALT_ARM_STATUS,
            SENSOR_ALTITUDE, SENSOR_IMU, SENSOR_MAG, SENSOR_BARO, SENSOR_ANALOG,
            GPS_TIMESTAMP, GPS_LATITUDE, GPS_LONGITUDE, GPS_ALTITUDE, GPS_INFO,
            STATE_EST_DATA, STREAM_STATUS, STREAM_DATA, STREAM_RETRY,
        ]
        for cls in payload_classes:
            assert issubclass(cls, ParsleyDataPayload), f"{cls.__name__} is not a subclass of ParsleyDataPayload"


class TestRoundTrip:
    """Test that from_bitstring correctly consumes all bits from the BitString."""

    def test_actuator_cmd_consumes_all_bits(self):
        # 2 bytes timestamp + 1 byte actuator + 1 byte state = 4 bytes = 32 bits
        bs = BitString(b'\x03\xE8\x00\x00', 32)
        result = ACTUATOR_CMD.from_bitstring(bs)
        assert bs.length == 0  # all bits should be consumed

    def test_gps_info_consumes_all_bits(self):
        # 2 bytes timestamp + 1 byte num_sats + 1 byte quality = 4 bytes = 32 bits
        bs = BitString(b'\x03\xE8\x08\x01', 32)
        result = GPS_INFO.from_bitstring(bs)
        assert bs.length == 0

    def test_stream_retry_consumes_all_bits(self):
        # 2 bytes timestamp + 1 byte seq_id = 3 bytes = 24 bits
        bs = BitString(b'\x03\xE8\x05', 24)
        result = STREAM_RETRY.from_bitstring(bs)
        assert bs.length == 0
