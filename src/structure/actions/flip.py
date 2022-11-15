from structure import Action, GameState, Piece, Location
import helpers

class Flip(Action):
    """
    Flips a piece on the board if it is valid. Piece has to belong to the owner
    """
    @staticmethod
    def get_name():
        return "Flip"
    
    @staticmethod
    def check(state: GameState, loc: Location) -> bool:
        if not loc.validate(state.board.size):
            return False
        cell = state.board.rows[loc.y][loc.x]
        return not cell.is_empty and cell.top.owner == state.current_player
        
    @staticmethod
    def execute(state: GameState, loc: Location) -> int:
        if Flip.check(state, loc):
            Flip.unsafe_execute(state, loc)
            return Action.SUCCEEDED
        return Action.FAILED
    
    @staticmethod
    def unsafe_execute(state: GameState, loc: Location):
        cell = state.board.rows[loc.y][loc.x]
        cell.top.state = Piece.STANDING if cell.top.state is Piece.FLAT else Piece.FLAT

    @staticmethod
    def undo(state: GameState, loc: Location):
        Flip.unsafe_execute(state, loc)

    @staticmethod
    def ask_args(state: GameState) -> list[any]:
        loc = helpers.get_location(state)
        return [loc]
    
    @staticmethod
    def get_args(state: GameState) -> list[list[any]]:
        valid_locations = []
        for loc in state.board.get_all_locations():
            cell = state.board.rows[loc.y][loc.x]
            if not cell.is_empty and cell.top.owner == state.current_player:
                valid_locations.append([loc])
        return valid_locations
    
    @staticmethod
    def to_str(loc: Location):
        return "Flip piece at " + str(loc)