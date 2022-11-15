from structure import Board, GameState, Location, Piece, Player
from structure.actions import Insert, Move, Flip

SIZE = 5

def test_flip_execute():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    # Execute a flat piece to flip
    Insert.execute(gs, Location(0, 0), 0)
    assert gs.board.select(Location(0, 0)).state == Piece.FLAT

    # Flip the piece
    Flip.execute(gs, Location(0, 0))
    assert gs.board.select(Location(0, 0)).state == Piece.STANDING

def test_flip_undo():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    # Execute a flat piece to flip
    Insert.execute(gs, Location(0, 0), 0)
    assert gs.board.select(Location(0, 0)).state == Piece.FLAT

    # Flip the piece
    Flip.execute(gs, Location(0, 0))
    assert gs.board.select(Location(0, 0)).state == Piece.STANDING  

    # Undo the flip
    Flip.undo(gs, Location(0, 0))
    assert gs.board.select(Location(0, 0)).state == Piece.FLAT
    
def run_flip_tests():
    test_flip_execute()
    test_flip_undo()

if __name__ == "__main__":
    run_flip_tests()