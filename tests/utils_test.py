import pytest

from parsley.bitstring import BitString
from parsley.message_definitions import MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import utils as utilities

def test_create_msg_sid():
	sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'GROUND')

	expected_bytes_len = (MESSAGE_SID.length + 7) // 8 # rounds up to nearest byte

	assert len(sid) == expected_bytes_len

	# expected format: HIGH(0x1) | GENERAL_BOARD_STATUS(0x001) | RLCS_RELAY(0x0C) | GROUND(0x01) | metadata(0x00)
	# prio:  01
	# type:  0000001
	# btype: 001100
	# binst: 000001
	# meta:  00000000
	# padded to 32 bits: 000 01000 00010011 00000001 00000000
	# turns into \x08\x13\x01\x00
	assert sid == b'\x08\x13\x01\x00'
