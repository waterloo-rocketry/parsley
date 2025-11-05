from dataclasses import dataclass
from typing import Literal, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

BoardTypeID = str
BoardInstID = str
MsgPrio = Literal["HIGHEST", "HIGH", "MEDIUM", "LOW"]
MsgType = Literal["GENERAL_BOARD_STATUS", "RESET_CMD", "DEBUG_RAW", "CONFIG_SET", "CONFIG_STATUS", "ACTUATOR_CMD", "ACTUATOR_ANALOG_CMD", "ACTUATOR_STATUS", "ALT_ARM_CMD", "ALT_ARM_STATUS", "SENSOR_TEMP", "SENSOR_ALTITUDE", "SENSOR_IMU_X", "SENSOR_IMU_Y", "SENSOR_IMU_Z", "SENSOR_MAG_X", "SENSOR_MAG_Y", "SENSOR_MAG_Z", "SENSOR_BARO", "SENSOR_ANALOG", "GPS_TIMESTAMP", "GPS_LATITUDE", "GPS_LONGITUDE", "GPS_ALTITUDE", "GPS_INFO", "STATE_EST_DATA", "LEDS_ON", "LEDS_OFF"]

@dataclass
class ParsleyError():
    """Custom exception class for Parsley errors."""
    
    msg_data: str
    error: str


class ParsleyObject(BaseModel, Generic[T]):
    """
    Dataclass to store parsed CAN message data.
    """

    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_prio: MsgPrio
    msg_type: MsgType
    data: T # ParsleyDataType

    def __eq__(self, other: object) -> bool: #allows comparison to dicts
        if isinstance(other, dict):
            isSame = True
            
            if self.board_type_id != other.get('board_type_id'):
                isSame = False
            if self.board_inst_id != other.get('board_inst_id'):
                isSame = False
            if self.msg_prio != other.get('msg_prio'):
                isSame = False
            if self.msg_type != other.get('msg_type'):
                isSame = False
            if self.data != other.get('data'):
                isSame = False
                
            return isSame
        if isinstance(other, ParsleyObject):
            isSame = True
            if self.board_type_id != other.board_type_id:
                isSame = False
            if self.board_inst_id != other.board_inst_id:
                isSame = False
            if self.msg_prio != other.msg_prio:
                isSame = False
            if self.msg_type != other.msg_type:
                isSame = False
            if self.data != other.data:
                isSame = False
            return isSame

    def __getitem__(self, key: str): #allows you to access elements similarly to a dict
        d = {
            'msg_type': self.msg_type,
            'board_type_id': self.board_type_id,
            'board_inst_id': self.board_inst_id,
            'msg_prio': self.msg_prio,
            'data': self.data
        }
        
        return d[key]  
