from dataclasses import dataclass
from typing import Literal, Generic, TypeVar
from pydantic import BaseModel, field_validator
import parsley.message_types as mt

T = TypeVar("T")

BoardTypeID = str
BoardInstID = str
MsgPrio = str #will be checked during runtime
MsgType = str #will be checked during runtime

#I CAN ALSO CREATE AN ENUM BUT I THINK THAT THIS METHOD BETTER FOR ACTUAL IMPLMENET RUNTIME
@dataclass
class ParsleyError():
    """Custom exception class for Parsley errors."""
    msg_type: str
    msg_data: str
    error: str
    
class ParsleyObject(BaseModel, Generic[T]):
    """
    Dataclass to store parsed CAN message data.
    """

    board_type_id: BoardTypeID
    board_inst_id: BoardInstID
    msg_prio: MsgPrio
    msg_type: MsgType
    data: T # ParsleyDataType

    @field_validator("msg_prio")
    def validate_msg_prio(cls, value):
        if value not in mt.msg_prio:
            raise ValueError(f"Invalid msg_prio type '{value}'")
        return value
    
    @field_validator("msg_type")
    def validate_msg_type(cls, value):
        if value not in mt.msg_type:
            raise ValueError(f"Invalid msg_type type '{value}'")
        return value

    #confirm deletion with Chris as it only works with other Parsley Objects, cause you can always just run model dump.
    '''   
    def __eq__(self, other: object) -> bool: #allows comparison to dicts
        if isinstance(other, dict):
            isSame = True
            
            if self.board_type_id != other.get('board_type_id'):
                isSame = False
            if self.board_inst_id != other.get('board_inst_id'):
                isSame = False
            if self.msg_prio != other.get('msg_prio'):
                isSame = False
            if self.msg_type != other.get('msg_type'):
                isSame = False
            if self.data != other.get('data'):
                isSame = False
                
            return isSame
        
        if isinstance(other, ParsleyObject):
            isSame = True
            
            if self.board_type_id != other.board_type_id:
                isSame = False
            if self.board_inst_id != other.board_inst_id:
                isSame = False
            if self.msg_prio != other.msg_prio:
                isSame = False
            if self.msg_type != other.msg_type:
                isSame = False
            if self.data != other.data:
                isSame = False
                
            return isSame
    '''
    
    def __getitem__(self, key: str):        
        return self.model_dump()[key]  
    
if __name__ == "__main__":
    testing = ParsleyObject(
        msg_prio="HIGHEST",
        msg_type="GENERAL_BOARD_STATUS",
        board_type_id="ID 1",
        board_inst_id="Board ID 2",
        data="Yo yo honey singh",
    )
    
    testing2 = ParsleyObject(
        msg_prio="HIGHEST",
        msg_type="GENERAL_BOARD_STATUS",
        board_type_id="ID 1",
        board_inst_id="Board ID 2",
        data="Yo yo honey singh",
    )
    
    testing3 = ParsleyObject(
        msg_prio="LOW",
        msg_type="GENERAL_BOARD_STATUS",
        board_type_id="ID 1",
        board_inst_id="Board ID 2",
        data="Yo yo honey singh",
    )
    
    if (testing == testing2):
        print("GAY")
    else:
        print("NAh I'd win")
        
    if (testing == testing3):
        print("Peepeepoopoo")
    else:
        print("NAh I'd win")
        
    if (testing["data"] == testing2["data"]):
        print("GAY")
    else:
        print("NAh I'd win")
        
    if (testing3["data"] == testing2["data"]):
        print("GAY")
    else:
        print("NAh I'd win")
        
    print("peppepepeppepepep")
