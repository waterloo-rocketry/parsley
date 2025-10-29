import pytest
import parsley

from pytest import approx
from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric, Floating, Bitfield
from parsley.message_definitions import TIMESTAMP_2, MESSAGES

import parsley.message_types as mt
import test_utils as tu

class TestCANMessage:
    """
    We are testing only the message body of CAN messages, which means that BitString won't contain
    a message_sid (ie. message_type | board_id where '|' represents bitwise OR)
    """

    @pytest.fixture()
    def bit_str2(self):
        bit_str2 = BitString()
        # TIMESTAMP_2 is the first field in the fields list, so it needs to be pushed first.
        # It reads raw data in milliseconds and outputs seconds (scale=1/1000).
        bit_str2.push(*TIMESTAMP_2.encode(3))
        return bit_str2

    
    def test1_general_board_status(self, bit_str2):
        # 0b [...(32) 1011] [...(16)] 
        bit_str2.push(b"\x00\x00\x00\x0B" + b"\x00\x00", 48) # 0x0B = 00001011
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                    Bitfield("general_board_status", 32, "E_NOMINAL", mt.general_board_status_offset),
                    Bitfield("board_error_bitfield", 16, "E_NOMINAL", mt.board_specific_status_offset)])

        assert res["general_board_status"] == 'E_5V_OVER_CURRENT|E_5V_OVER_VOLTAGE|E_12V_OVER_CURRENT'
        assert res["board_error_bitfield"] == 'E_NOMINAL'

    def test2_general_board_status(self, bit_str2):
        # 0b [...(32) 10100101] [...(16) 0111] 
        bit_str2.push(b"\x00\x00\x00\xA5" + b"\x00\x07", 48) # 0xA5 = 10100101. 0x07 = 0000000000000111
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                    Bitfield("general_board_status", 32, "E_NOMINAL", mt.general_board_status_offset),
                    Bitfield("board_error_bitfield", 16, "E_NOMINAL", mt.board_specific_status_offset)])

        # E_5V_OVER_CURRENT(0)|E_5V_UNDER_VOLTAGE(2)|E_12V_UNDER_VOLTAGE(5)|E_BATT_OVER_VOLTAGE(7)
        assert res["general_board_status"] == 'E_5V_OVER_CURRENT|E_5V_UNDER_VOLTAGE|E_12V_UNDER_VOLTAGE|E_BATT_OVER_VOLTAGE'
        # E_12V_EFUSE_FAULT(0)|E_5V_EFUSE_FAULT(1)|E_PT_OUT_OF_RANGE(2)
        assert res["board_error_bitfield"] == 'E_12V_EFUSE_FAULT|E_5V_EFUSE_FAULT|E_PT_OUT_OF_RANGE'

    # --- RESET_CMD Tests ---
    def test1_reset_cmd(self, bit_str2):
        bit_str2.push(b"\x0A\x00", 16) # 0x0A (ALTIMETER), 0x00 (ANY)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                    Enum("board_type_id", 8, mt.board_type_id),
                    Enum("board_inst_id", 8, mt.board_inst_id)])

        assert res["board_type_id"] == 'ALTIMETER'
        assert res["board_inst_id"] == 'ANY'

    def test2_reset_cmd(self, bit_str2):
        bit_str2.push(b"\x82\x08", 16) # 0x82 (DAQ), 0x08 (RECOVERY)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                    Enum("board_type_id", 8, mt.board_type_id),
                    Enum("board_inst_id", 8, mt.board_inst_id)])

        assert res["board_type_id"] == 'DAQ'
        assert res["board_inst_id"] == 'RECOVERY'

    # --- DEBUG_RAW Tests ---
    def test1_debug_raw(self, bit_str2):
        bit_str2.push(b"rawmsg", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     ASCII('string', 48)])

        assert res["string"] == "rawmsg"

    def test2_debug_raw(self, bit_str2):
        bit_str2.push(b"\n 1.${", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     ASCII('string', 48)])

        assert res["string"] == "\n 1.${"

    # --- CONFIG_SET Tests (Fixed Assertions) ---
    def test1_config_set(self, bit_str2):
        # 0x01 (INJ_SENSOR), 0x02 (ROCKET), 0x0304 (ID), 0x0506 (Value)
        bit_str2.push(b"\x01\x02\x03\x04\x05\x06", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("board_type_id", 8, mt.board_type_id),
                     Enum("board_inst_id", 8, mt.board_inst_id),
                     Numeric("config_id", 16),
                     Numeric("config_value", 16)])

        assert res["board_type_id"] == 'INJ_SENSOR'
        assert res["board_inst_id"] == 'ROCKET'
        assert res["config_id"] == 0x0304
        assert res["config_value"] == 0x0506
        
    def test2_config_set(self, bit_str2):
        # 0x80 (RLCS_GLS), 0x01 (GROUND), 0xABCD (ID), 0xEF00 (Value)
        bit_str2.push(b"\x80\x01\xAB\xCD\xEF\x00", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("board_type_id", 8, mt.board_type_id),
                     Enum("board_inst_id", 8, mt.board_inst_id),
                     Numeric("config_id", 16),
                     Numeric("config_value", 16)])

        assert res["board_type_id"] == 'RLCS_GLS'
        assert res["board_inst_id"] == 'GROUND'
        assert res["config_id"] == 0xABCD
        assert res["config_value"] == 0xEF00

    # --- CONFIG_STATUS Tests ---
    def test1_config_status(self, bit_str2):
        # 0x1122 (ID), 0x3344 (Value)
        bit_str2.push(b"\x11\x22\x33\x44", 32)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("config_id", 16),
                     Numeric("config_value", 16)])

        assert res["config_id"] == 0x1122
        assert res["config_value"] == 0x3344

    def test2_config_status(self, bit_str2):
        # 0xEEFF (ID), 0xAABB (Value)
        bit_str2.push(b"\xEE\xFF\xAA\xBB", 32)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("config_id", 16),
                     Numeric("config_value", 16)])

        assert res["config_id"] == 0xEEFF
        assert res["config_value"] == 0xAABB

    # --- ACTUATOR_CMD Tests ---
    def test1_actuator_cmd(self, bit_str2):
        # 0x00 (ACTUATOR_OX_INJECTOR_VALVE), 0x00 (ACT_STATE_ON)
        bit_str2.push(b"\x00\x00", 16)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("actuator", 8, mt.actuator_id),
                     Enum("cmd_state", 8, mt.actuator_state)])

        assert res["actuator"] == "ACTUATOR_OX_INJECTOR_VALVE"
        assert res["cmd_state"] == "ACT_STATE_ON"

    def test2_actuator_cmd(self, bit_str2):
        # 0x0C (ACTUATOR_CAMERA_PAYLOAD), 0x01 (ACT_STATE_OFF)
        bit_str2.push(b"\x0C\x01", 16)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("actuator", 8, mt.actuator_id),
                     Enum("cmd_state", 8, mt.actuator_state)])

        assert res["actuator"] == "ACTUATOR_CAMERA_PAYLOAD"
        assert res["cmd_state"] == "ACT_STATE_OFF"

    # --- ACTUATOR_ANALOG_CMD Tests ---
    def test1_actuator_analog_cmd(self, bit_str2):
        # 0x11 (ACTUATOR_CANARD_ANGLE), 0x0100 (cmd_state=256)
        bit_str2.push(b"\x11\x01\x00", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("actuator", 8, mt.actuator_id),
                     Numeric("cmd_state", 16)])

        assert res["actuator"] == "ACTUATOR_CANARD_ANGLE"
        assert res["cmd_state"] == 256

    def test2_actuator_analog_cmd(self, bit_str2):
        # 0x10 (ACTUATOR_CANARD_ENABLE), 0xFFFE (cmd_state=65534)
        bit_str2.push(b"\x10\xFF\xFE", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("actuator", 8, mt.actuator_id),
                     Numeric("cmd_state", 16)])

        assert res["actuator"] == "ACTUATOR_CANARD_ENABLE"
        assert res["cmd_state"] == 65534

    # --- ACTUATOR_STATUS Tests ---
    def test1_actuator_status(self, bit_str2):
        # 0x01 (ACTUATOR_FUEL_INJECTOR_VALVE), 0x00 (curr_state=ON), 0x01 (cmd_state=OFF)
        bit_str2.push(b"\x01\x00\x01", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("actuator", 8, mt.actuator_id),
                     Enum("curr_state", 8, mt.actuator_state),
                     Enum("cmd_state", 8, mt.actuator_state)])

        assert res["actuator"] == "ACTUATOR_FUEL_INJECTOR_VALVE"
        assert res["curr_state"] == "ACT_STATE_ON"
        assert res["cmd_state"] == "ACT_STATE_OFF"

    def test2_actuator_status(self, bit_str2):
        # 0x08 (ACTUATOR_TELEMETRY), 0x03 (curr_state=ILLEGAL), 0x02 (cmd_state=UNK)
        bit_str2.push(b"\x08\x03\x02", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("actuator", 8, mt.actuator_id),
                     Enum("curr_state", 8, mt.actuator_state),
                     Enum("cmd_state", 8, mt.actuator_state)])

        assert res["actuator"] == "ACTUATOR_TELEMETRY"
        assert res["curr_state"] == "ACT_STATE_ILLEGAL"
        assert res["cmd_state"] == "ACT_STATE_UNK"

    # --- ALT_ARM_CMD Tests ---
    def test1_alt_arm_cmd(self, bit_str2):
        # 0x02 (ALTIMETER_ROCKET_SRAD), 0x01 (ALT_ARM_STATE_ARMED)
        bit_str2.push(b"\x02\x01", 16)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("alt_id", 8, mt.altimeter_id),
                     Enum("alt_arm_state", 8, mt.alt_arm_state)])

        assert res["alt_id"] == "ALTIMETER_ROCKET_SRAD"
        assert res["alt_arm_state"] == "ALT_ARM_STATE_ARMED"

    def test2_alt_arm_cmd(self, bit_str2):
        # 0x04 (ALTIMETER_PAYLOAD_STRATOLOGGER), 0x00 (ALT_ARM_STATE_DISARMED)
        bit_str2.push(b"\x04\x00", 16)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("alt_id", 8, mt.altimeter_id),
                     Enum("alt_arm_state", 8, mt.alt_arm_state)])

        assert res["alt_id"] == "ALTIMETER_PAYLOAD_STRATOLOGGER"
        assert res["alt_arm_state"] == "ALT_ARM_STATE_DISARMED"

    # --- ALT_ARM_STATUS Tests ---
    def test1_alt_arm_status(self, bit_str2):
        # 0x00 (ALTIMETER_ROCKET_RAVEN), 0x01 (ARMED), 0x0500 (drogue=1280), 0x0A00 (main=2560)
        bit_str2.push(b"\x00\x01\x05\x00\x0A\x00", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("alt_id", 8, mt.altimeter_id),
                     Enum("alt_arm_state", 8, mt.alt_arm_state),
                     Numeric("drogue_v", 16),
                     Numeric("main_v", 16)])

        assert res["alt_id"] == "ALTIMETER_ROCKET_RAVEN"
        assert res["alt_arm_state"] == "ALT_ARM_STATE_ARMED"
        assert res["drogue_v"] == 1280
        assert res["main_v"] == 2560

    def test2_alt_arm_status(self, bit_str2):
        # 0x03 (ALTIMETER_PAYLOAD_RAVEN), 0x00 (DISARMED), 0x0000 (drogue=0), 0xFFFF (main=65535)
        bit_str2.push(b"\x03\x00\x00\x00\xFF\xFF", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum("alt_id", 8, mt.altimeter_id),
                     Enum("alt_arm_state", 8, mt.alt_arm_state),
                     Numeric("drogue_v", 16),
                     Numeric("main_v", 16)])

        assert res["alt_id"] == "ALTIMETER_PAYLOAD_RAVEN"
        assert res["alt_arm_state"] == "ALT_ARM_STATE_DISARMED"
        assert res["drogue_v"] == 0
        assert res["main_v"] == 65535

    # --- SENSOR_TEMP Tests (Fixed Data/Assertions) ---
    def test1_sensor_temp(self, bit_str2):
        # ID 1 (0x01), Temperature -128.0°C. Raw value for -128.0 * 1024 = -131072 = 0xFFFE0000 (signed 32-bit)
        bit_str2.push(b"\x01\xFF\xFE\x00\x00", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("temp_sensor_id", 8),
                     Numeric("temperature", 32, scale=1/2**10, unit='°C', signed=True)])

        assert res["temp_sensor_id"] == 1
        assert res["temperature"] == -128.0

    def test2_sensor_temp(self, bit_str2):
        # ID 2 (0x02), Temperature 25.0°C. Raw value for 25.0 * 1024 = 25600 = 0x00006400
        bit_str2.push(b"\x02\x00\x00\x64\x00", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("temp_sensor_id", 8),
                     Numeric("temperature", 32, scale=1/2**10, unit='°C', signed=True)])

        assert res["temp_sensor_id"] == 2
        assert res["temperature"] == 25.0

    # --- SENSOR_ALTITUDE Tests ---
    def test1_sensor_altitude(self, bit_str2):
        # Altitude 3000m (0x00000BB8), APOGEE_NOT_REACHED (0x01)
        bit_str2.push(b"\x00\x00\x0B\xB8\x01", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("altitude", 32, signed=True),
                     Enum("apogee_state", 8, mt.apogee_state)])

        assert res["altitude"] == 3000
        assert res["apogee_state"] == "APOGEE_NOT_REACHED"

    def test2_sensor_altitude(self, bit_str2):
        # Altitude -500m (0xFFFFFE0C), APOGEE_REACHED (0x02)
        bit_str2.push(b"\xFF\xFF\xFE\x0C\x02", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("altitude", 32, signed=True),
                     Enum("apogee_state", 8, mt.apogee_state)])

        assert res["altitude"] == -500
        assert res["apogee_state"] == "APOGEE_REACHED"

    # --- SENSOR_IMU_X Tests ---
    def test1_sensor_imu_x(self, bit_str2):
        # 0x01 (IMU_PROC_MTI630), linear_accel 1024 (0x0400), angular_velocity 512 (0x0200)
        bit_str2.push(b"\x01\x04\x00\x02\x00", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                     Enum('imu_id', 8, mt.imu_id), 
                     Numeric('linear_accel', 16), 
                     Numeric('angular_velocity', 16)])

        assert res["imu_id"] == "IMU_PROC_MTI630"
        assert res["linear_accel"] == 1024
        assert res["angular_velocity"] == 512

    def test2_sensor_imu_y(self, bit_str2):
        # 0x03 (IMU_SRAD_ALT_ALTIMU10), linear_accel 65535 (0xFFFF), angular_velocity 0 (0x0000)
        # Note: Testing SENSOR_IMU_Y with the same payload structure
        bit_str2.push(b"\x03\xFF\xFF\x00\x00", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                     Enum('imu_id', 8, mt.imu_id), 
                     Numeric('linear_accel', 16), 
                     Numeric('angular_velocity', 16)])

        assert res["imu_id"] == "IMU_SRAD_ALT_ALTIMU10"
        assert res["linear_accel"] == 65535
        assert res["angular_velocity"] == 0

    # --- SENSOR_MAG_X Tests ---
    def test1_sensor_mag_x(self, bit_str2):
        # 0x00 (IMU_PROC_ALTIMU10), mag 1000 (0x03E8)
        bit_str2.push(b"\x00\x03\xE8", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                     Enum('imu_id', 8, mt.imu_id), 
                     Numeric('mag', 16)])

        assert res["imu_id"] == "IMU_PROC_ALTIMU10"
        assert res["mag"] == 1000

    def test2_sensor_mag_y(self, bit_str2):
        # 0x02 (IMU_PROC_LSM6DSO32), mag 40000 (0x9C40)
        # Note: Testing SENSOR_MAG_Y with the same payload structure
        bit_str2.push(b"\x02\x9C\x40", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                     Enum('imu_id', 8, mt.imu_id), 
                     Numeric('mag', 16)])

        assert res["imu_id"] == "IMU_PROC_LSM6DSO32"
        assert res["mag"] == 40000

    # --- SENSOR_BARO Tests ---
    def test1_sensor_baro(self, bit_str2):
        # 0x00 (IMU_PROC_ALTIMU10), pressure 101325 (0x018B6D), temp 298 (0x012A)
        bit_str2.push(b"\x00\x01\x8B\x6D\x01\x2A", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                     Enum('imu_id', 8, mt.imu_id), 
                     Numeric('pressure', 24), 
                     Numeric('temp', 16)])

        assert res["imu_id"] == "IMU_PROC_ALTIMU10"
        assert res["pressure"] == 101229
        assert res["temp"] == 298

    def test2_sensor_baro(self, bit_str2):
        # 0x03 (IMU_SRAD_ALT_ALTIMU10), pressure 50000 (0x00C350), temp 350 (0x015E)
        bit_str2.push(b"\x03\x00\xC3\x50\x01\x5E", 48)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2, 
                     Enum('imu_id', 8, mt.imu_id), 
                     Numeric('pressure', 24), 
                     Numeric('temp', 16)])

        assert res["imu_id"] == "IMU_SRAD_ALT_ALTIMU10"
        assert res["pressure"] == 50000
        assert res["temp"] == 350

    # --- SENSOR_ANALOG Tests ---
    def test1_sensor_analog(self, bit_str2):
        # 0x07 (SENSOR_BATT_CURR), value 1000 (0x03E8)
        bit_str2.push(b"\x07\x03\xE8", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum('sensor_id', 8, mt.analog_sensor_id), 
                     Numeric('value', 16)])

        assert res["sensor_id"] == "SENSOR_BATT_CURR"
        assert res["value"] == 1000

    def test2_sensor_analog(self, bit_str2):
        # 0x0F (SENSOR_PT_CHANNEL_3), value 65535 (0xFFFF)
        bit_str2.push(b"\x0F\xFF\xFF", 24)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum('sensor_id', 8, mt.analog_sensor_id), 
                     Numeric('value', 16)])

        assert res["sensor_id"] == "SENSOR_PT_CHANNEL_3"
        assert res["value"] == 65535

    # --- GPS_TIMESTAMP Tests ---
    def test1_gps_timestamp(self, bit_str2):
        # 10 hrs (0x0A), 30 mins (0x1E), 59 secs (0x3B), 99 dsecs (0x63) -> 10:30:59.99
        bit_str2.push(b"\x0A\x1E\x3B\x63", 32)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('hrs', 8), 
                     Numeric('mins', 8), 
                     Numeric('secs', 8), 
                     Numeric('dsecs', 8)])

        assert res["hrs"] == 10
        assert res["mins"] == 30
        assert res["secs"] == 59
        assert res["dsecs"] == 99

    def test2_gps_timestamp(self, bit_str2):
        # 0 hrs (0x00), 0 mins (0x00), 0 secs (0x00), 0 dsecs (0x00) -> 00:00:00.00
        bit_str2.push(b"\x00\x00\x00\x00", 32)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('hrs', 8), 
                     Numeric('mins', 8), 
                     Numeric('secs', 8), 
                     Numeric('dsecs', 8)])

        assert res["hrs"] == 0
        assert res["mins"] == 0
        assert res["secs"] == 0
        assert res["dsecs"] == 0

    # --- GPS_LATITUDE Tests ---
    def test1_gps_latitude(self, bit_str2):
        # 43 degs (0x2B), 28 mins (0x1C), 1234 dmins (0x04D2), 'N' (0x4E)
        bit_str2.push(b"\x2B\x1C\x04\xD2\x4E", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('degs', 8), 
                     Numeric('mins', 8), 
                     Numeric('dmins', 16), 
                     ASCII('direction', 8)])

        assert res["degs"] == 43
        assert res["mins"] == 28
        assert res["dmins"] == 1234
        assert res["direction"] == 'N'

    def test2_gps_latitude(self, bit_str2):
        # 10 degs (0x0A), 59 mins (0x3B), 9999 dmins (0x270F), 'S' (0x53)
        bit_str2.push(b"\x0A\x3B\x27\x0F\x53", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('degs', 8), 
                     Numeric('mins', 8), 
                     Numeric('dmins', 16), 
                     ASCII('direction', 8)])

        assert res["degs"] == 10
        assert res["mins"] == 59
        assert res["dmins"] == 9999
        assert res["direction"] == 'S'

    # --- GPS_LONGITUDE Tests ---
    def test1_gps_longitude(self, bit_str2):
        # 79 degs (0x4F), 59 mins (0x3B), 5678 dmins (0x162E), 'W' (0x57)
        bit_str2.push(b"\x4F\x3B\x16\x2E\x57", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('degs', 8), 
                     Numeric('mins', 8), 
                     Numeric('dmins', 16), 
                     ASCII('direction', 8)])

        assert res["degs"] == 79
        assert res["mins"] == 59
        assert res["dmins"] == 5678
        assert res["direction"] == 'W'

    def test2_gps_longitude(self, bit_str2):
        # 179 degs (0xB3), 0 mins (0x00), 1 dmins (0x0001), 'E' (0x45)
        bit_str2.push(b"\xB3\x00\x00\x01\x45", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('degs', 8), 
                     Numeric('mins', 8), 
                     Numeric('dmins', 16), 
                     ASCII('direction', 8)])

        assert res["degs"] == 179
        assert res["mins"] == 0
        assert res["dmins"] == 1
        assert res["direction"] == 'E'

    # --- GPS_ALTITUDE Tests ---
    def test1_gps_altitude(self, bit_str2):
        # altitude 500 (0x01F4), daltitude 25 (0x19), 'M' (0x4D) -> 500.25 M
        bit_str2.push(b"\x01\xF4\x19\x4D", 32)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('altitude', 16), 
                     Numeric('daltitude', 8), 
                     ASCII('unit', 8)])

        assert res["altitude"] == 500
        assert res["daltitude"] == 25
        assert res["unit"] == 'M'

    def test2_gps_altitude(self, bit_str2):
        # altitude 10000 (0x2710), daltitude 99 (0x63), 'F' (0x46) -> 10000.99 F
        bit_str2.push(b"\x27\x10\x63\x46", 32)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric('altitude', 16), 
                     Numeric('daltitude', 8), 
                     ASCII('unit', 8)])

        assert res["altitude"] == 10000
        assert res["daltitude"] == 99
        assert res["unit"] == 'F'

    # --- GPS_INFO Tests ---
    def test1_gps_info(self, bit_str2):
        bit_str2.push(b"\x05\x02", 16) # 5 sats, quality 2
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("num_sats", 8),
                     Numeric("quality", 8)])

        assert res["num_sats"] == 5
        assert res["quality"] == 2

    def test2_gps_info(self, bit_str2):
        bit_str2.push(b"\x08\x03", 16) # 8 sats, quality 3
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Numeric("num_sats", 8),
                     Numeric("quality", 8)])

        assert res["num_sats"] == 8
        assert res["quality"] == 3

    # --- STATE_EST_DATA Tests ---
    def test1_state_est_data(self, bit_str2):
        # 0x0A (STATE_ID_ALT), data 123.45 (approx 0x42F6E666 float)
        bit_str2.push(b"\x0A\x42\xF6\xE6\x66", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum('state_id', 8, mt.state_est_id), 
                     Floating('data', big_endian=True)])

        assert res["state_id"] == "STATE_ID_ALT"
        assert res["data"] == approx(123.45, abs=1e-3)

    def test2_state_est_data(self, bit_str2):
        # 0x04 (STATE_ID_RATE_WX), data -0.01 (approx 0xBCA3D70A float)
        bit_str2.push(b"\x04\xBC\xA3\xD7\x0A", 40)
        res = parsley.parse_fields(bit_str2, 
                    [TIMESTAMP_2,
                     Enum('state_id', 8, mt.state_est_id), 
                     Floating('data', big_endian=True)])

        assert res["state_id"] == "STATE_ID_RATE_WX"
        assert res["data"] == approx(-0.02, abs=1e-3)

    # --- LEDS_ON Tests ---
    def test1_leds_on(self, bit_str2):
        # LEDS_ON only has MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID in its definition. 
        # The parsley fields list is empty after TIMESTAMP_2.
        # It's an empty message payload.
        res = parsley.parse_fields(bit_str2, [TIMESTAMP_2]) # Only TIMESTAMP_2 in the payload
        print(res["time"])
        assert res['time'] 

    def test2_leds_off(self, bit_str2):
        # LEDS_OFF only has MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID in its definition.
        res = parsley.parse_fields(bit_str2, [TIMESTAMP_2])
        print(res["time"])
        assert res['time']

