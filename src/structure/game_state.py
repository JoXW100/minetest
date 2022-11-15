from __future__ import annotations
import structure as st

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
    
    def __init__(self, players: list[st.Player], actions: list[st.Action], size: int = 5, difficulty: int = 1, round: int = 0):
        self.__board = st.Board(size)
        self.__players = players
        self.__actions = actions
        self.__difficulty = difficulty
        self.__round = round

    @property
    def players(self) -> list[st.Player]:
        return self.__players

    @property
    def actions(self) -> list[st.Action]:
        return self.__actions

    @property
    def round(self) -> int:
        return self.__round
        
    @property
    def ai_difficulty(self) -> int:
        return self.__difficulty

    @property
    def board(self) -> board.Board:
        return self.__board

    @property
    def current_player(self) -> st.Player|None:
        """
        Returns the current player
        """
        return self.__players[self.__round % len(self.__players)] if len(self.__players) > 0 else None

    def overwrite(self, state: GameState):
        """
        Replaces the game state values with that of another game state
        """
        self.__board = state.__board
        self.__players = state.__players
        self.__actions = state.__actions
        self.__difficulty = state.__difficulty
        self.__round = state.__round
    
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

    def is_game_over(self) -> int:
        """
        Checks if the game is over
        A player has won if their pieces form a line without diagonals from one opposing side to the other.
        The game is a draw if a player runs out of pieces or the board is full.

        Returns
        -------
        int:
            identifier for player that has won (0-1), draw (2) or game not over (-1)
        """
        # Start counting from left and top
        for n in range(self.board.size):
            # Top
            top_loc = st.Location(n, 0)
            if self.check_line(top_loc, top_loc, top_loc):
                # Get the owner of the piece at the top location
                return self.board.select(top_loc).owner.identifier

            # Left
            left_loc = st.Location(0, n)
            if self.check_line(left_loc, left_loc, left_loc):
                # Get the owner of the piece at the left location
                return self.board.select(left_loc).owner.identifier

        # Check if any player is out of pieces (DRAW)
        for p in self.players:
            if p.pieces == 0:
                return GameState.DRAW

        # Check if all locations on the board contain standing pieces (DRAW)
        no_playable_cells = True
        for x in range(self.board.size):
            for y in range(self.board.size):
                piece = self.board.select(st.Location(x, y))
                if piece is None or piece.state == 0:
                    no_playable_cells = False
                    break

        # Game is not over if there are positions with flat pieces
        if no_playable_cells:
            return GameState.DRAW
        else:
            return GameState.PLAYING

    def _valid_cell(self, owner: st.Player, state: int, loc: st.Location):
        cell = self.board.rows[loc.y][loc.x]
        return not cell.is_empty and cell.top.owner == owner and cell.top.state == state
    
    def check_line(self, start: st.Location, currLoc: st.Location, prevLoc: st.Location, turns: int = 0) -> bool:
        """
        Recursively checks for a line of pieces from the current location to the opposing side.

        Parameters
        ----------
        start: location.Location
            The start location
        currLoc : location.Location
            The current location
        prevLoc : location.Location
            The previous location
        turns : int
            The number of turns the line has made

        Returns
        -------
        bool
            True if a line is found, False otherwise
        """
        cell = self.board.rows[currLoc.y][currLoc.x]
        if cell.is_empty:
            return False
        # Adjacent locations with pieces with the same owner and same state
        nextLocs = self.board.get_adjacent(currLoc, \
            lambda x: self._valid_cell(cell.top.owner, cell.top.state, x))
        for nextLoc in nextLocs:
            if nextLoc == prevLoc:
                continue
            local_turns = turns # turns if the next location is nextLoc
            if start != currLoc:
                # If the previous and current location has the same x or y 
                # coordinate and the next location has a different 
                # respective value, this will form a turn.
                if (currLoc.x == prevLoc.x and currLoc.x != nextLoc.x) \
                or (currLoc.y == prevLoc.y and currLoc.y != nextLoc.y):
                    local_turns += 1
                # A valid line can only turn twice 
                if local_turns > 2:
                    continue
            # If on the other side of the board than the start location
            # or part of a line that ends on the other side.
            if (start.x == 0 and nextLoc.x == self.board.size - 1) \
            or (start.y == 0 and nextLoc.y == self.board.size - 1)\
            or self.check_line(start, nextLoc, currLoc, local_turns):
                return True
        # The line did not end at the other side of the board
        return False

    def get_all_valid_actions(self) -> list[tuple[st.Action, list[any]]]:
        """
        Gets all valid actions for for the current game state

        Returns
        -------
        actions : list[action.Action]
            A list of all available actions
        """
        possible_actions = []
        for action in self.actions:
            possible_args = action.get_args(self)
            for args in possible_args:
                possible_actions.append((action, args))
        return possible_actions

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        if len(self.players) != len(other.players):
            return False
        for (a, b) in zip(self.players, other.players):
            if a != b:
                return False
        return self.round == other.round and self.board == other.board