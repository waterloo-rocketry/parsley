import pytest
import parsley

from bitstring import BitString
from fields import ASCII, Enum, Numeric
from message_definitions import TIMESTAMP_2, TIMESTAMP_3, CAN_MESSAGE

import message_types as mt
import test_utils as tu

class TestCANMessage:
    """
    We are testing only the message body of CAN messages, which means that BitString won't contain
    a message_sid (ie. message_type | board_id where '|' represents bitwise OR)
    """
    @pytest.fixture()
    def bit_str2(self):
        bit_str2 = BitString()
        bit_str2.push(*TIMESTAMP_2.encode(0))
        return bit_str2

    @pytest.fixture()
    def bit_str3(self):
        bit_str3 = BitString()
        bit_str3.push(*TIMESTAMP_3.encode(0))
        return bit_str3

    def test_general_cmd(self, bit_str3):
        bit_str3.push(*Enum('command', 8, mt.gen_cmd).encode('BUS_DOWN_WARNING'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_CMD')[1:])
        assert res['command'] == 'BUS_DOWN_WARNING'

    def test_actuator_cmd(self, bit_str3):
        bit_str3.push(*Enum('actuator', 8, mt.actuator_id).encode('ACTUATOR_VENT_VALVE'))
        bit_str3.push(*Enum('req_state', 8, mt.actuator_states).encode('ACTUATOR_OFF'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('ACTUATOR_CMD')[1:])
        assert res['actuator'] == 'ACTUATOR_VENT_VALVE'
        assert res['req_state'] == 'ACTUATOR_OFF'

    def test_alt_arm_cmd(self, bit_str3):
        bit_str3.push(*Enum('state', 4, mt.arm_states).encode('ARMED'))
        bit_str3.push(*Numeric('altimeter', 4).encode(7))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('ALT_ARM_CMD')[1:])
        assert res['state'] == 'ARMED'
        assert res['altimeter'] == 7

    def test_reset_cmd(self, bit_str3):
        bit_str3.push(*Enum('board_id', 8, mt.board_id).encode('ANY'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('RESET_CMD')[1:])
        assert res['board_id'] == 'ANY'

    def test_debug_msg(self, bit_str3):
        bit_str3.push(*Numeric('level', 4).encode(6))
        bit_str3.push(*Numeric('line', 12).encode(0x123))
        bit_str3.push(*ASCII('data', 24).encode('AC'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('DEBUG_MSG')[1:])
        assert res['level'] == 6
        assert res['line'] == 0x123
        assert res['data'] == 'AC'

    # don't need pytest fixtures since this message type doesn't contain a timestamp
    def test_debug_printf(self):
        bit_str = BitString()
        bit_str.push(*ASCII('string', 64).encode('ABCDEFGH'))
        res = parsley.parse_fields(bit_str, CAN_MESSAGE.get_fields('DEBUG_PRINTF')[1:])
        assert res['string'] == 'ABCDEFGH'

    # don't need pytest fixtures since this message type doesn't contain a timestamp
    def test_debug_radio_cmd(self):
        bit_str = BitString()
        bit_str.push(*ASCII('string', 64).encode('RADIO'))
        res = parsley.parse_fields(bit_str, CAN_MESSAGE.get_fields('DEBUG_RADIO_CMD')[1:])
        assert res['string'] == 'RADIO'

    def test_actuator_status(self, bit_str3):
        bit_str3.push(*Enum('actuator', 8, mt.actuator_id).encode('ACTUATOR_INJECTOR_VALVE'))
        bit_str3.push(*Enum('cur_state', 8, mt.actuator_states).encode('ACTUATOR_UNK'))
        bit_str3.push(*Enum('req_state', 8, mt.actuator_states).encode('ACTUATOR_OFF'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('ACTUATOR_STATUS')[1:])
        assert res['actuator'] == 'ACTUATOR_INJECTOR_VALVE'
        assert res['cur_state'] == 'ACTUATOR_UNK'
        assert res['req_state'] == 'ACTUATOR_OFF'

    def test_alt_arm_status(self, bit_str3):
        bit_str3.push(*Enum('state', 4, mt.arm_states).encode('DISARMED'))
        bit_str3.push(*Numeric('altimeter', 4).encode(4))
        bit_str3.push(*Numeric('drogue_v', 16).encode(12345))
        bit_str3.push(*Numeric('main_v', 16).encode(54321))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('ALT_ARM_STATUS')[1:])
        assert res['state'] == 'DISARMED'
        assert res['altimeter'] == 4
        assert res['drogue_v'] == 12345
        assert res['main_v'] == 54321

    def test_board_status_nominal(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_NOMINAL'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_NOMINAL'

    def test_board_status_current(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_BUS_OVER_CURRENT'))
        bit_str3.push(*Numeric('current', 16).encode(12345))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_BUS_OVER_CURRENT'
        assert res['current'] == 12345

    def test_board_status_voltage(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_BUS_UNDER_VOLTAGE'))
        bit_str3.push(*Numeric('voltage', 16).encode(54321))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_BUS_UNDER_VOLTAGE'
        assert res['voltage'] == 54321

    def test_board_status_dead(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_BOARD_FEARED_DEAD'))
        bit_str3.push(*Enum('board_id', 8, mt.board_id).encode('KALMAN'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        print(res)
        assert res['status'] == 'E_BOARD_FEARED_DEAD'
        assert res['board_id'] == 'KALMAN'

    def test_board_status_quiet(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_NO_CAN_TRAFFIC'))
        bit_str3.push(*Numeric('err_time', 16).encode(54321))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_NO_CAN_TRAFFIC'
        assert res['err_time'] == 54321

    def test_board_status_actuator(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_ACTUATOR_STATE'))
        bit_str3.push(*Enum('req_state', 8, mt.actuator_states).encode('ACTUATOR_OFF'))
        bit_str3.push(*Enum('cur_state', 8, mt.actuator_states).encode('ACTUATOR_UNK'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_ACTUATOR_STATE'
        assert res['req_state'] == 'ACTUATOR_OFF'
        assert res['cur_state'] == 'ACTUATOR_UNK'

    def test_board_status_logging(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_LOGGING'))
        bit_str3.push(*Enum('error', 8, mt.logger_error).encode('E_SYSLOG_ALL_BUFFERS_FULL'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_LOGGING'
        assert res['error'] == 'E_SYSLOG_ALL_BUFFERS_FULL'

    def test_board_status_sensor(self, bit_str3):
        bit_str3.push(*Enum('status', 8, mt.board_status).encode('E_SENSOR'))
        bit_str3.push(*Enum('sensor_id', 8, mt.sensor_id).encode('SENSOR_BARO'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GENERAL_BOARD_STATUS')[1:])
        assert res['status'] == 'E_SENSOR'
        assert res['sensor_id'] == 'SENSOR_BARO'

    def test_sensor_temp(self, bit_str3):
        bit_str3.push(*Numeric('sensor_id', 8).encode(0x12))
        bit_str3.push(*Numeric('temperature', 24, scale=1/2**10, signed=True).encode(12.5))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('SENSOR_TEMP')[1:])
        assert res['sensor_id'] == 0x12
        assert res['temperature'] == tu.approx(12.5)

    def test_sensor_altitude(self, bit_str3):
        bit_str3.push(*Numeric('altitude', 32, signed=True).encode(-12345))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('SENSOR_ALTITUDE')[1:])
        assert res['altitude'] == -12345

    def test_sensor_acc(self, bit_str2):
        bit_str2.push(*Numeric('x', 16, scale=8/2**16, signed=True).encode(-2))
        bit_str2.push(*Numeric('y', 16, scale=8/2**16, signed=True).encode(-3))
        bit_str2.push(*Numeric('z', 16, scale=8/2**16, signed=True).encode(-4))
        res = parsley.parse_fields(bit_str2, CAN_MESSAGE.get_fields('SENSOR_ACC')[1:])
        assert res['x'] == tu.approx(-2)
        assert res['y'] == tu.approx(-3)
        assert res['z'] == tu.approx(-4)

    def test_sensor_acc2(self, bit_str2):
        bit_str2.push(*Numeric('x', 16, scale=16/2**16, signed=True).encode(3))
        bit_str2.push(*Numeric('y', 16, scale=16/2**16, signed=True).encode(0))
        bit_str2.push(*Numeric('z', 16, scale=16/2**16, signed=True).encode(-3))
        res = parsley.parse_fields(bit_str2, CAN_MESSAGE.get_fields('SENSOR_ACC2')[1:])
        assert res['x'] == tu.approx(3)
        assert res['y'] == tu.approx(0)
        assert res['z'] == tu.approx(-3)

    def test_sensor_gyro(self, bit_str2):
        bit_str2.push(*Numeric('x', 16, scale=2000/2**16, signed=True).encode(3))
        bit_str2.push(*Numeric('y', 16, scale=2000/2**16, signed=True).encode(4))
        bit_str2.push(*Numeric('z', 16, scale=2000/2**16, signed=True).encode(5))
        res = parsley.parse_fields(bit_str2, CAN_MESSAGE.get_fields('SENSOR_GYRO')[1:])
        assert res['x'] == tu.approx(3)
        assert res['y'] == tu.approx(4)
        assert res['z'] == tu.approx(5)
    
    def test_sensor_mag(self, bit_str2):
        bit_str2.push(*Numeric('x', 16, signed=True).encode(-100))
        bit_str2.push(*Numeric('y', 16, signed=True).encode(-200))
        bit_str2.push(*Numeric('z', 16, signed=True).encode(-300))
        res = parsley.parse_fields(bit_str2, CAN_MESSAGE.get_fields('SENSOR_MAG')[1:])
        assert res['x'] == tu.approx(-100)
        assert res['y'] == tu.approx(-200)
        assert res['z'] == tu.approx(-300)

    def test_sensor_analog(self, bit_str2):
        bit_str2.push(*Enum('sensor_id', 8, mt.sensor_id).encode('SENSOR_BARO'))
        bit_str2.push(*Numeric('value', 16, signed=True).encode(-12345))
        res = parsley.parse_fields(bit_str2, CAN_MESSAGE.get_fields('SENSOR_ANALOG')[1:])
        assert res['sensor_id'] == 'SENSOR_BARO'
        assert res['value'] == -12345

    def test_gps_timestamp(self, bit_str3):
        bit_str3.push(*Numeric('hrs', 8).encode(12))
        bit_str3.push(*Numeric('mins', 8).encode(23))
        bit_str3.push(*Numeric('secs', 8).encode(34))
        bit_str3.push(*Numeric('dsecs', 8).encode(45))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GPS_TIMESTAMP')[1:])
        assert res['hrs'] == 12
        assert res['mins'] == 23
        assert res['secs'] == 34
        assert res['dsecs'] == 45

    def test_gps_latitude(self, bit_str3):
        bit_str3.push(*Numeric('degs', 8).encode(12))
        bit_str3.push(*Numeric('mins', 8).encode(23))
        bit_str3.push(*Numeric('dmins', 16).encode(12345))
        bit_str3.push(*ASCII('direction', 8).encode('N'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GPS_LATITUDE')[1:])
        assert res['degs'] == 12
        assert res['mins'] == 23
        assert res['dmins'] == 12345
        assert res['direction'] == 'N'

    def test_gps_longitude(self, bit_str3):
        bit_str3.push(*Numeric('degs', 8).encode(12))
        bit_str3.push(*Numeric('mins', 8).encode(23))
        bit_str3.push(*Numeric('dmins', 16).encode(12345))
        bit_str3.push(*ASCII('direction', 8).encode('W'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GPS_LONGITUDE')[1:])
        assert res['degs'] == 12
        assert res['mins'] == 23
        assert res['dmins'] == 12345
        assert res['direction'] == 'W'

    def test_gps_altitude(self, bit_str3):
        bit_str3.push(*Numeric('altitude', 16).encode(12345))
        bit_str3.push(*Numeric('daltitude', 8).encode(12))
        bit_str3.push(*ASCII('unit', 8).encode('m'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GPS_ALTITUDE')[1:])
        assert res['altitude'] == 12345
        assert res['daltitude'] == 12
        assert res['unit'] == 'm'

    def test_gps_info(self, bit_str3):
        bit_str3.push(*Numeric('num_sats', 8).encode(12))
        bit_str3.push(*Numeric('quality', 8).encode(23))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('GPS_INFO')[1:])
        assert res['num_sats'] == 12
        assert res['quality'] == 23

    def test_fill_lvl(self, bit_str3):
        bit_str3.push(*Numeric('level', 8).encode(9))
        bit_str3.push(*Enum('direction', 8, mt.fill_direction).encode('FILLING'))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('FILL_LVL')[1:])
        assert res['level'] == 9
        assert res['direction'] == 'FILLING'

    def test_radi_value(self, bit_str3):
        bit_str3.push(*Numeric('radi_board', 8).encode(1))
        bit_str3.push(*Numeric('radi', 16).encode(500))
        res = parsley.parse_fields(bit_str3, CAN_MESSAGE.get_fields('RADI_VALUE')[1:])
        assert res['radi_board'] == 1
        assert res['radi'] == 500

    def test_leds_on(self):
        # LED_ON message has no message body
        pass

    def test_leds_off(self):
        # LED_OFF message has no message body
        pass
