import pytest
import parsley
 
from pytest import approx
from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric, Floating, Bitfield
from parsley.message_definitions import TIMESTAMP_2, MESSAGES

import parsley.message_types as mt

class TestCANMessage:
    """
    We are testing only the message body of CAN messages, which means that BitString won't contain
    a message_sid (ie. message_type | board_id where '|' represents bitwise OR)
    """

    @pytest.fixture()
    def bit_str2(self):
        bit_str2 = BitString()
        bit_str2.push(*TIMESTAMP_2.encode(3))
        return bit_str2

    
    def test_general_board_status(self, bit_str2):
        # 0b [...(32) 1011] [...(16)] 
        bit_str2.push(b"\x00\x00\x00\x0B" + b"\x00\x00", 48)
        res = parsley.parse_fields(bit_str2, MESSAGES["GENERAL_BOARD_STATUS"][3:]) # [3:] to skip prio, type, inst
        assert res["general_board_status"] == 'E_5V_OVER_CURRENT|E_5V_OVER_VOLTAGE|E_12V_OVER_CURRENT'
        assert res["board_error_bitfield"] == 'E_NOMINAL'

    def test_reset_cmd(self, bit_str2):
        bit_str2.push(b"\x0A\x00", 16) # 0x0A (ALTIMETER), 0x00 (ANY)
        res = parsley.parse_fields(bit_str2, MESSAGES["RESET_CMD"][3:])

        assert res["board_type_id"] == 'ALTIMETER'
        assert res["board_inst_id"] == 'ANY'

    def test_debug_raw(self, bit_str2):
        bit_str2.push(b"rawmsg", 48)
        res = parsley.parse_fields(bit_str2, MESSAGES["DEBUG_RAW"][3:])

        assert res["string"] == "rawmsg"

    def test_config_set(self, bit_str2):
        # 0x01 (INJ_SENSOR), 0x02 (ROCKET), 0x0304 (ID), 0x0506 (Value)
        bit_str2.push(b"\x01\x02\x03\x04\x05\x06", 48)
        res = parsley.parse_fields(bit_str2, MESSAGES["CONFIG_SET"][3:])

        assert res["board_type_id"] == 'INJ_SENSOR'
        assert res["board_inst_id"] == 'ROCKET'
        assert res["config_id"] == 0x0304
        assert res["config_value"] == 0x0506

    def test_config_status(self, bit_str2):
        # 0x1122 (ID), 0x3344 (Value)
        bit_str2.push(b"\x11\x22\x33\x44", 32)
        res = parsley.parse_fields(bit_str2, MESSAGES["CONFIG_STATUS"][3:])

        assert res["config_id"] == 0x1122
        assert res["config_value"] == 0x3344

    def test_actuator_cmd(self, bit_str2):
        # 0x00 (ACTUATOR_OX_INJECTOR_VALVE), 0x00 (ACT_STATE_ON)
        bit_str2.push(b"\x00\x00", 16)
        res = parsley.parse_fields(bit_str2, MESSAGES["ACTUATOR_CMD"][3:])

        assert res["actuator"] == "ACTUATOR_OX_INJECTOR_VALVE"
        assert res["cmd_state"] == "ACT_STATE_ON"

    def test_actuator_analog_cmd(self, bit_str2):
        # 0x11 (ACTUATOR_CANARD_ANGLE), 0x0100 (cmd_state=256)
        bit_str2.push(b"\x11\x01\x00", 24)
        res = parsley.parse_fields(bit_str2, MESSAGES["ACTUATOR_ANALOG_CMD"][3:])

        assert res["actuator"] == "ACTUATOR_CANARD_ANGLE"
        assert res["cmd_state"] == 256

    def test_actuator_status(self, bit_str2):
        # 0x01 (ACTUATOR_FUEL_INJECTOR_VALVE), 0x00 (curr_state=ON), 0x01 (cmd_state=OFF)
        bit_str2.push(b"\x01\x00\x01", 24)
        res = parsley.parse_fields(bit_str2, MESSAGES["ACTUATOR_STATUS"][3:])

        assert res["actuator"] == "ACTUATOR_FUEL_INJECTOR_VALVE"
        assert res["curr_state"] == "ACT_STATE_ON"
        assert res["cmd_state"] == "ACT_STATE_OFF"

    def test_alt_arm_cmd(self, bit_str2):
        # 0x02 (ALTIMETER_ROCKET_SRAD), 0x01 (ALT_ARM_STATE_ARMED)
        bit_str2.push(b"\x02\x01", 16)
        res = parsley.parse_fields(bit_str2, MESSAGES["ALT_ARM_CMD"][3:])

        assert res["alt_id"] == "ALTIMETER_ROCKET_SRAD"
        assert res["alt_arm_state"] == "ALT_ARM_STATE_ARMED"

    def test_alt_arm_status(self, bit_str2):
        # 0x00 (ALTIMETER_ROCKET_RAVEN), 0x01 (ARMED), 0x0500 (drogue=1280), 0x0A00 (main=2560)
        bit_str2.push(b"\x00\x01\x05\x00\x0A\x00", 48)
        res = parsley.parse_fields(bit_str2, MESSAGES["ALT_ARM_STATUS"][3:])

        assert res["alt_id"] == "ALTIMETER_ROCKET_RAVEN"
        assert res["alt_arm_state"] == "ALT_ARM_STATE_ARMED"
        assert res["drogue_v"] == 1280
        assert res["main_v"] == 2560

    def test_stream_status(self, bit_str2):
        # total_size 0x000A1B (2587), tx_size 0x000005 (5)
        bit_str2.push(b"\x00\x0A\x1B\x00\x00\x05", 48)
        res = parsley.parse_fields(bit_str2, MESSAGES["STREAM_STATUS"][3:])

        assert res["total_size"] == 2587
        assert res["tx_size"] == 5
    
    def test_stream_data(self, bit_str2):
        # seq_id 0x12 (18), data "cools"
        # push seq_id first (8 bits) then the 40-bit ASCII field (5 bytes)
        bit_str2.push(b"\x12", 8)
        bit_str2.push(b"cools", 40)
        res = parsley.parse_fields(bit_str2, MESSAGES["STREAM_DATA"][3:])

        assert res["seq_id"] == 18
        assert res["data"] == "cools"
        
    def test_stream_retry(self, bit_str2):
        # seq_id 0x34 (52)
        bit_str2.push(b"\x34", 8)
        res = parsley.parse_fields(bit_str2, MESSAGES["STREAM_RETRY"][3:])

        assert res["seq_id"] == 52

    def test_sensor_altitude(self, bit_str2):
        # Altitude 3000m (0x00000BB8), APOGEE_NOT_REACHED (0x01)
        bit_str2.push(b"\x00\x00\x0B\xB8\x01", 40)
        res = parsley.parse_fields(bit_str2, MESSAGES["SENSOR_ALTITUDE"][3:])

        assert res["altitude"] == 3000
        assert res["apogee_state"] == "APOGEE_NOT_REACHED"

    def test_sensor_imu_x(self, bit_str2):
        # 0x01 (IMU_PROC_MTI630), linear_accel 1024 (0x0400), angular_velocity 512 (0x0200)
        bit_str2.push(b"\x01\x04\x00\x02\x00", 40)
        res = parsley.parse_fields(bit_str2, MESSAGES["SENSOR_IMU_X"][3:])

        assert res["imu_id"] == "IMU_PROC_MTI630"
        assert res["linear_accel"] == 1024
        assert res["angular_velocity"] == 512

    def test_sensor_mag_x(self, bit_str2):
        # 0x00 (IMU_PROC_ALTIMU10), mag 1000 (0x03E8)
        bit_str2.push(b"\x00\x03\xE8", 24)
        res = parsley.parse_fields(bit_str2, MESSAGES["SENSOR_MAG_X"][3:])

        assert res["imu_id"] == "IMU_PROC_ALTIMU10"
        assert res["mag"] == 1000

    def test_sensor_baro(self, bit_str2):
        # 0x00 (IMU_PROC_ALTIMU10), pressure 101325 (0x018B6D), temp 298 (0x012A)
        bit_str2.push(b"\x00\x01\x8B\x6D\x01\x2A", 48) # imu_id, pressure, temp
        res = parsley.parse_fields(bit_str2, MESSAGES["SENSOR_BARO"][3:])

        assert res["imu_id"] == "IMU_PROC_ALTIMU10"
        assert res["pressure"] == 101229
        assert res["temp"] == 298

    def test_sensor_analog(self, bit_str2):
        # 0x07 (SENSOR_BATT_CURR), value 1000 (0x03E8)
        bit_str2.push(b"\x07\x03\xE8", 24)
        res = parsley.parse_fields(bit_str2, MESSAGES["SENSOR_ANALOG"][3:])

        assert res["sensor_id"] == "SENSOR_BATT_CURR"
        assert res["value"] == 1000

    def test_gps_timestamp(self, bit_str2):
        # 10 hrs (0x0A), 30 mins (0x1E), 59 secs (0x3B), 99 dsecs (0x63) -> 10:30:59.99
        bit_str2.push(b"\x0A\x1E\x3B\x63", 32)
        res = parsley.parse_fields(bit_str2, MESSAGES["GPS_TIMESTAMP"][3:])

        assert res["hrs"] == 10
        assert res["mins"] == 30
        assert res["secs"] == 59
        assert res["dsecs"] == 99

    def test_gps_latitude(self, bit_str2):
        # 43 degs (0x2B), 28 mins (0x1C), 1234 dmins (0x04D2), 'N' (0x4E)
        bit_str2.push(b"\x2B\x1C\x04\xD2\x4E", 40)
        res = parsley.parse_fields(bit_str2, MESSAGES["GPS_LATITUDE"][3:])

        assert res["degs"] == 43
        assert res["mins"] == 28
        assert res["dmins"] == 1234
        assert res["direction"] == 'N'

    def test_gps_longitude(self, bit_str2):
        # 79 degs (0x4F), 59 mins (0x3B), 5678 dmins (0x162E), 'W' (0x57)
        bit_str2.push(b"\x4F\x3B\x16\x2E\x57", 40)
        res = parsley.parse_fields(bit_str2, MESSAGES["GPS_LONGITUDE"][3:])

        assert res["degs"] == 79
        assert res["mins"] == 59
        assert res["dmins"] == 5678
        assert res["direction"] == 'W'

    def test_gps_altitude(self, bit_str2):
        # altitude 500 (0x01F4), daltitude 25 (0x19), 'M' (0x4D) -> 500.25 M
        bit_str2.push(b"\x01\xF4\x19\x4D", 32)
        res = parsley.parse_fields(bit_str2, MESSAGES["GPS_ALTITUDE"][3:])

        assert res["altitude"] == 500
        assert res["daltitude"] == 25
        assert res["unit"] == 'M'

    def test_gps_info(self, bit_str2):
        bit_str2.push(b"\x05\x02", 16) # 5 sats, quality 2
        res = parsley.parse_fields(bit_str2, MESSAGES["GPS_INFO"][3:])

        assert res["num_sats"] == 5
        assert res["quality"] == 2

    def test_state_est_data(self, bit_str2):
        # 0x0A (STATE_ID_ALT), data 123.45 (approx 0x42F6E666 float)
        bit_str2.push(b"\x0A\x42\xF6\xE6\x66", 40)
        res = parsley.parse_fields(bit_str2, MESSAGES["STATE_EST_DATA"][3:])

        assert res["state_id"] == "STATE_ID_ALT"
        assert res["data"] == approx(123.45, abs=1e-3)

    def test_leds_on(self, bit_str2):
        res = parsley.parse_fields(bit_str2, [])
        assert res == {}
