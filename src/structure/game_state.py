from __future__ import annotations
from enum import Enum
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
                    text += ' ' + (st.Color.colored_text(st.Color.GREEN, str(cell)) \
                        if cell.location == self.selection else str(cell)) 
                text += ' │\n' 
        print(text)
        
    def get_action(self, key) -> st.Action:
        try:
            print("input: " + str(key))
            print("code:" + str(key.char))
            if key.char == "q":
                print("q was pressed")
                return None
        except AttributeError:
            pass
    
    def __eq__(self, other: object):
        return isinstance(other, GameState) \
            and self.player == other.player \
            and self.round == other.round \
            and self.mines == other.mines \
            and self.board == other.board