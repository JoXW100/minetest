from structure import Board, GameState, Location, Piece, Player
from structure.actions import Flip, Insert, Move

SIZE = 5

def test_round():
    state = GameState([Player(0,21)], [])
    assert state.round == 0
    state.next_round()
    assert state.round == 1
    state.prev_round()
    assert state.round == 0

def test_current_player():
    p1 = Player(0,21)
    p2 = Player(1,21)
    state = GameState([p1, p2], [])

    # First, p1 will place for p2 so p2 is current_player
    assert state.current_player is p1
    assert state.current_player is not p2
    state.next_round()
    # p2 will place for p1 so p1 is current_player
    assert state.current_player is p2
    state.next_round()
    
    # regular rounds starting, p1 is current_player
    assert state.current_player is p1

    state = GameState([], [])
    assert state.current_player is None

def test_game_state_init():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert gs.board.size == SIZE
    assert gs.current_player == players[0]
    assert gs.round == 0
    assert gs.players == players
    assert gs.actions == actions

def test_game_state_round():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert gs.round == 0
    gs.next_round()
    assert gs.round == 1
    gs.prev_round()
    assert gs.round == 0
    gs.next_round()
    gs.next_round()
    assert gs.round == 2
    assert gs.current_player == players[0]

def test_game_state_is_game_over_straight_lines():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert gs.is_game_over() == GameState.PLAYING

    # Straight line from left to right is a valid win
    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(1, 0), 0)
    Insert.execute(gs, Location(2, 0), 0)
    Insert.execute(gs, Location(3, 0), 0)
    Insert.execute(gs, Location(4, 0), 0)
    assert gs.is_game_over() == gs.current_player.identifier

    # Reset game state
    gs = GameState(players, actions, SIZE, round=2)

    # Straight line from top to bottom is a valid win
    Insert.execute(gs, Location(1, 0), 1)
    Insert.execute(gs, Location(1, 1), 1)
    Insert.execute(gs, Location(1, 2), 1)
    Insert.execute(gs, Location(1, 3), 1)
    Insert.execute(gs, Location(1, 4), 1)
    assert gs.is_game_over() == gs.current_player.identifier
    
    # Reset game state
    gs = GameState(players, actions, SIZE, round=2)
    
    # Straight line from top to bottom with some standing, some flat pieces is not a valid win
    Insert.execute(gs, Location(1, 0), 1)
    Insert.execute(gs, Location(1, 1), 1)
    Insert.execute(gs, Location(1, 2), 0)
    Insert.execute(gs, Location(1, 3), 0)
    Insert.execute(gs, Location(1, 4), 0)
    assert gs.is_game_over() == GameState.PLAYING

def test_game_state_is_game_over_adjacent_pieces():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE, round=2)
    assert gs.is_game_over() == GameState.PLAYING

    Insert.execute(gs, Location(0, 0), 1)
    Insert.execute(gs, Location(0, 1), 1) 
    Insert.execute(gs, Location(1, 0), 1)
    Insert.execute(gs, Location(1, 1), 1)
    Insert.execute(gs, Location(1, 2), 1)
    Insert.execute(gs, Location(1, 3), 1)
    Insert.execute(gs, Location(1, 4), 1)
   
    assert gs.is_game_over() == gs.current_player.identifier

def test_game_state_is_game_over_diagonal_line():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert gs.is_game_over() == GameState.PLAYING

    # Diagonal line is not a valid win
    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(1, 1), 0)
    Insert.execute(gs, Location(2, 2), 0)
    Insert.execute(gs, Location(3, 3), 0)
    Insert.execute(gs, Location(4, 4), 0)
    assert gs.is_game_over() == GameState.PLAYING

def test_game_state_is_game_over_curved_lines():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert gs.is_game_over() == GameState.PLAYING

    # Line with 1 turn is a valid win
    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(1, 0), 0)
    Insert.execute(gs, Location(1, 1), 0)
    Insert.execute(gs, Location(2, 1), 0)
    Insert.execute(gs, Location(3, 1), 0)
    Insert.execute(gs, Location(4, 1), 0)
    assert gs.is_game_over() == 0

    # Reset game state and skip initial placing turns
    gs = GameState(players, actions, SIZE, round=2)
    assert gs.is_game_over() == GameState.PLAYING

    # Line with 2 turns is not a valid win
    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(1, 0), 0)
    Insert.execute(gs, Location(1, 1), 0)
    Insert.execute(gs, Location(2, 1), 0)
    Insert.execute(gs, Location(2, 2), 0)
    Insert.execute(gs, Location(3, 2), 0)
    Insert.execute(gs, Location(4, 2), 0)
    assert gs.is_game_over() == GameState.PLAYING

def test_game_state_invalid_game_over():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert gs.is_game_over() == GameState.PLAYING

    # Going from left to top is not a valid win
    Insert.execute(gs, Location(0, 3), 0)
    Insert.execute(gs, Location(1, 3), 0)
    Insert.execute(gs, Location(1, 2), 0)
    Insert.execute(gs, Location(1, 1), 0)
    Insert.execute(gs, Location(1, 0), 0)
    assert gs.is_game_over() == GameState.PLAYING

    # Reset game state and skip initial placing turns
    gs = GameState(players, actions, SIZE, round=2)
    assert gs.is_game_over() == GameState.PLAYING

    # Going from bottom to right is not a valid win
    Insert.execute(gs, Location(3, 0), 0)
    Insert.execute(gs, Location(3, 1), 0)
    Insert.execute(gs, Location(3, 2), 0)
    Insert.execute(gs, Location(3, 3), 0)
    Insert.execute(gs, Location(4, 3), 0)
    assert gs.is_game_over() == GameState.PLAYING

def test_game_state_is_game_over_stacks():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE, round=2)

    assert gs.is_game_over() == GameState.PLAYING

    # Straight line from left to right is a valid win
    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(1, 0), 0)
    Insert.execute(gs, Location(2, 0), 0)
    Insert.execute(gs, Location(3, 0), 0)
    Insert.execute(gs, Location(4, 0), 0)
    assert gs.is_game_over() == 0

    # Player 1 inserts on top of a piece
    gs.next_round()
    Insert.execute(gs, Location(2, 0), 0)
    assert gs.is_game_over() == GameState.PLAYING

    # Player 0 inserts on top again
    gs.next_round()
    Insert.execute(gs, Location(2, 0), 0)
    assert gs.is_game_over() == 0

def test_game_state_is_game_over_all_standing_pieces():
    # Checks if the game is over if all tiles are covered in standing pieces
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE, round=2)

    assert gs.is_game_over() == GameState.PLAYING

    # Fill the board with standing pieces
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            Insert.execute(gs, Location(i, j), 1)
            gs.next_round()
    assert gs.is_game_over() == GameState.DRAW

def run_game_state_tests():
    test_game_state_init()
    test_game_state_round()
    test_game_state_is_game_over_straight_lines()
    test_game_state_is_game_over_diagonal_line()
    test_game_state_is_game_over_curved_lines()
    test_game_state_invalid_game_over()
    test_game_state_is_game_over_stacks()
    test_game_state_is_game_over_all_standing_pieces()
    test_round()
    test_current_player()
    test_game_state_is_game_over_adjacent_pieces()

if __name__ == "__main__":
    run_game_state_tests()
