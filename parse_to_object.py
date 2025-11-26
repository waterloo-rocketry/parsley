'''
Contains the new static class implementation of Parsley.py
'''

#MAKE A DECISION BETWEEN STATIC METHOD OR CLASS METHOD MYSELF

from sre_parse import parse
from typing import Tuple
from parsley.parsley_message import ParsleyObject, ParsleyError
from parsley.bitstring import BitString
from parsley.message_definitions import CAN_MESSAGE, MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import parsley.parse_utils as pu
from typing import List, TypeVar, Union, Iterator
from parsley.fields import Field, Switch, Bitfield
from abc import ABC, abstractmethod

T = TypeVar("T")

class _ParsleyParseInternal:
    def __init__(self):
        raise NotImplementedError("This class is static-only")
    
    
    @staticmethod
    def _parse_fields(bit_str: BitString, fields: List[Field]) -> dict[str, T]:
        res: dict[str, T] = {}
        for field in fields:
            data = bit_str.pop(field.length, field.variable_length)
            res[field.name] = field.decode(data)
            if isinstance(field, Switch):
                nested_fields = field.get_fields(res[field.name])
                res.update(_ParsleyParseInternal._parse_fields(bit_str, nested_fields))
            if isinstance(field, Bitfield):
                res[field.name] = field.decode(data)
        return res

    @staticmethod
    def _parse_board_type_id(encoded_board_type_id: bytes) -> dict:
        board_type_id = None
        try:
            board_type_id = BOARD_TYPE_ID.decode(encoded_board_type_id)
        except ValueError:
            board_type_id = pu.hexify(encoded_board_type_id)
        return board_type_id

    @staticmethod
    def _parse_board_inst_id(encoded_board_inst_id: bytes) -> str:
        board_inst_id = None
        try:
            board_inst_id = BOARD_INST_ID.decode(encoded_board_inst_id)
        except ValueError:
            board_inst_id = pu.hexify(encoded_board_inst_id)
        return board_inst_id

    @staticmethod
    def parse_to_object(msg_sid: bytes, msg_data: bytes) -> Union[ParsleyObject, ParsleyError]:
        """Parse msg_sid and msg_data into a ParsleyObject."""
        
        # begin parsing
        bit_str_msg_sid = BitString(msg_sid, MESSAGE_SID.length)
        encoded_msg_prio = bit_str_msg_sid.pop(MESSAGE_PRIO.length)
        encoded_msg_type = bit_str_msg_sid.pop(MESSAGE_TYPE.length)
        bit_str_msg_sid.pop(2)  # reserved field
        encoded_board_type_id = bit_str_msg_sid.pop(BOARD_TYPE_ID.length)
        encoded_board_inst_id = bit_str_msg_sid.pop(BOARD_INST_ID.length)

        board_type_id = _ParsleyParseInternal._parse_board_type_id(encoded_board_type_id)
        board_inst_id = _ParsleyParseInternal._parse_board_inst_id(encoded_board_inst_id)

        msg_prio = ''
        msg_type = ''
        data: T = {} 

        try:
            msg_prio = MESSAGE_PRIO.decode(encoded_msg_prio)
            msg_type = MESSAGE_TYPE.decode(encoded_msg_type)
            # we splice the first element since we've already manually parsed BOARD_ID
            # if BOARD_ID threw an error, we want to try and parse the rest of the CAN message
            fields = CAN_MESSAGE.get_fields(msg_type)[3:]
            data = _ParsleyParseInternal._parse_fields(BitString(msg_data), fields)
        except (ValueError, IndexError) as error:
            # convert the 6-bit msg_type into its canlib 12-bit form and include an error object
            # raise ValueError(f"Failed to parse CAN message type {pu.hexify(encoded_msg_type, is_msg_type=True)}: {error}") from error WANTED A THROWN ERROR?
            return ParsleyError(
                msg_type=pu.hexify(encoded_msg_type, is_msg_type=True),
                msg_data =pu.hexify(msg_data),
                error=str(error)
            )
            
        return ParsleyObject(
            msg_prio=msg_prio,
            msg_type=msg_type,
            board_type_id=board_type_id,
            board_inst_id=board_inst_id,
            data=data,
        )