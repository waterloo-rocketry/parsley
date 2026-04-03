from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from pydantic import BaseModel, field_validator
import parsley.message_types as mt

BoardTypeID = str
BoardInstID = str
MsgPrio = str
MsgType = str
MsgMetadata = int


@dataclass
class ParsleyError:
    """Custom error container for Parsley errors."""
    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_type: MsgType
    msg_metadata: MsgMetadata
    msg_data: str
    error: str

    def __getitem__(self, key: str) -> object:
        return asdict(self)[key]


class ParsleyObject(BaseModel):
    """Dataclass to store parsed CAN message data."""

    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_prio: MsgPrio
    msg_type: MsgType
    msg_metadata: MsgMetadata
    data: Any

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("msg_prio")
    @classmethod
    def validate_msg_prio(cls, value: str) -> str:
        if value not in mt.msg_prio:
            raise ValueError(f"Invalid msg_prio type '{value}'")
        return value

    @field_validator("msg_type")
    @classmethod
    def validate_msg_type(cls, value: str) -> str:
        if value not in mt.msg_type:
            raise ValueError(f"Invalid msg_type type '{value}'")
        return value

    @field_validator("msg_metadata")
    @classmethod
    def validate_msg_metadata(cls, value: int) -> int:
        if not (0 <= value <= 255):
            raise ValueError(f"msg_metadata '{value}' is out of range (0-255)")
        return value

    def __getitem__(self, key: str) -> object:
        return self.model_dump()[key]
