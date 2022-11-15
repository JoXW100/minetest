from __future__ import annotations
import structure as st

class Piece:
    """
    A class used to represent a piece in the game

    Attributes
    ----------
    FLAT : int
    STANDING : int
    owner : Player
        the owner of the piece
    state : int
        the state of the piece, standing (1) or flat (0)
    """
    FLAT = 0
    STANDING = 1
    
    def __init__(self, owner: st.Player, state: int):
        self.__owner = owner
        self.__state = state
        
    @property
    def owner(self) -> st.Player:
        return self.__owner
    
    @property
    def state(self) -> int:
        return self.__state
    
    @state.setter
    def state(self, state: int):
        self.__state = state
        
    def __eq__(self, other):
        return isinstance(other, Piece) \
            and self.owner == other.owner \
            and self.state == other.state
    
        