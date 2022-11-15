from structure import GameState, Location, Piece, Player
from structure.actions import Insert, Move, Flip

SIZE = 5

def test_insert_execute():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    # Execute should fail if the location is not valid
    Insert().execute(gs, Location(5, 5), 0)
    assert gs.board.select(Location(5, 5)) is None

    # Insert a piece
    Insert().execute(gs, Location(0, 0), 0)
    assert gs.board.select(Location(0, 0)).state == Piece.FLAT

    # Insert a piece on top of another piece
    Insert().execute(gs, Location(0, 0), 1)
    assert gs.board.select(Location(0, 0)).state == Piece.STANDING
    assert gs.board.rows[0][0].size == 2

def test_insert_unsafe_execute():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    Insert().unsafe_execute(gs, Location(0, 0), 0)
    assert gs.board.select(Location(0, 0)).state == Piece.FLAT

def test_insert_undo():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    Insert().execute(gs, Location(0, 0), 0)
    assert gs.board.select(Location(0, 0)).state == Piece.FLAT
    Insert().undo(gs, Location(0, 0), 0)
    assert gs.board.select(Location(0, 0)) is None
    
def run_insert_tests():
    test_insert_execute()
    test_insert_unsafe_execute()
    test_insert_undo()

if __name__ == "__main__":
    run_insert_tests()