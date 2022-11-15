from structure.actions import Move
from structure import GameState, BoardCell, Location, Piece, Player

IN_LOCATION = Location(-1,-1) #Invalid location
A1_LOCATION = Location(0,0)
A2_LOCATION = Location(0,1)
A3_LOCATION = Location(0,2)
B1_LOCATION = Location(1,0)
B2_LOCATION = Location(1,1)
B3_LOCATION = Location(1,2)

def get_cell(state: GameState, loc: Location) -> BoardCell:
    return state.board.rows[loc.y][loc.x]

def insert(state: GameState, piece: Piece, loc: Location):
    state.board.rows[loc.y][loc.x].put(piece)

def test_move_get_name():
    """
    The get_name function returns a string
    """
    assert type(Move.get_name()) == str 
    assert len(Move.get_name()) > 0

def test_move_single_check():
    """
    Tests the move check function for various edge cases when moving a single 
    piece
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), B1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), B2_LOCATION)
    # No destinations are provided:
    assert Move.check(state, A1_LOCATION, []) is False
    # Source outside board:
    assert Move.check(state, IN_LOCATION, [A1_LOCATION]) is False
    # Destination outside board
    assert Move.check(state, A1_LOCATION, [IN_LOCATION]) is False
    # Move from empty cell to empty cell
    assert Move.check(state, A2_LOCATION, [B3_LOCATION]) is False
    # Move from empty cell
    assert Move.check(state, A2_LOCATION, [B2_LOCATION]) is False
    # Move from source to itself
    assert Move.check(state, A1_LOCATION, [A1_LOCATION]) is False
    # Valid onto empty cell
    assert Move.check(state, A1_LOCATION, [A2_LOCATION]) is True
    # Move onto standing piece
    assert Move.check(state, A1_LOCATION, [B1_LOCATION]) is False
    # Move onto flat piece
    assert Move.check(state, A1_LOCATION, [B2_LOCATION]) is True

def test_move_multiple_check():
    """
    Tests the move check function for various edge cases when moving multiple 
    pieces
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    # 3 pieces in A0
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), B1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), B2_LOCATION)
    # No destinations are provided:
    assert Move.check(state, A1_LOCATION, []) is False
    # Source outside board:
    assert Move.check(state, IN_LOCATION, [A1_LOCATION, A2_LOCATION]) is False
    # Destination outside board
    assert Move.check(state, A1_LOCATION, [IN_LOCATION, IN_LOCATION]) is False
    # Move from empty cell to empty cells
    assert Move.check(state, A2_LOCATION, [B3_LOCATION, B3_LOCATION]) is False
    # Move from empty cell
    assert Move.check(state, A2_LOCATION, [B1_LOCATION, B2_LOCATION]) is False
    # Move from source to itself
    assert Move.check(state, A1_LOCATION, [A1_LOCATION, A1_LOCATION]) is False
    # Move from source to empty and itself
    assert Move.check(state, A1_LOCATION, [A2_LOCATION, A1_LOCATION]) is False
    # Valid onto empty cells
    assert Move.check(state, A1_LOCATION, [A2_LOCATION, A2_LOCATION]) is True
    # Move onto standing piece
    assert Move.check(state, A1_LOCATION, [B1_LOCATION, B1_LOCATION]) is False
    # Move onto flat piece
    assert Move.check(state, A1_LOCATION, [B2_LOCATION, B2_LOCATION]) is True
    # Move onto mixed
    assert Move.check(state, A1_LOCATION, [B1_LOCATION, B2_LOCATION]) is False
    # Move fewer than in the stack
    assert Move.check(state, A1_LOCATION, [B2_LOCATION]) is True
    # Move more than in the stack
    assert Move.check(state, A1_LOCATION, [B2_LOCATION, B2_LOCATION, B2_LOCATION, B2_LOCATION]) is False
    # Move all in stack (last piece cannot be moved)
    assert Move.check(state, A1_LOCATION, [B2_LOCATION, B2_LOCATION, B2_LOCATION]) is False
    assert Move.check(state, A1_LOCATION, [B2_LOCATION, B2_LOCATION]) is True

def test_move_others_check():
    """
    Tests the move check function for different players
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    # 2 pieces for each player
    insert(state, p0.get_piece(Piece.FLAT    ), A1_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), A2_LOCATION)
    insert(state, p1.get_piece(Piece.FLAT    ), B1_LOCATION)
    insert(state, p1.get_piece(Piece.STANDING), B2_LOCATION)
    # p0 is the current player
    assert state.current_player is p0
    # Move own piece:
    assert Move.check(state, A1_LOCATION, [A3_LOCATION]) is True
    assert Move.check(state, A2_LOCATION, [A3_LOCATION]) is True
    # Move others piece:
    assert Move.check(state, B1_LOCATION, [B3_LOCATION]) is False
    assert Move.check(state, B2_LOCATION, [B3_LOCATION]) is False
    # Move onto others piece:
    assert Move.check(state, A1_LOCATION, [B1_LOCATION]) is True
    assert Move.check(state, A2_LOCATION, [B1_LOCATION]) is True
    # Move others onto own piece:
    assert Move.check(state, B1_LOCATION, [A1_LOCATION]) is False
    assert Move.check(state, B2_LOCATION, [A1_LOCATION]) is False

def test_move_mixed_stack_check():
    """
    Tests moving stacks where pieces are owned by different players
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    # A0: p1 p1 p0 p0
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p1.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p1.get_piece(Piece.FLAT), A1_LOCATION)
    # B0: p0 p0 p1
    insert(state, p1.get_piece(Piece.FLAT), B1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), B1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), B1_LOCATION)
    # Move stack where top is owner by other player:
    assert Move.check(state, A1_LOCATION, [A2_LOCATION]) is False
    assert Move.check(state, A1_LOCATION, [A2_LOCATION, A2_LOCATION]) is False
    assert Move.check(state, A1_LOCATION, [A2_LOCATION, A2_LOCATION, A2_LOCATION]) is False
    # Move stack where top is owner by current player:
    assert Move.check(state, B1_LOCATION, [B2_LOCATION]) is True
    assert Move.check(state, B1_LOCATION, [B2_LOCATION, B2_LOCATION]) is True
    assert Move.check(state, B1_LOCATION, [B2_LOCATION, B2_LOCATION, B2_LOCATION]) is False

def test_move_execute():
    """
    Tests the move check function for various edge cases when moving a single 
    piece, uses check and only verifies that board is modified accurately
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), B1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), B2_LOCATION)
    # No destinations are provided:
    assert Move.execute(state, A1_LOCATION, []) is Move.FAILED
    # move onto standing tile:
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, B1_LOCATION).size == 1
    assert Move.execute(state, A1_LOCATION, [B1_LOCATION]) is Move.FAILED
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, B1_LOCATION).size == 1
    # move onto flat tiles:
    assert get_cell(state, B2_LOCATION).size == 1
    assert Move.execute(state, A1_LOCATION, [B2_LOCATION, B2_LOCATION]) is Move.SUCCEEDED
    assert get_cell(state, A1_LOCATION).size == 1
    assert get_cell(state, B2_LOCATION).size == 3
    # Restore
    Move.undo(state, A1_LOCATION, [B2_LOCATION, B2_LOCATION])
    # move onto mixed tiles:
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, B1_LOCATION).size == 1
    assert get_cell(state, B2_LOCATION).size == 1
    assert Move.execute(state, A1_LOCATION, [B1_LOCATION, B2_LOCATION]) is Move.FAILED
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, B1_LOCATION).size == 1
    assert get_cell(state, B2_LOCATION).size == 1

def test_move_undo():
    """
    Tests undoing move actions
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), B1_LOCATION)
    # Move single
    args = [state, A1_LOCATION, [A2_LOCATION]]
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, A2_LOCATION).size == 0
    assert Move.execute(*args) is Move.SUCCEEDED
    assert get_cell(state, A1_LOCATION).size == 2
    assert get_cell(state, A2_LOCATION).size == 1
    Move.undo(*args)
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, A2_LOCATION).size == 0
    
    # Move multiple
    args = [state, A1_LOCATION, [A2_LOCATION, A3_LOCATION]]
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, A2_LOCATION).size == 0
    assert get_cell(state, A3_LOCATION).size == 0
    assert Move.execute(*args) is Move.SUCCEEDED
    assert get_cell(state, A1_LOCATION).size == 1
    assert get_cell(state, A2_LOCATION).size == 1
    assert get_cell(state, A3_LOCATION).size == 1
    Move.undo(*args)
    assert get_cell(state, A1_LOCATION).size == 3
    assert get_cell(state, A2_LOCATION).size == 0
    assert get_cell(state, A3_LOCATION).size == 0

def test_get_args_valid():
    """
    Tests that all arguments from the get_args function are valid
    """
    p0 = Player(0, 21)
    p1 = Player(1, 21)
    state = GameState([p0, p1], [])
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A1_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), B1_LOCATION)
    insert(state, p0.get_piece(Piece.FLAT), A2_LOCATION)
    insert(state, p0.get_piece(Piece.STANDING), A2_LOCATION)
    all_args = Move.get_args(state)
    assert len(all_args) > 0
    for args in all_args:
        assert Move.check(state, *args) is True

def run_move_tests():
    test_move_get_name()
    test_move_single_check()
    test_move_multiple_check()
    test_move_others_check()
    test_move_mixed_stack_check()
    test_move_execute()
    test_move_undo()
    test_get_args_valid()

if __name__ == "__main__":
    run_move_tests()