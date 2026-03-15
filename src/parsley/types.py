from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import ClassVar

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric, Floating, Bitfield, Switch, Field
import parsley.message_types as mt


# ── SID-level field definitions (formerly in message_definitions.py) ────────

TIMESTAMP_2 = Numeric('time', 16, scale=1/1000, unit='s')

MESSAGE_PRIO = Enum('msg_prio', 2, mt.msg_prio)
MESSAGE_TYPE = Enum('msg_type', 7, mt.msg_type)
BOARD_TYPE_ID = Enum('board_type_id', 6, mt.board_type_id)
BOARD_INST_ID = Enum('board_inst_id', 6, mt.board_inst_id)
MESSAGE_METADATA = Numeric('msg_metadata', 8)
MESSAGE_SID = Enum(
    'msg_sid',
    MESSAGE_PRIO.length + MESSAGE_TYPE.length + BOARD_TYPE_ID.length
    + BOARD_INST_ID.length + MESSAGE_METADATA.length,
    {},
)

_SID_HEADER = [MESSAGE_PRIO, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_METADATA]


# ── Base class ──────────────────────────────────────────────────────────────

class ParsleyDataPayload:
    """Base class for all typed CAN message payloads.

    Subclasses must define a ``FIELDS`` class variable listing the payload
    :class:`Field` objects in wire order.  The generic :meth:`from_bitstring`
    implementation iterates over ``FIELDS`` to decode a :class:`BitString`
    into the concrete dataclass.
    """

    FIELDS: ClassVar[list[Field]] = []

    @classmethod
    def from_bitstring(cls, bit_str: BitString):
        kwargs: dict = {}
        for field in cls.FIELDS:
            kwargs[field.name] = field.decode(
                bit_str.pop(field.length, field.variable_length)
            )
        return cls(**kwargs)

    def get_identifier(self) -> str | None:
        return None

    def get_time(self) -> float:
        return self.time  # type: ignore[attr-defined]

    def to_dict(self) -> dict:
        return asdict(self)  # type: ignore[call-overload]


# ── Payload dataclasses ─────────────────────────────────────────────────────

@dataclass(frozen=True)
class GENERAL_BOARD_STATUS(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Bitfield('general_board_status', 32, 'E_NOMINAL', mt.general_board_status_offset),
        Bitfield('board_error_bitfield', 16, 'E_NOMINAL', mt.board_specific_status_offset),
    ]

    time: float
    general_board_status: str
    board_error_bitfield: str


@dataclass(frozen=True)
class RESET_CMD(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('board_type_id', 8, mt.board_type_id),
        Enum('board_inst_id', 8, mt.board_inst_id),
    ]

    time: float
    board_type_id: str
    board_inst_id: str


@dataclass(frozen=True)
class DEBUG_RAW(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, ASCII('string', 48)]

    time: float
    string: str


@dataclass(frozen=True)
class CONFIG_SET(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('board_type_id', 8, mt.board_type_id),
        Enum('board_inst_id', 8, mt.board_inst_id),
        Numeric('config_id', 16),
        Numeric('config_value', 16),
    ]

    time: float
    board_type_id: str
    board_inst_id: str
    config_id: int
    config_value: int


@dataclass(frozen=True)
class CONFIG_STATUS(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('config_id', 16),
        Numeric('config_value', 16),
    ]

    time: float
    config_id: int
    config_value: int


@dataclass(frozen=True)
class ACTUATOR_CMD(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('cmd_state', 8, mt.actuator_state),
    ]

    time: float
    cmd_state: str


@dataclass(frozen=True)
class ACTUATOR_STATUS(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('curr_state', 8, mt.actuator_state),
        Enum('cmd_state', 8, mt.actuator_state),
    ]

    time: float
    curr_state: str
    cmd_state: str


@dataclass(frozen=True)
class ALT_ARM_CMD(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('alt_arm_state', 8, mt.alt_arm_state),
    ]

    time: float
    alt_arm_state: str


@dataclass(frozen=True)
class ALT_ARM_STATUS(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('alt_arm_state', 8, mt.alt_arm_state),
        Numeric('drogue_v', 16),
        Numeric('main_v', 16),
    ]

    time: float
    alt_arm_state: str
    drogue_v: int
    main_v: int


@dataclass(frozen=True)
class SENSOR_ANALOG16(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, Numeric('value', 16)]

    time: float
    value: int


@dataclass(frozen=True)
class SENSOR_ANALOG32(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, Numeric('value', 32)]

    time: float
    value: int


@dataclass(frozen=True)
class SENSOR_DEM_ANALOG16(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('value_x', 16),
        Numeric('value_y', 16),
        Numeric('value_z', 16),
    ]

    time: float
    value_x: int
    value_y: int
    value_z: int


@dataclass(frozen=True)
class GPS_TIMESTAMP(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('hrs', 8),
        Numeric('mins', 8),
        Numeric('secs', 8),
        Numeric('dsecs', 8),
    ]

    time: float
    hrs: int
    mins: int
    secs: int
    dsecs: int


@dataclass(frozen=True)
class GPS_LATITUDE(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('degs', 8),
        Numeric('mins', 8),
        Numeric('dmins', 16),
        ASCII('direction', 8),
    ]

    time: float
    degs: int
    mins: int
    dmins: int
    direction: str


@dataclass(frozen=True)
class GPS_LONGITUDE(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('degs', 8),
        Numeric('mins', 8),
        Numeric('dmins', 16),
        ASCII('direction', 8),
    ]

    time: float
    degs: int
    mins: int
    dmins: int
    direction: str


@dataclass(frozen=True)
class GPS_ALTITUDE(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('altitude', 16),
        Numeric('daltitude', 8),
        ASCII('unit', 8),
    ]

    time: float
    altitude: int
    daltitude: int
    unit: str


@dataclass(frozen=True)
class GPS_INFO(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('num_sats', 8),
        Numeric('quality', 8),
    ]

    time: float
    num_sats: int
    quality: int


@dataclass(frozen=True)
class STREAM_STATUS(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('total_size', 24),
        Numeric('tx_size', 24),
    ]

    time: float
    total_size: int
    tx_size: int


@dataclass(frozen=True)
class STREAM_DATA(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, ASCII('data', 48)]

    time: float
    data: str


@dataclass(frozen=True)
class STREAM_RETRY(ParsleyDataPayload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2]

    time: float


# ── MESSAGES dict & CAN_MESSAGE Switch ──────────────────────────────────────

_PAYLOAD_MAP: dict[str, type[ParsleyDataPayload]] = {
    'GENERAL_BOARD_STATUS': GENERAL_BOARD_STATUS,
    'RESET_CMD': RESET_CMD,
    'DEBUG_RAW': DEBUG_RAW,
    'CONFIG_SET': CONFIG_SET,
    'CONFIG_STATUS': CONFIG_STATUS,
    'ACTUATOR_CMD': ACTUATOR_CMD,
    'ACTUATOR_STATUS': ACTUATOR_STATUS,
    'ALT_ARM_CMD': ALT_ARM_CMD,
    'ALT_ARM_STATUS': ALT_ARM_STATUS,
    'SENSOR_ANALOG16': SENSOR_ANALOG16,
    'SENSOR_ANALOG32': SENSOR_ANALOG32,
    'SENSOR_DEM_ANALOG16': SENSOR_DEM_ANALOG16,
    'GPS_TIMESTAMP': GPS_TIMESTAMP,
    'GPS_LATITUDE': GPS_LATITUDE,
    'GPS_LONGITUDE': GPS_LONGITUDE,
    'GPS_ALTITUDE': GPS_ALTITUDE,
    'GPS_INFO': GPS_INFO,
    'STREAM_STATUS': STREAM_STATUS,
    'STREAM_DATA': STREAM_DATA,
    'STREAM_RETRY': STREAM_RETRY,
}

MESSAGES: dict[str, list[Field]] = {
    name: _SID_HEADER + cls.FIELDS
    for name, cls in _PAYLOAD_MAP.items()
}
# LED messages have no payload
MESSAGES['LEDS_ON'] = list(_SID_HEADER)
MESSAGES['LEDS_OFF'] = list(_SID_HEADER)

CAN_MESSAGE = Switch('msg_type', MESSAGE_TYPE.length, mt.msg_type, MESSAGES)


# ── Factory function ────────────────────────────────────────────────────────

def parse_payload(msg_type: str, bit_str: BitString) -> ParsleyDataPayload | None:
    """Parse a message payload bitstring into a typed dataclass.

    Returns ``None`` for message types with no payload (e.g. LEDS_ON/OFF).
    """
    payload_cls = _PAYLOAD_MAP.get(msg_type)
    if payload_cls is None:
        return None
    return payload_cls.from_bitstring(bit_str)
