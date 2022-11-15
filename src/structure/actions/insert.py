from structure import Action, GameState, Location, Piece
import helpers

class Insert(Action):
    """
    Inserts a piece to the board
    """
    @staticmethod
    def get_name():
        return "Insert"
    
    @staticmethod
    def check(state: GameState, loc: Location, piece_state: int) -> bool:
        if not loc.validate(state.board.size) or not state.current_player.has_pieces:
            return False
        cell = state.board.rows[loc.y][loc.x]
        return cell.is_empty or cell.top.state != Piece.STANDING
        
    @staticmethod
    def execute(state: GameState, loc: Location, piece_state: int) -> int:
        if Insert.check(state, loc, piece_state):
            Insert.unsafe_execute(state, loc, piece_state)
            return Action.SUCCEEDED
        return Action.FAILED
    
    @staticmethod
    def unsafe_execute(state: GameState, loc: Location, piece_state: int):
        cell = state.board.rows[loc.y][loc.x]
        cell.put(state.current_player.get_piece(piece_state))
    
    @staticmethod
    def undo(state: GameState, loc: Location, piece_state: int):
        state.board.rows[loc.y][loc.x].pop()
        state.current_player.add_pieces(1)

    @staticmethod
    def ask_args(state: GameState) -> list[any]:
        if not state.current_player.has_pieces:
            print("Failed to insert piece, no pieces left")
            return [loc.Location(-1, -1), loc.Location(-1, -1)]
        piece_state = 0
        while True:
            value = input("Enter piece state (S = Standing, F = Flat): ").lower()
            if (value == 's'):
                piece_state = Piece.STANDING
                break
            elif (value == 'f'):
                piece_state = Piece.FLAT
                break
            else:
                print("Invalid state, enter 'S', or 'F'")
        loc = helpers.get_location(state)
        return [loc, piece_state]
    
    @staticmethod
    def get_args(state: GameState) -> list[list[any]]:
        args = []
        locations = state.board.get_all_locations()
        if state.current_player.has_pieces:
            for loc in locations:
                cell = state.board.rows[loc.y][loc.x]
                if cell.is_empty or cell.top.state != Piece.STANDING:
                    args.append([loc, Piece.FLAT])
                    args.append([loc, Piece.STANDING])
        return args
    
    @staticmethod
    def to_str(loc: Location, piece_state: int):
        return "Insert " + ('flat' if piece_state is Piece.FLAT else 'standing') + " piece at " + str(loc)