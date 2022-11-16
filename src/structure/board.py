from __future__ import annotations
import structure as st

class Board:
    """
    Represent the Board in the game

    Attributes
    ----------
    size : int
        number of rows and columns in the board
    rows : list[list[cell.BoardCell]]
        the cells in the board
    """

    def __init__(self, size = 5):
        assert(size > 0)
        self.__size = size
        self.__rows = [
            [ st.BoardCell() for x in range(size)] for y in range(size)
        ]
    
    @property
    def size(self):
        return self.__size
    
    @property
    def rows(self) -> list[list[st.BoardCell]]:
        return self.__rows
    
    def select(self, loc: st.Location) -> st.BoardCell:
        """
        Returns the top piece at the given location, or None if the location is 
        invalid or no piece exists at the given location.
        
        Attributes
        ----------
        loc : location.Location
            the location of the piece to flip
        
        Returns
        -------
        cell : BoardCell
            The cell at the given location, or None
        """
        
        if not loc.validate(self.size):
            return None
        return self.rows[loc.y][loc.x]
    
    def get_adjacent(self, loc: st.Location, filter = lambda x: True) -> list[st.Location]:
        """
        Returns all valid adjacent locations to the given location that pass
        the given filter 
        
        Attributes
        ----------
        loc : location.Location
            the location to check
        filter : function
            the filter each location must pass 
        Returns
        -------
        list[Location]
            A list of adjacent locations that pass the given filter
        """
        return [ l for l in 
            [ st.Location(x, y) 
                for x in range(loc.x - 1, loc.x + 2) 
                for y in range(loc.y - 1, loc.y + 2) 
            ] if l != loc and l.validate(self.size) and filter(l)
        ]
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Board) or self.size != other.size:
            return False
        for (row_a, row_b) in zip(self.rows, other.rows):
            for (cell_a, cell_b) in zip(row_a, row_b):
                if cell_a != cell_b:
                    return False
        return True
    
    def __str__(self) -> str:
        text = ""
        for y in range(self.size + 2):
            if y == 0:
                text += ' ┌─' +  '──' * (self.size - 1) + '──┐\n'
            elif y == (self.size + 1):
                text += ' └─' +  '──' * (self.size - 1) + '──┘\n'
            else:
                text += ' │'
                for cell in self.rows[y - 1]:
                    text += ' ' + str(cell)
                text += ' │\n'
        return text
