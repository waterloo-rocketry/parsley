from dataclasses import dataclass
from typing import Literal, Generic, TypeVar
from pydantic import BaseModel, field_validator
import parsley.message_types as mt

T = TypeVar("T")

BoardTypeID = str
BoardInstID = str
MsgPrio = str #will be checked during runtime
MsgType = str #will be checked during runtime

@dataclass
class ParsleyError():
    """Custom exception class for Parsley errors."""
    board_type_id: str
    board_inst_id: str
    msg_type: str
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

    @field_validator("msg_prio")
    def validate_msg_prio(cls, value):
        if value not in mt.msg_prio:
            raise ValueError(f"Invalid msg_prio type '{value}'")
        return value
    
    @field_validator("msg_type")
    def validate_msg_type(cls, value):
        if value not in mt.msg_type:
            raise ValueError(f"Invalid msg_type type '{value}'")
        return value
    
    def __getitem__(self, key: str):        
        return self.model_dump()[key]