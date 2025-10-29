import pytest

from parsley.bitstring import BitString
from parsley.message_definitions import MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import utils as utilities

def test_create_msg_sid():	
	sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'PRIMARY')
	
	expected_bytes_len = (MESSAGE_SID.length + 7) // 8 # rounds up to nearest byte
 
	assert len(sid) == expected_bytes_len

	# expected format: HIGH(0x1) | GENERAL_BOARD_STATUS(0x001) | reserved(0x0) | RLCS_RELAY(0x81) | PRIMARY(0x04)
	# value:                01   |      000000001              |  00           |      10000001    |    00000100
	#     padding + 01000 00000100 10000001 00000100
 	# turns into \x08\x04\x81\x04
	assert sid == b'\x08\x04\x81\x04'
