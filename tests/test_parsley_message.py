import pytest
from pydantic import ValidationError

from parsley.parsley_message import ParsleyObject, ParsleyError

def test_parsley_error_getitem():
    err = ParsleyError(
        board_type_id='ANY',
        board_inst_id='GROUND',
        msg_type='RESET_CMD',
        msg_data='deadbeef',
        error='something went wrong'
    )

    assert err['board_type_id'] == 'ANY'
    assert err['msg_data'] == 'deadbeef'
    assert err['error'] == 'something went wrong'


def test_parsley_object_getitem():
    obj = ParsleyObject(
        board_type_id='ANY',
        board_inst_id='GROUND',
        msg_prio='HIGH',
        msg_type='RESET_CMD',
        data={}
    )

    assert obj['board_type_id'] == 'ANY'
    assert obj['msg_prio'] == 'HIGH'
    assert obj['msg_type'] == 'RESET_CMD'
    assert obj['data'] == {}


def test_parsley_object_invalid_prio_raises():
    with pytest.raises(ValidationError):
        ParsleyObject(
            board_type_id='ANY',
            board_inst_id='GROUND',
            msg_prio='BAD_PRIO',
            msg_type='RESET_CMD',
            data={}
        )


def test_parsley_object_invalid_type_raises():
    with pytest.raises(ValidationError):
        ParsleyObject(
            board_type_id='ANY',
            board_inst_id='GROUND',
            msg_prio='HIGH',
            msg_type='BAD_TYPE',
            data={}
        )
