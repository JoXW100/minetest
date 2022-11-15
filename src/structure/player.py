from __future__ import annotations
import structure as st

COLOR_MAP = [
    st.Color.BLUE,
    st.Color.GREEN,
    st.Color.RED,
    st.Color.YELLOW,
    st.Color.PURPLE,
    st.Color.CYAN
]

class Player:
    """
    Represents a player and handles how they process their turns
    
    Attributes
    ----------
    has_pieces : bool
        True if the player has any pieces left, False otherwise
    color : bool
        The color of the player
    
    Methods
    -------
    get_piece(state : int) -> piece.Piece
        Gets one of the players pieces  
    """
    def __init__(self, identifier: int, pieces: int = 21):
        assert identifier >= 0
        self._identifier = identifier
        self._pieces = pieces
        self._color = COLOR_MAP[identifier % len(COLOR_MAP)]
    
    @staticmethod
    def get_type() -> str:
        return "Player"
    
    @property
    def has_pieces(self) -> bool:
        return self._pieces > 0
    
    @property
    def color(self):
        return self._color
    
    @property
    def pieces(self):
        return self._pieces

    @property
    def identifier(self):
        return self._identifier
    
    @color.setter
    def color(self, color: str):
        self._color = color
    
    def add_pieces(self, num: int):
        self._pieces += num
    
    def get_piece(self, state: int) -> st.Piece:
        """
        Gets one of the players pieces with the given state if it has at least one

        Attributes
        ---------
        state : int
            The state to set the piece as

        Returns
        -------
        piece: piece.Piece
            One of the player's pieces
        """
        if self.has_pieces:
            self._pieces -= 1
            return st.Piece(self, state)
        return None
    
    def perform_turn(self, state : st.GameState):
        raise NotImplementedError
    
    def __str__(self) -> str:
        return st.Color.colored_text(self.color, 'Player #' + str(self._identifier))
    
    def __eq__(self, other):
        return isinstance(other, Player) \
            and self._identifier == other._identifier