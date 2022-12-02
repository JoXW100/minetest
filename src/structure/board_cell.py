from __future__ import annotations
from enum import Enum
import structure as st

class CellState(Enum):
    Visible = ' '
    Hidden  = '■'
    Flagged = '⚑'
    
MINE_TEXT:str = st.Color.colored_text(st.Color.RED, '○')

class BoardCell:
    """
    Represents a cell on the board.

    Attributes
    ----------
    state : CellState
        The state of the cell
    mined : bool
        If there is a mine in this cell
    location : Location
        The location of this cell in the board
        
    Methods
    -------
    set_mined(state : bool) -> None
        Sets the mined state of the cell
    set_state(state : CellState) -> None
        Sets the visible state of the cell
    """
    def __init__(self, loc: st.Location, board: st.Board):
        self.__state = CellState.Hidden
        self.__mined = False
        self.__location = loc
        self.__board = board
    
    @property 
    def state(self) -> CellState:
        return self.__state
      
    @property 
    def location(self) -> st.Location:
        return self.__location
    
    @property 
    def mined(self) -> bool:
        return self.__mined
    
    def set_mined(self, state: bool = True):
        self.__mined = state
        
    def set_state(self, state: CellState):
        self.__state = state
        
    def __eq__(self, other: object) -> bool:
        return isinstance(other, BoardCell) \
            and self.location == other.location \
            and self.state == other.state \
            and self.mined == other.mined
    
    def __str__(self) -> str:
        if self.mined and self.state is CellState.Visible:
            return MINE_TEXT
        num = len(self.__board.get_neighbors(self.location, lambda x: x.mined))
        if num > 0 and self.state is CellState.Visible:
            return str(num)
        if self.state is CellState.Flagged:
            return st.Color.colored_text(st.Color.YELLOW, self.__state.value)
        return self.__state.value