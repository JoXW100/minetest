from __future__ import annotations
import structure as st

class BoardCell(st.Stack[st.Piece]):
    """
    Represents a board cell containing a stack of pieces.

    Attributes
    ----------
    top : Piece
        The top piece in the cell
    size : int
        The number of pieces in the cell

    Methods
    -------
    put(item : T) -> None
        Adds an piece to the top of the stack
    pop(item : T) -> T
        Removes the top piece of in stack and returns it
    is_empty() -> bool
        Checks if the cell is empty
    """
    @property
    def is_empty(self) -> bool:
        return super().size == 0
    
    def __str__(self) -> str:
        if (self.is_empty):
            return '   '
        else:
            char = 'F' if self.top.state is st.Piece.FLAT else 'S'
            size = str(self.size) if self.size >= 10 else str(self.size) + ' '
            return self.top.owner.color + char + size + st.Color.WHITE