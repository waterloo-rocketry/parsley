from dataclasses import dataclass
from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric, Floating, Bitfield
import parsley.message_types as mt


# This is an interface hence the raises, implementations should also use @dataclass(frozen=True) annotation
class ParsleyDataPayload:
    def __init__(self):
        raise NotImplementedError
    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        raise NotImplementedError
    
    def get_identifier(self) -> str | None:
        raise NotImplementedError
    
    def get_time(self) -> float:
        raise NotImplementedError
 
    def get_data_dict(self) -> dict:
        raise NotImplementedError

TIMESTAMP_2 = Numeric('time', 16, scale=1/1000, unit='s')

@dataclass(frozen = True)
class GENERAL_BOARD_STATUS (ParsleyDataPayload):
    time: float
    general_board_status: str
    board_error_bitfield: str
    
    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        general_board_status = Bitfield("general_board_status", 32, "E_NOMINAL", mt.general_board_status_offset).decode(bit_str)
        board_error_bitfield = Bitfield('board_error_bitfield', 16, "E_NOMINAL", mt.board_specific_status_offset).decode(bit_str)
        return cls (time, general_board_status, board_error_bitfield)
    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time

    def get_data_dict(self) -> dict:
        return {
            "general_board_status": self.general_board_status,
            "board_error_bitfield": self.board_error_bitfield,
        }
    
@dataclass(frozen = True)
class RESET_CMD (ParsleyDataPayload):
    time: float
    board_type_id: str
    board_inst_id: str
    
    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        board_type_id = Enum('board_type_id', 8, mt.board_type_id).decode(bit_str)
        board_inst_id = Enum('board_inst_id', 8, mt.board_inst_id).decode(bit_str)
        return cls (time, board_type_id, board_inst_id)
    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time

    def get_data_dict(self) -> dict:
        return {
            "board_type_id": self.board_type_id,
            "board_inst_id": self.board_inst_id,
        }
    
@dataclass(frozen = True)
class DEBUG_RAW (ParsleyDataPayload):
    time: float
    string: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        string = ASCII('string', 48).decode(bit_str)
        return cls (time, string)
    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "string": self.string,
        }
    
@dataclass(frozen = True)
class CONFIG_SET (ParsleyDataPayload):
    time: float
    board_type_id: str
    board_inst_id: str
    config_id:int
    config_value: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        board_type_id = Enum('board_type_id', 8, mt.board_type_id).decode(bit_str)
        board_inst_id = Enum('board_inst_id', 8, mt.board_inst_id).decode(bit_str)
        config_id = Numeric('config_id', 16).decode(bit_str)
        config_value = Numeric('config_value', 16).decode(bit_str)
        return cls (time, board_type_id, board_inst_id, config_id, config_value)
    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict[str]:
        return {
            "board_type_id": self.board_type_id,
            "board_inst_id": self.board_inst_id,
            "config_id": self.config_id,
            "config_value": self.config_value,
        }
    
@dataclass(frozen = True)
class CONFIG_STATUS (ParsleyDataPayload):
    time: float
    config_id: int
    config_value: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        config_id = Numeric('config_id', 16).decode(bit_str)
        config_value = Numeric('config_value', 16).decode(bit_str)
        return cls (time, config_id, config_value)
    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "config_id": self.config_id,
            "config_value": self.config_value,
        }

@dataclass(frozen = True)
class ACTUATOR_CMD (ParsleyDataPayload):

    time: float
    actuator : str
    cmd_state: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        actuator = Enum('actuator', 8, mt.actuator_id).decode(bit_str)
        cmd_state = Enum('cmd_state', 8, mt.actuator_state).decode(bit_str)
        return cls(time, actuator, cmd_state)
    def get_identifier(self) -> str | None:
        return self.actuator
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "actuator": self.actuator,
            "cmd_state": self.cmd_state,
        }
    
@dataclass(frozen = True)    
class ACTUATOR_ANALOG_CMD (ParsleyDataPayload):

    time: float
    actuator: str
    cmd_state: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        actuator = Enum('actuator', 8, mt.actuator_id).decode(bit_str)
        cmd_state = Numeric('cmd_state', 16).decode(bit_str)
        return cls(time, actuator, cmd_state)
    def get_identifier(self) -> str | None:
        return self.actuator
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "actuator": self.actuator,
            "cmd_state": self.cmd_state,
        }

@dataclass(frozen = True)
class ACTUATOR_STATUS (ParsleyDataPayload):

    time:float
    actuator: str
    curr_state: str
    cmd_state: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        actuator = Enum('actuator', 8, mt.actuator_id).decode(bit_str)
        curr_state = Enum('curr_state', 8, mt.actuator_state).decode(bit_str)
        cmd_state = Enum('cmd_state', 8, mt.actuator_state).decode(bit_str)
        return cls(time, actuator, curr_state, cmd_state)
        
    def get_identifier(self) -> str | None:
        return self.actuator
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "actuator": self.actuator,
            "curr_state": self.curr_state,
            "cmd_state": self.cmd_state,    
        }

@dataclass(frozen=True)
class ALT_ARM_CMD(ParsleyDataPayload):

    time: float
    alt_id: str
    alt_arm_state: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        alt_id = Enum("alt_id", 8, mt.altimeter_id).decode(bit_str)
        alt_arm_state = Enum("alt_arm_state", 8, mt.alt_arm_state).decode(bit_str)
        return cls(time, alt_id, alt_arm_state)

    def get_identifier(self) -> str | None:
        return self.alt_id 
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "alt_id": self.alt_id,
            "alt_arm_state": self.alt_arm_state,
        }

@dataclass(frozen=True)
class ALT_ARM_STATUS(ParsleyDataPayload):
    time: float
    alt_id: str
    alt_arm_state: str
    drogue_v: int
    main_v: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        alt_id = Enum("alt_id", 8, mt.altimeter_id).decode(bit_str)
        alt_arm_state = Enum("alt_arm_state", 8, mt.alt_arm_state).decode(bit_str)
        drogue_v = Numeric("drogue_v", 16).decode(bit_str)
        main_v = Numeric("main_v", 16).decode(bit_str)
        return cls(time, alt_id, alt_arm_state, drogue_v, main_v)

    def get_identifier(self) -> str | None:
        return self.alt_id
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "alt_id": self.alt_id,
            "alt_arm_state": self.alt_arm_state,
            "drogue_v": self.drogue_v,
            "main_v": self.main_v,
        }

@dataclass(frozen=True)
class SENSOR_ALTITUDE(ParsleyDataPayload):
    time: float
    altitude: int
    apogee_state: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        altitude = Numeric("altitude", 32, signed=True).decode(bit_str)
        apogee_state = Enum("apogee_state", 8, mt.apogee_state).decode(bit_str)
        return cls(time, altitude, apogee_state)

    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "altitude": self.altitude, 
            "apogee_state": self.apogee_state
        }

@dataclass(frozen=True)
class SENSOR_IMU(ParsleyDataPayload):
    time: float
    imu_id: str
    linear_accel: int
    angular_velocity: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        imu_id = Enum("imu_id", 8, mt.imu_id).decode(bit_str)
        linear_accel = Numeric("linear_accel", 16).decode(bit_str)
        angular_velocity = Numeric("angular_velocity", 16).decode(bit_str)
        return cls(time, imu_id, linear_accel, angular_velocity)

    def get_identifier(self) -> str | None:
        return self.imu_id
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "imu_id": self.imu_id,
            "linear_accel": self.linear_accel,
            "angular_velocity": self.angular_velocity,
        }

@dataclass(frozen=True)
class SENSOR_MAG(ParsleyDataPayload):
    time: float
    imu_id: str
    mag: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        imu_id = Enum("imu_id", 8, mt.imu_id).decode(bit_str)
        mag = Numeric("mag", 16).decode(bit_str)
        return cls(time, imu_id, mag)

    def get_identifier(self)-> str | None:
        return self.imu_id
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "imu_id": self.imu_id, 
            "mag": self.mag
        }
    
@dataclass(frozen=True)
class SENSOR_BARO(ParsleyDataPayload):
    time: float
    imu_id: str
    pressure: int
    temp: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        imu_id = Enum("imu_id", 8, mt.imu_id).decode(bit_str)
        pressure = Numeric("pressure", 24).decode(bit_str)
        temp = Numeric("temp", 16).decode(bit_str)
        return cls(time, imu_id, pressure, temp)

    def get_identifier(self) -> str | None:
        return self.imu_id
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "imu_id": self.imu_id,
            "pressure": self.pressure,
            "temp": self.temp,
        }

@dataclass(frozen=True)
class SENSOR_ANALOG(ParsleyDataPayload):
    time: float
    sensor_id: str
    value: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        sensor_id = Enum("sensor_id", 8, mt.analog_sensor_id).decode(bit_str)
        value = Numeric("value", 16).decode(bit_str)
        return cls(time, sensor_id, value)

    def get_identifier(self) -> str | None:
        return self.sensor_id
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "sensor_id": self.sensor_id, 
            "value": self.value
        }

@dataclass(frozen=True)
class GPS_TIMESTAMP(ParsleyDataPayload):
    time: float
    hrs: int
    mins: int
    secs: int
    dsecs: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        hrs = Numeric("hrs", 8).decode(bit_str)
        mins = Numeric("mins", 8).decode(bit_str)
        secs = Numeric("secs", 8).decode(bit_str)
        dsecs = Numeric("dsecs", 8).decode(bit_str)
        return cls(time, hrs, mins, secs, dsecs)

    def get_identifier(self)-> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "hrs": self.hrs, 
            "mins": self.mins, 
            "secs": self.secs, 
            "dsecs": self.dsecs
        }

@dataclass(frozen=True)
class GPS_LATITUDE(ParsleyDataPayload):
    time: float
    degs: int
    mins: int
    dmins: int
    direction: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        degs = Numeric("degs", 8).decode(bit_str)
        mins = Numeric("mins", 8).decode(bit_str)
        dmins = Numeric("dmins", 16).decode(bit_str)
        direction = ASCII("direction", 8).decode(bit_str)
        return cls(time, degs, mins, dmins, direction)

    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "degs": self.degs,
            "mins": self.mins,
            "dmins": self.dmins,
            "direction": self.direction,
        }

@dataclass(frozen=True)
class GPS_LONGITUDE(ParsleyDataPayload):
    time: float
    degs: int
    mins: int
    dmins: int
    direction: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        degs = Numeric("degs", 8).decode(bit_str)
        mins = Numeric("mins", 8).decode(bit_str)
        dmins = Numeric("dmins", 16).decode(bit_str)
        direction = ASCII("direction", 8).decode(bit_str)
        return cls(time, degs, mins, dmins, direction)

    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "degs": self.degs,
            "mins": self.mins,
            "dmins": self.dmins,
            "direction": self.direction,
        }

@dataclass(frozen=True)
class GPS_ALTITUDE(ParsleyDataPayload):
    time: float
    altitude: int
    daltitude: int
    unit: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        altitude = Numeric("altitude", 16).decode(bit_str)
        daltitude = Numeric("daltitude", 8).decode(bit_str)
        unit = ASCII("unit", 8).decode(bit_str)
        return cls(time, altitude, daltitude, unit)

    def get_identifier(self) -> str | None:
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "altitude": self.altitude,
            "daltitude": self.daltitude,
            "unit": self.unit,
        }

@dataclass(frozen=True)
class GPS_INFO(ParsleyDataPayload):
    time: float
    num_sats: int
    quality: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        num_sats = Numeric("num_sats", 8).decode(bit_str)
        quality = Numeric("quality", 8).decode(bit_str)
        return cls(time, num_sats, quality)

    def get_identifier(self) -> str | None: 
        return None
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "num_sats": self.num_sats,
            "quality": self.quality
        }


@dataclass(frozen=True)
class STATE_EST_DATA(ParsleyDataPayload):
    time: float
    state_id: str
    data: float

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        state_id = Enum("state_id", 8, mt.state_est_id).decode(bit_str)
        data = Floating("data", big_endian=True).decode(bit_str)
        return cls(time, state_id, data)

    def get_identifier(self) -> str | None:
        return self.state_id
    def get_time(self) -> float:
        return self.time
    def get_data_dict(self) -> dict:
        return {
            "state_id": self.state_id, 
            "data": self.data
        }
    
@dataclass(frozen=True)
class STREAM_STATUS(ParsleyDataPayload):
    time: float
    total_size: int
    tx_size: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        total_size = Numeric("total_size", 24).decode(bit_str)
        tx_size = Numeric("tx_size", 24).decode(bit_str)
        return cls(time, total_size, tx_size)

    def get_identifier(self) -> str | None:
        return None

    def get_time(self) -> float:
        return self.time

    def get_data_dict(self) -> dict:
        return {
            "total_size": self.total_size,
            "tx_size": self.tx_size
        }

@dataclass(frozen=True)
class STREAM_DATA(ParsleyDataPayload):
    time: float
    seq_id: int
    data: str

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        seq_id = Numeric("seq_id", 8).decode(bit_str)
        data = ASCII("data", 40).decode(bit_str)
        return cls(time, seq_id, data)

    def get_identifier(self) -> str | None:
        return None

    def get_time(self) -> float:
        return self.time

    def get_data_dict(self) -> dict:
        return {
            "seq_id": self.seq_id,
            "data": self.data
        }

@dataclass(frozen=True)
class STREAM_RETRY(ParsleyDataPayload):
    time: float
    seq_id: int

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        time = TIMESTAMP_2.decode(bit_str)
        seq_id = Numeric("seq_id", 8).decode(bit_str)
        return cls(time, seq_id)

    def get_identifier(self) -> str | None:
        return None

    def get_time(self) -> float:
        return self.time

    def get_data_dict(self) -> dict:
        return {
            "seq_id": self.seq_id
        }

# Factory function to build each type
def parse_payload(msg_type, bit_str):
    mapping = {
        "GENERAL_BOARD_STATUS": GENERAL_BOARD_STATUS,
        "RESET_CMD": RESET_CMD,
        "DEBUG_RAW": DEBUG_RAW,
        "CONFIG_SET": CONFIG_SET,
        "CONFIG_STATUS": CONFIG_STATUS,
        "ACTUATOR_CMD": ACTUATOR_CMD,
        "ACTUATOR_ANALOG_CMD": ACTUATOR_ANALOG_CMD,
        "ACTUATOR_STATUS": ACTUATOR_STATUS,
        "ALT_ARM_CMD": ALT_ARM_CMD,
        "ALT_ARM_STATUS": ALT_ARM_STATUS,
        "SENSOR_ALTITUDE": SENSOR_ALTITUDE,
        "SENSOR_IMU_X": SENSOR_IMU,
        "SENSOR_IMU_Y": SENSOR_IMU,
        "SENSOR_IMU_Z": SENSOR_IMU,
        "SENSOR_MAG_X": SENSOR_MAG,
        "SENSOR_MAG_Y": SENSOR_MAG,
        "SENSOR_MAG_Z": SENSOR_MAG,
        "SENSOR_BARO": SENSOR_BARO,
        "SENSOR_ANALOG": SENSOR_ANALOG,
        "GPS_TIMESTAMP": GPS_TIMESTAMP,
        "GPS_LATITUDE": GPS_LATITUDE,
        "GPS_LONGITUDE": GPS_LONGITUDE,
        "GPS_ALTITUDE": GPS_ALTITUDE,
        "GPS_INFO": GPS_INFO,
        "STATE_EST_DATA": STATE_EST_DATA,
        "STREAM_STATUS": STREAM_STATUS,
        "STREAM_DATA": STREAM_DATA,
        "STREAM_RETRY": STREAM_RETRY,
    }

    payload_cls = mapping.get(msg_type) # gets the corresponding class
    if payload_cls is None: # for messages like like LED_ON and LED_OFF
        return None
    return payload_cls.from_bitstring(bit_str)




