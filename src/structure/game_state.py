from __future__ import annotations
from enum import Enum
from collections import deque
from random import randint
import structure as st

class Direction(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

class GameStatus(Enum):
    Won = 0
    Lost = 1
    Playing = 2

class GameState:
    """
    Describes the current state of the game

    Attributes
    ----------
    players : list[player.Player]
        The players in the game
    actions : list[action.Action]
        The actions available for players in the game
    round : int
        The current round
    board : board.Board
        The current board state
    current_player : player.Player
        The player whose turn it is
    ai_difficulty : int
        The difficulty of the AI (0: easy, 1: medium, 2: difficult)
    
    Methods
    -------
    next_round()
        Increments the round counter
    prev_round()
        Decrements the round counter
    is_game_over()
        Checks if the game is over
    get_all_valid_actions()
        Get a list of all available actions in the current game state
    check_line()
        Recursively checks for a line of pieces from the current location to the opposing side.
    """
    DRAW = -2
    PLAYING = -1
    
    def __init__(self, actions: list[st.Action], size: int = 5, mines: int = 0, round: int = 0):
        self.__board = st.Board(size)
        self.__player = st.Player()
        self.__mines = mines
        self.__actions = actions
        self.__selection = st.Location(0, 0)
        self.__round = round
        self.__paused = False

    @property
    def player(self) -> st.Player:
        return self.__player

    @property
    def actions(self) -> list[st.Action]:
        return self.__actions

    @property
    def round(self) -> int:
        return self.__round
        
    @property
    def mines(self) -> int:
        return self.__mines

    @property
    def board(self) -> st.Board:
        return self.__board
    
    @property
    def selection(self) -> st.Location:
        return self.__selection
    
    def next_round(self):
        """
        Increments the round counter
        """
        self.__round += 1

    def prev_round(self):
        """
        Decrements the round counter
        """
        self.__round -= 1

    @property
    def is_paused(self) -> bool:
        return self.__paused
    
    def toggle_pause(self):
        self.__paused = not self.__paused

    def navigate(self, dir: Direction):
        """
        Moves the selection in the given direction

        Attributes
        ----------
        dir : Direction 
            The direction to move
        """
        res = None
        if dir is Direction.Up:
            res = st.Location(self.selection.x, self.selection.y - 1)
        elif dir is Direction.Right:
            res = st.Location(self.selection.x + 1, self.selection.y)
        elif dir is Direction.Down:
            res = st.Location(self.selection.x, self.selection.y + 1)
        elif dir is Direction.Left:
            res = st.Location(self.selection.x - 1, self.selection.y)
        if res.validate(self.board.size):
            self.__selection = res
            
    def __inner_reveal(self, cell: st.BoardCell):
        # Keep track of iterated cells to avoid visiting the same cell multiple 
        # times and getting stuck in a loop
        visited = {cell.location}
        # The pending cells to visit & reveal
        stack = deque([cell])
        while len(stack) > 0:
            # reveal the cell first in the stack
            cell = stack.pop()
            cell.set_state(st.CellState.Visible)
            neighbors = self.board.get_neighbors(cell.location)
            # If no neighboring cell is mined, reveal them.
            if all(not cell.mined for cell in neighbors):
                for cell in neighbors:
                    if cell.location not in visited:
                        visited.add(cell.location)
                        if cell.state is st.CellState.Hidden and not cell.mined:
                            stack.appendleft(cell)
    
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
        cell = self.board.select(loc)
        if cell is None or cell.state is not st.CellState.Hidden:
            return False
        if cell.mined:
            cell.set_state(st.CellState.Visible)
            return True
        else:
            self.__inner_reveal(cell)
            return False
               
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
        cell = self.board.select(loc) 
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
        cells = self.board.get_all_cells()
        while num > 0 and len(cells) > 0:
            i = randint(0, len(cells) - 1)
            cell = cells[i]
            if cell.state is st.CellState.Hidden and not cell.mined:
                num -= 1
                cell.set_mined()
            cells.pop(i)

    def get_game_status(self) -> GameStatus:
        """
        Checks if the game is over
        A player has won if their pieces form a line without diagonals from one opposing side to the other.
        The game is a draw if a player runs out of pieces or the board is full.

        Returns
        -------
        status : GameStatus 
            The status of the current game board
        """
        status = GameStatus.Won
        
        for row in self.board.rows:
            for cell in row:
                # mined cell revealed -> Lost
                if cell.mined and cell.state is st.CellState.Visible:
                    return GameStatus.Lost
                # Not all cells without mines are revealed -> Playing
                if not cell.mined and cell.state is not st.CellState.Visible:
                    status = GameStatus.Playing
        return status
    
    def reveal_mines(self):
        for row in self.board.rows:
            for cell in row:
                if cell.mined:
                    cell.set_state(st.CellState.Visible)
    
    def set_flag_on_mines(self):
        for row in self.board.rows:
            for cell in row:
                if cell.mined:
                    cell.set_state(st.CellState.Flagged)
    
    def print_actions(self):
        text = ""

        if self.is_paused:
            text += "Game is paused!\n\n"

        for action in self.actions:
            # If the game is paused we only print actions that are allowed.
            if not self.is_paused or action.allowed_in_pause:
                text += action.get_name() + '\n'

        print(text)
        
    def __cell_text(self, cell: st.BoardCell) -> str:
        if cell.location == self.selection:
            text = str(cell) if str(cell) != ' ' else '□'
            return st.Color.colored_text(st.Color.GREEN, text)
        return str(cell)
    
    def print_board(self):
        size = self.board.size
        text = ""
        for y in range(size + 2):
            if y == 0:
                text += ' ┌─' +  '──' * (size - 1) + '──┐\n'
            elif y == (size + 1):
                text += ' └─' +  '──' * (size - 1) + '──┘\n'
            else:
                text += ' │'
                for cell in self.board.rows[y - 1]:
                    text += ' ' + self.__cell_text(cell)
                text += ' │\n' 
        print(text)
        
    def get_action(self, key) -> st.Action|None:
        for action in self.actions:
            if action.get_key() == key:
                return action
        return None
    
    def __eq__(self, other: object):
        return isinstance(other, GameState) \
            and self.player == other.player \
            and self.round == other.round \
            and self.mines == other.mines \
            and self.board == other.board