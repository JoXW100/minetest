from __future__ import annotations
import os
from enum import Enum
from collections import deque
from random import randint
import structure as st
from utils import pad_list

class PrintConfig(Enum):
    """Class representing board and actions printing configuration"""
    Vertical = 0
    Horizontal = 1
    NoneFits = 2

class Direction(Enum):
    """Class representing directions"""
    Up = 0
    Right = 1
    Down = 2
    Left = 3

class GameStatus(Enum):
    """Class representing game states"""
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

    @property
    def is_paused(self) -> bool:
        return self.__paused

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

    def set_selection(self, loc: st.Location) -> bool:
        """
        Move the current selection on the board to a new location
        
        Attributes
        ----------
        loc : st.Location
            The new location to move the selection to
        Returns
        -------
        successful : bool
            If the move was successful or not
        """
        if loc.validate(self.board.size):
            self.__selection = loc
            return True
        return False

    def toggle_pause(self):
        """
        Toggles the paused state of the game
        """
        self.__paused = not self.__paused

    def navigate(self, dir: Direction):
        """
        Moves the selection in the given direction

        Attributes
        ----------
        dir : Direction 
            The direction to move the selection in
        """
        res = self.selection
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
        """
        This method is used by the :func:`reveal_cell` method on a cell not containing
        a mine to recursively reveal that cell's neighbors that also do not
        contain any mines.
        """

        # Keep track of iterated cells to avoid visiting the same cell multiple 
        # times and getting stuck in a loop.
        visited = {cell.location}
        # The pending cells to visit & reveal
        stack = deque([cell])
        while len(stack) > 0:
            # Reveal the first cell in the stack
            cell = stack.pop()
            cell.set_state(st.CellState.Visible)
            neighbors = self.board.get_neighbors(cell.location)
            # If no neighboring cell is mined, reveal them
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
        If the cell is visible and the number of flagged neighbors equals the number of mined neighbors,
        all non-flagged neighbors are revealed.
        
        Attributes
        ----------
        loc : Location
            the location of the cell reveal
        
        Returns
        -------
        mined : bool
            If a revealed cell was mined
        """
        cell = self.board.select(loc)
        if cell is None or cell.state is st.CellState.Flagged:
            return False
        
        # If the cell is mined, reveal it and return True.
        if cell.mined:
            cell.set_state(st.CellState.Visible)
            return True
        
        # If the cell is hidden,
        # reveal it and all other hidden cells connected to it if they are not mined.
        elif cell.state is st.CellState.Hidden:
            self.__inner_reveal(cell)
            return False 
        
        # If the cell is visible and the number of flagged neighbors equals
        # the number of mined neighbors, reveal all non-flagged neighbors.
        else:
            # Get the number of flagged and mined neighbors
            neighbors = self.board.get_neighbors(cell.location)
            flagged_neighbors = len([n for n in neighbors if n.state is st.CellState.Flagged])
            mined_neighbors = len([n for n in neighbors if n.mined])
            
            # Reveal all non-flagged neighbors if the number of flagged neighbors
            # equals the number of mined neighbors
            return mined_neighbors > 0 and flagged_neighbors == mined_neighbors \
                and any([n.state is st.CellState.Hidden and self.reveal_cell(n.location) for n in neighbors])

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
        A player has won if their pieces form a line without diagonals from one
        opposing side to the other. The game is a draw if a player runs out of
        pieces or the board is full.

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
        """
        Reveals all the mines on the board by setting their state to visible.
        """
        for row in self.board.rows:
            for cell in row:
                if cell.mined:
                    cell.set_state(st.CellState.Visible)

    def set_flag_on_mines(self):
        """
        Sets all the mines on the board to be flagged.
        """
        for row in self.board.rows:
            for cell in row:
                if cell.mined:
                    cell.set_state(st.CellState.Flagged)

    def __get_print_actions_strings(self) -> [str]:
        """
        Collects the strings for all possible actions into a list for printing

        Returns
        -------
        action_strings : [str] 
            A list of all possible actions to play given the current game state
        """
        strings = []

        if self.is_paused:
            strings.append("Game is paused!")

        for action in self.actions:
            # If the game is paused we only add actions that are allowed to be
            # performed when paused
            if not self.is_paused or action.allowed_in_pause:
                strings.append(action.get_name())

        return strings

    def print_actions(self):
        """
        Prints all the possible actions available to the user at the current
        time
        """
        for action_str in self.__get_print_actions_strings():
            print(action_str)

    def __cell_text(self, cell: st.BoardCell) -> str:
        cell_str = str(cell)

        # Replace the cell color with "selected" color if the cell is selected.
        if cell.location == self.selection:
            text = cell_str if cell_str != ' ' else '□'
            text = st.Color.remove_color(text)
            return st.Color.colored_text(st.ColorScheme.get_color("selected"), text)

        return cell_str

    def print_board(self, print_actions = False):
        """
        Prints the board to the terminal

        Attributes
        ----------
        and_actions : Bool
            If the actions should be printed alongside the board
        """
        size = self.board.size
        print_range = size + 2
        action_strings = self.__get_print_actions_strings()
        text = ""

        padded_action_strings = pad_list(
            action_strings, None, 1, (print_range - len(action_strings)))

        for (y, action_str) in zip(range(print_range), padded_action_strings):
            if y == 0:
                text += ' ┌─' +  '──' * (size - 1) + '──┐'
            elif y == (size + 1):
                text += ' └─' +  '──' * (size - 1) + '──┘'
            else:
                text += ' │'
                for cell in self.board.rows[y - 1]:
                    text += ' ' + self.__cell_text(cell)
                text += ' │'

            # Add action to the end of the line if printing them
            if print_actions and (action_str is not None and y != 0):
                text += " " + action_str

            text += "\n"

        print(text, end = "")

    def print_resize_prompt(self):
        """
        Prints a resize prompt for when the board and actions cannot be printed
        legibly
        """
        # Find exit action key and print error message
        exit_action_key = None
        for action in self.actions:
            if "exit" in action.get_name().lower():
                exit_action_key = str(action.get_key())

        text = "Terminal too small. Resize and refresh by" + \
            " pressing a key"

        if exit_action_key is not None:
            text += f" or exit by pressing [{exit_action_key}]"

        print(text)

    def __get_suitable_print_config(self) -> PrintConfig:
        """
        Returns the most suitable print configuration depending on the size of
        the terminal

        Returns
        -------
        configuration : PrintConfig
           The most suitable print configuration
        """
        # Get size of the terminal window.
        (_, t_lines) = os.get_terminal_size()
        board_print_size = self.board.size + 1
        blank_lines = 2 # One blank lines below the board and one below actions

        if (board_print_size + len(self.actions) + blank_lines) > t_lines:
            # Check if we are able to either print all actions or that the total
            # print board size fits on the window.
            if len(self.actions) < board_print_size <= t_lines:
                return PrintConfig.Horizontal

            return PrintConfig.NoneFits
        else:
            return PrintConfig.Vertical


    def print_board_and_actions(self):
        """
        Prints the board and all possible actions to the terminal
        """
        print_config = self.__get_suitable_print_config()

        if print_config == PrintConfig.Vertical:
            self.print_board()
            self.print_actions()
        elif print_config == PrintConfig.Horizontal:
            self.print_board(print_actions = True)
        elif print_config == PrintConfig.NoneFits:
            self.print_resize_prompt()

    def get_action(self, key: str) -> st.Action|None:
        """
        Gets the action corresponding to character representing a key press.
        
        Attributes
        ----------
        key : str
            The key (character) corresponding to the action to be played
        Returns
        -------
        action : st.Action|None
           Returns the corresponding action if there is one, otherwise None
        """
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
