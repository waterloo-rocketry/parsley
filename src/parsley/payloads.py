from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import ClassVar, Self

from parsley.bitstring import BitString
from parsley.fields import ASCII, Enum, Numeric, Bitfield, Field
import parsley.message_types as mt


TIMESTAMP_2 = Numeric('time', 16, scale=1/1000, unit='s')


# ── Base class ──────────────────────────────────────────────────────────────


class Payload:
    """Base class for all typed CAN message payloads.

    Subclasses must define a ``FIELDS`` class variable listing the payload
    :class:`Field` objects in wire order.  The generic :meth:`from_bitstring`
    implementation iterates over ``FIELDS`` to decode a :class:`BitString`
    into the concrete dataclass.
    """

    FIELDS: ClassVar[list[Field]] = []

    time: float

    @classmethod
    def from_bitstring(cls, bit_str: BitString) -> Self:
        kwargs: dict[str, str | int | float] = {}
        for field in cls.FIELDS:
            kwargs[field.name] = field.decode(
                bit_str.pop(field.length, field.variable_length)
            )
        return cls(**kwargs)

    def get_identifier(self) -> str | None:
        return None

    def get_time(self) -> float:
        return self.time

    def to_dict(self) -> dict[str, str | int | float]:
        return asdict(self)  # type: ignore[call-overload]

    def to_bytes(self) -> bytes:
        bit_str = BitString()
        for field in self.FIELDS:
            bit_str.push(*field.encode(getattr(self, field.name)))
        return bytes(bit_str.pop(bit_str.length))


# ── Payload dataclasses ─────────────────────────────────────────────────────


@dataclass(frozen=True)
class GENERAL_BOARD_STATUS(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Bitfield('board_error_bitfield', 32, 'E_NOMINAL', mt.board_error_bitfield_offset),
    ]

    time: float
    board_error_bitfield: str


@dataclass(frozen=True)
class RESET_CMD(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('board_type_id', 8, mt.board_type_id),
        Enum('board_inst_id', 8, mt.board_inst_id),
    ]

    time: float
    board_type_id: str
    board_inst_id: str


@dataclass(frozen=True)
class DEBUG_RAW(Payload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, ASCII('string', 48)]

    time: float
    string: str


@dataclass(frozen=True)
class CONFIG_SET(Payload):
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
class CONFIG_STATUS(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('config_id', 16),
        Numeric('config_value', 16),
    ]

    time: float
    config_id: int
    config_value: int


@dataclass(frozen=True)
class ACTUATOR_CMD(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('cmd_state', 8, mt.actuator_state),
    ]

    time: float
    cmd_state: str


@dataclass(frozen=True)
class ACTUATOR_STATUS(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('cmd_state', 8, mt.actuator_state),
        Enum('curr_state', 8, mt.actuator_state),
    ]

    time: float
    cmd_state: str
    curr_state: str


@dataclass(frozen=True)
class ALT_ARM_CMD(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Enum('alt_arm_state', 8, mt.alt_arm_state),
    ]

    time: float
    alt_arm_state: str


@dataclass(frozen=True)
class ALT_ARM_STATUS(Payload):
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
class SENSOR_ANALOG16(Payload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, Numeric('value', 16)]

    time: float
    value: int


@dataclass(frozen=True)
class SENSOR_ANALOG32(Payload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, Numeric('value', 32)]

    time: float
    value: int


@dataclass(frozen=True)
class SENSOR_2D_ANALOG24(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('value_x', 24),
        Numeric('value_y', 24),
    ]

    time: float
    value_x: int
    value_y: int


@dataclass(frozen=True)
class SENSOR_3D_ANALOG16(Payload):
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
class GPS_TIMESTAMP(Payload):
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
class GPS_LATITUDE(Payload):
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
class GPS_LONGITUDE(Payload):
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
class GPS_ALTITUDE(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('altitude', 32),
        Numeric('daltitude', 8),
    ]

    time: float
    altitude: int
    daltitude: int


@dataclass(frozen=True)
class GPS_INFO(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('num_sats', 8),
        Numeric('quality', 8),
    ]

    time: float
    num_sats: int
    quality: int


@dataclass(frozen=True)
class STREAM_STATUS(Payload):
    FIELDS: ClassVar[list[Field]] = [
        TIMESTAMP_2,
        Numeric('total_size', 24),
        Numeric('tx_size', 24),
    ]

    time: float
    total_size: int
    tx_size: int


@dataclass(frozen=True)
class STREAM_DATA(Payload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2, ASCII('data', 48)]

    time: float
    data: str


@dataclass(frozen=True)
class STREAM_RETRY(Payload):
    FIELDS: ClassVar[list[Field]] = [TIMESTAMP_2]

    time: float


# ── Payload map & factory ──────────────────────────────────────────────────


_PAYLOAD_MAP: dict[str, type[Payload] | None] = {
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
    'SENSOR_2D_ANALOG24': SENSOR_2D_ANALOG24,
    'SENSOR_3D_ANALOG16': SENSOR_3D_ANALOG16,
    'GPS_TIMESTAMP': GPS_TIMESTAMP,
    'GPS_LATITUDE': GPS_LATITUDE,
    'GPS_LONGITUDE': GPS_LONGITUDE,
    'GPS_ALTITUDE': GPS_ALTITUDE,
    'GPS_INFO': GPS_INFO,
    'STREAM_STATUS': STREAM_STATUS,
    'STREAM_DATA': STREAM_DATA,
    'STREAM_RETRY': STREAM_RETRY,
    'LEDS_ON': None,
    'LEDS_OFF': None,
}


def get_payload_type(msg_type: str) -> type[Payload] | None:
    """Return the payload class for a message type, or None for empty payloads.

    Raises ``ValueError`` for unknown message types.
    """
    try:
        return _PAYLOAD_MAP[msg_type]
    except KeyError:
        raise ValueError(f"Unknown message type: {msg_type}")
