from dataclasses import dataclass, asdict
from typing import Generic, TypeVar
from pydantic import BaseModel, field_validator, model_validator
import parsley.message_types as mt

T = TypeVar("T")

BoardTypeID = str
BoardInstID = str
MsgPrio = str
MsgType = str
MsgMetadata = int | str

# Per-msg-type metadata enum mapping. Mirrors the index-3 field of each
# msg_type in CAN_MESSAGE (parsley.message_definitions). Kept here as a
# literal table to avoid pulling message_definitions into this module —
# message_definitions imports parsley.fields which doesn't import this
# file, but importing CAN_MESSAGE would couple the validators to the
# wire-format module unnecessarily. If a new msg_type with an Enum
# metadata byte is added to MESSAGES, add it here too.
_METADATA_ENUM_BY_MSG_TYPE: dict[str, dict[str, int]] = {
    'ACTUATOR_CMD':       mt.actuator_id,
    'ACTUATOR_STATUS':    mt.actuator_id,
    'ALT_ARM_CMD':        mt.altimeter_id,
    'ALT_ARM_STATUS':     mt.altimeter_id,
    'SENSOR_ANALOG16':    mt.analog_sensor_id,
    'SENSOR_ANALOG32':    mt.analog_sensor_id,
    'SENSOR_2D_ANALOG24': mt.dem_2d_sensor_id,
    'SENSOR_3D_ANALOG16': mt.dem_3d_sensor_id,
}

@dataclass
class ParsleyError():
    """Custom error container for Parsley errors."""
    msg_prio: MsgPrio
    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_type: MsgType
    msg_metadata: MsgMetadata
    msg_data: str
    error: str

    def __getitem__(self, key: str):
        return asdict(self)[key]
    
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
        # MESSAGE_PRIO is a 2-bit Enum with all 4 values mapped, so the parser
        # will always emit a value from mt.msg_prio. Any other string is a
        # caller-side mistake — accepting it silently used to mask bugs like
        # callers passing the hexified bytes `'0x03'` instead of the name `'LOW'`.
        if value not in mt.msg_prio:
            raise ValueError(
                f"Invalid msg_prio '{value}' (expected one of {list(mt.msg_prio)})"
            )
        return value

    @field_validator("msg_type")
    def validate_msg_type(cls, value):
        if value not in mt.msg_type:
            raise ValueError(f"Invalid msg_type type '{value}'")
        return value

    @field_validator("msg_metadata")
    def validate_msg_metadata(cls, value):
        # Field-level validation: shape + numeric range. The semantic check
        # (string value is a valid key in the per-msg-type enum) needs
        # msg_type, so it runs in the model-level validator below.
        if isinstance(value, int):
            if not (0 <= value <= 255):
                raise ValueError(f"msg_metadata '{value}' is out of range (0-255)")
        elif isinstance(value, str):
            if len(value) == 0:
                raise ValueError('msg_metadata string must be non-empty')
        else:
            raise ValueError('msg_metadata must be int or str')
        return value

    @model_validator(mode='after')
    def validate_msg_metadata_against_msg_type(self):
        # Cross-check the metadata value against the msg_type's expected enum.
        # The parser falls back to an int byte (0-255) when an Enum-typed
        # metadata decode fails on a corrupt frame, so int values are always
        # accepted regardless of msg_type. But a string value must be a real
        # key in the matching enum — otherwise encode_data would crash later
        # at re-emit time, and the bad value would silently propagate through
        # consumers that branch on the metadata string.
        if isinstance(self.msg_metadata, str):
            enum_map = _METADATA_ENUM_BY_MSG_TYPE.get(self.msg_type)
            if enum_map is None:
                raise ValueError(
                    f"msg_metadata is a string ('{self.msg_metadata}') but msg_type "
                    f"'{self.msg_type}' uses a numeric metadata byte"
                )
            if self.msg_metadata not in enum_map:
                raise ValueError(
                    f"msg_metadata '{self.msg_metadata}' is not a valid key for "
                    f"msg_type '{self.msg_type}' "
                    f"(expected a name from {list(enum_map.keys())[:3]}…)"
                )
        return self

    def __getitem__(self, key: str):
        return self.model_dump()[key]
