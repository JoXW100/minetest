from __future__ import annotations
from typing import Callable
from collections import deque
from random import randint
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
            [ st.BoardCell(st.Location(x,y), self) for x in range(size)
            ] for y in range(size)
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
    
    def get_neighbors(self, loc: st.Location, filter: Callable[[st.BoardCell], bool] = lambda x: True) -> list[st.BoardCell]:
        """
        Returns all valid neighboring cells (8) to the given location that pass
        the given filter 
        
        Attributes
        ----------
        loc : Location
            the location to find surrounding tiles
        filter : callable(BoardCell) -> Bool
            the filter each location must pass 
        Returns
        -------
        list[BoardCell]
            A list of neighboring cells that pass the given filter
        """  
        return [ self.rows[l.y][l.x] for l in 
            [ st.Location(x, y) 
                for x in range(loc.x - 1, loc.x + 2) 
                for y in range(loc.y - 1, loc.y + 2) 
            ] if l != loc 
            and l.validate(self.size) 
            and filter(self.rows[l.y][l.x])
        ]
    
    
    def get_all_cells(self) -> list[st.BoardCell]:
        """
        Creates a list of all the locations on the board
        
        Returns
        -------
        locs : list[Location]
            A list of all the locations on the board
        """
        return [self.rows[y][x] for x in range(self.size) for y in range(self.size)]

    def __inner_reveal(self, cell: st.BoardCell):
        visited = {cell.location}
        stack = deque([cell])
        while len(stack) > 0:
            cell = stack.pop()
            cell.set_state(st.CellState.Visible)
            neighbors = self.get_neighbors(cell.location)
            if len([x for x in neighbors if x.mined]) == 0:
                for adj in neighbors:
                    if adj.location not in visited:
                        visited.add(adj.location)
                        if adj.state is st.CellState.Hidden and not adj.mined:
                            stack.appendleft(adj)
    
    def reveal_cell(self, loc: st.Location) -> bool:
        """
        Reveals the cell at the given location if it is hidden. Reveals all
        other hidden cells connected to it if they are not mined.
        
        Attributes
        ----------
        loc : Location
            the location of the cell reveal
        
        Returns
        -------
        mined : bool
            If the revealed cell was mined
        """
        cell = self.select(loc)
        if cell is None:
            return False
        self.__inner_reveal(cell)
        return cell.mined
               
    def reveal_and_distribute(self, loc: st.Location, num: int) -> bool:
        """
        Reveals the cell at the given location if it is hidden and not mined. 
        Distributes mines on other hidden cells on the board and reveals other 
        hidden cells connected to the cell at the given location if they are 
        not mined.
        
        Attributes
        ----------
        loc : Location
            the location of the cell reveal
        num : int
            the number of mines to distribute
        
        Returns
        -------
        success : bool
            If the cell at the given location could be revealed
        """
        cell = self.select(loc) 
        if cell is None or cell.state is not st.CellState.Hidden or cell.mined:
            return False
        cell.set_state(st.CellState.Visible)
        self.distribute_mines(num)
        self.__inner_reveal(cell)
        return True
     
    def distribute_mines(self, num: int):
        """
        Distributes up to the given number of mines on board cells randomly. 
        
        Attributes
        ----------
        num : int
            the number of mines to distribute
        """
        cells = self.get_all_cells()
        while num > 0 and len(cells) > 0:
            i = randint(0, len(cells) - 1)
            cell = cells[i]
            if cell.state is st.CellState.Hidden and not cell.mined:
                num -= 1
                cell.set_mined()
            cells.pop(i)
    
    def __eq__(self, other: object) -> bool:
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
