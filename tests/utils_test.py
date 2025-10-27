import pytest

from parsley.bitstring import BitString
from parsley.message_definitions import MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import utils as utilities

def test_create_msg_sid():	
	sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'PRIMARY')
	
	expected_bytes_len = (MESSAGE_SID.length + 7) // 8 # rounds up to nearest byte
 
	assert len(sid) == expected_bytes_len

	assert sid == b'\x08\x04\x81\x04'