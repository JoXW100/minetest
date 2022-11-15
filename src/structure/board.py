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
        size = max(min(9, size), 2)
        self.__size = size
        self.__rows = [[st.BoardCell() for _ in range(size)] for b in range(size)]
    
    @property
    def size(self):
        return self.__size
    
    @property
    def rows(self) -> list[list[st.BoardCell]]:
        return self.__rows
    
    def select(self, loc: st.Location) -> st.Piece:
        """
        Returns the top piece at the given location, or None if the location is 
        invalid or no piece exists at the given location.
        
        Attributes
        ----------
        loc : location.Location
            the location of the piece to flip
        
        Returns
        -------
        piece : piece.Piece
            The top piece at the given location, or None
        """
        
        if not loc.validate(self.size):
            return None
        return self.rows[loc.y][loc.x].top
    
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
        a = st.Location(loc.x, loc.y + 1) # Above
        b = st.Location(loc.x, loc.y - 1) # Below
        r = st.Location(loc.x + 1, loc.y) # Right
        l = st.Location(loc.x - 1, loc.y) # Left
        # Return all locations that are on the board, and pass the given filter 
        return [l for l in [a,b,r,l] if l.validate(self.size) and filter(l)] 
    
    def get_all_locations(self) -> list[st.Location]:
        """
        Creates a list of all the available locations on the board
        
        Returns
        -------
        locs : list[location.Location]
            A list of all the available locations on the board
        """
        return [st.Location(x, y) for x in range(self.size) for y in range(self.size)]
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Board) or self.size != other.size:
            return False
        for (row_a, row_b) in zip(self.rows, other.rows):
            for (cell_a, cell_b) in zip(row_a, row_b):
                if (cell_a != cell_b):
                    return False
        return True
    
    def __str__(self) -> str:
        text = ""
        size = len(self.rows)
        for y in range(size + 2):
            if y == 0:
                for i in range(size):
                    text += '     ' + chr(65 + i)
                text += '\n  ┌' +  '─────┬' * (size - 1) + '─────┐\n'
            elif y == (size + 1):
                text +=   '  └' +  '─────┴' * (size - 1) + '─────┘\n'
            else:
                text += str(y) + ' │ '
                for cell in self.rows[y - 1]:
                    text += str(cell) + ' │ '
                text += '\n' if y == size else '\n  ├' +  '─────┼' * (size - 1) + '─────┤\n'
        return text
