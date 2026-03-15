from dataclasses import dataclass, asdict
from typing import Generic, TypeVar, Any
from pydantic import BaseModel, field_validator
import parsley.message_types as mt

T = TypeVar("T")

BoardTypeID = str
BoardInstID = str
MsgPrio = str
MsgType = str
MsgMetadata = int

@dataclass
class ParsleyError():
    """Custom error container for Parsley errors."""
    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_type: MsgType
    msg_metadata: MsgMetadata
    msg_data: str
    error: str

    def __getitem__(self, key: str):
        return asdict(self)[key]
    
    def to_flat_dict(self) -> dict[str, Any]:
        return asdict(self)
    
class ParsleyObject(BaseModel, Generic[T]):
    """
    Dataclass to store parsed CAN message data.
    """

    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_prio: MsgPrio
    msg_type: MsgType
    msg_metadata: MsgMetadata
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

    @field_validator("msg_metadata")
    def validate_msg_metadata(cls, value):
        if not (0 <= value <= 255):
            raise ValueError(f"msg_metadata '{value}' is out of range (0-255)")
        return value
    
    def __getitem__(self, key: str):        
        return self.model_dump()[key]
    
    def to_flat_dict(self) -> dict[str, Any]:
    
        dumped = self.model_dump()
        
        nested_data = dumped.pop("data", {})
        
        return {**dumped, **nested_data}

