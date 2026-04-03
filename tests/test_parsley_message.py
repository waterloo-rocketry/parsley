import pytest
from pydantic import ValidationError

from parsley.parsley_message import ParsleyObject, ParsleyError

def test_parsley_error_getitem():
    err = ParsleyError(
        board_type_id='ANY',
        board_inst_id='GROUND',
        msg_type='RESET_CMD',
        msg_metadata=0,
        msg_data='deadbeef',
        error='something went wrong'
    )

    assert err['board_type_id'] == 'ANY'
    assert err['board_inst_id'] == 'GROUND'
    assert err['msg_type'] == 'RESET_CMD'
    assert err['msg_metadata'] == 0
    assert err['msg_data'] == 'deadbeef'
    assert err['error'] == 'something went wrong'


def test_parsley_object_getitem():
    obj = ParsleyObject(
        board_type_id='ANY',
        board_inst_id='GROUND',
        msg_prio='HIGH',
        msg_type='RESET_CMD',
        msg_metadata=0,
        data={}
    )

    assert obj['board_type_id'] == 'ANY'
    assert obj['board_inst_id'] == 'GROUND'
    assert obj['msg_prio'] == 'HIGH'
    assert obj['msg_type'] == 'RESET_CMD'
    assert obj['msg_metadata'] == 0
    assert obj['data'] == {}


def test_parsley_object_unknown_prio_accepted():
    obj = ParsleyObject(
        board_type_id='ANY',
        board_inst_id='GROUND',
        msg_prio='0x03',
        msg_type='RESET_CMD',
        msg_metadata=0,
        data={}
    )
    assert obj['msg_prio'] == '0x03'


def test_parsley_object_empty_prio_raises():
    with pytest.raises(ValidationError):
        ParsleyObject(
            board_type_id='ANY',
            board_inst_id='GROUND',
            msg_prio='',
            msg_type='RESET_CMD',
            msg_metadata=0,
            data={}
        )


def test_parsley_object_metadata_boundary():
    # 0 and 255 are valid (8-bit field), 256 is not
    ParsleyObject(board_type_id='ANY', board_inst_id='GROUND', msg_prio='HIGH', msg_type='RESET_CMD', msg_metadata=0, data={})
    ParsleyObject(board_type_id='ANY', board_inst_id='GROUND', msg_prio='HIGH', msg_type='RESET_CMD', msg_metadata=255, data={})
    with pytest.raises(ValidationError):
        ParsleyObject(
            board_type_id='ANY',
            board_inst_id='GROUND',
            msg_prio='HIGH',
            msg_type='RESET_CMD',
            msg_metadata=256,
            data={}
        )


def test_parsley_object_invalid_type_raises():
    with pytest.raises(ValidationError):
        ParsleyObject(
            board_type_id='ANY',
            board_inst_id='GROUND',
            msg_prio='HIGH',
            msg_type='BAD_TYPE',
            msg_metadata=0,
            data={}
        )

def test_parsley_object_to_flat_dict():
    sensor_data = {
        'time': 40.423, 
        'mag_x': 100, 
        'mag_y': 200
    }

    obj = ParsleyObject(
        board_type_id='PROCESSOR',
        board_inst_id='GENERIC',
        msg_prio='LOW',
        msg_type='RESET_CMD',  
        msg_metadata=10,
        data=sensor_data
    )

    flat = obj.to_flat_dict()

    assert flat['board_type_id'] == 'PROCESSOR'
    assert 'data' not in flat
    assert flat['mag_x'] == 100
    assert len(flat) == 8

def test_parsley_error_to_flat_dict():
    err = ParsleyError(
        board_type_id='GPS',
        board_inst_id='ROCKET',
        msg_type='GPS_ALTITUDE',
        msg_metadata=0x42,
        msg_data='0xFFEEDDCC',
        error='ChecksumMismatch: GPS packet corrupted'
    )
    flat_err = err.to_flat_dict()
    assert flat_err['board_type_id'] == 'GPS'
    assert flat_err['board_inst_id'] == 'ROCKET'
    assert flat_err['msg_type'] == 'GPS_ALTITUDE'
    
    assert 'error' in flat_err
    assert 'msg_data' in flat_err
    
    assert isinstance(flat_err, dict)
    assert len(flat_err) == 6

    