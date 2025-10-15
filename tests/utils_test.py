import pytest

from parsley.bitstring import BitString
from parsley.message_definitions import MESSAGE_PRIO, MESSAGE_TYPE, BOARD_TYPE_ID, BOARD_INST_ID, MESSAGE_SID
import utils as utilities

def test_create_msg_sid():	
	sid = utilities.create_msg_sid_from_strings('HIGH', 'GENERAL_BOARD_STATUS', '0', 'RLCS_RELAY', 'PRIMARY')
	
	expected_bytes_len = (MESSAGE_SID.length + 7) // 8 # rounds up to nearest byte
 
	assert len(sid) == expected_bytes_len

	bs = BitString(sid, MESSAGE_SID.length)
	encoded_prio = bs.pop(MESSAGE_PRIO.length)
	encoded_type = bs.pop(MESSAGE_TYPE.length)
	bs.pop(2)
	encoded_board_type = bs.pop(BOARD_TYPE_ID.length)
	encoded_board_inst = bs.pop(BOARD_INST_ID.length)

	assert MESSAGE_PRIO.decode(encoded_prio) == 'HIGH'
	assert MESSAGE_TYPE.decode(encoded_type) == 'GENERAL_BOARD_STATUS'
	assert BOARD_TYPE_ID.decode(encoded_board_type) == 'RLCS_RELAY'
	assert BOARD_INST_ID.decode(encoded_board_inst) == 'PRIMARY'
