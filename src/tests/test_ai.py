from structure import GameState, Location, Piece, Player
from structure.players import AI
from structure.actions import Insert, ALL_ACTIONS

SIZE = 5

def test_ai_game_over_no_move():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], [], SIZE)

    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(0, 1), 0)
    Insert.execute(gs, Location(0, 2), 0)
    Insert.execute(gs, Location(0, 3), 0)
    Insert.execute(gs, Location(0, 4), 0)

    # Game should now be over
    assert gs.is_game_over() == 1
    
    # Asking for a move should raise Exception
    try:
        ai.perform_turn(gs)
        assert False
    except Exception:
        assert True

def test_longer_rows_is_better():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], [], SIZE)
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    
    assert gs.current_player is ai
    base_evaluate = ai._evaluate(gs)
    Insert.execute(gs, Location(1, 0), Piece.FLAT)
    new_evaluate = ai._evaluate(gs)
    assert new_evaluate > base_evaluate
    base_evaluate = new_evaluate
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    new_evaluate = ai._evaluate(gs)
    assert new_evaluate > base_evaluate
    base_evaluate = new_evaluate
    Insert.execute(gs, Location(3, 0), Piece.FLAT)
    new_evaluate = ai._evaluate(gs)
    assert new_evaluate > base_evaluate

def test_different_players_eval():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], [], SIZE)
    
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    assert ai._evaluate(gs) > 0
    gs.next_round()
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    assert ai._evaluate(gs) < 0
    
def test_perform_turn_improves_score():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(1, 0), Piece.FLAT)
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    
    base_evaluate = ai._evaluate(gs)
    assert gs.current_player is ai
    ai.perform_turn(gs)
    assert base_evaluate < ai._evaluate(gs)
    
def test_winning_move_horizontal_straight():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is ai
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(1, 0), Piece.FLAT)
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    Insert.execute(gs, Location(3, 0), Piece.FLAT)
    ai.perform_turn(gs)
    assert gs.is_game_over() is ai.identifier

def test_winning_move_vertical_straight():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is ai
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(0, 1), Piece.FLAT)
    Insert.execute(gs, Location(0, 2), Piece.FLAT)
    Insert.execute(gs, Location(0, 3), Piece.FLAT)
    ai.perform_turn(gs)
    assert gs.is_game_over() is ai.identifier

def test_winning_move_vertical_curved():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is ai
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(1, 0), Piece.FLAT)
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    Insert.execute(gs, Location(2, 1), Piece.FLAT)
    Insert.execute(gs, Location(3, 1), Piece.FLAT)
    ai.perform_turn(gs)
    assert gs.is_game_over() is ai.identifier
    
def test_winning_move_horizontal_curved():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is ai
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(0, 1), Piece.FLAT)
    Insert.execute(gs, Location(0, 2), Piece.FLAT)
    Insert.execute(gs, Location(1, 2), Piece.FLAT)
    Insert.execute(gs, Location(1, 3), Piece.FLAT)
    ai.perform_turn(gs)
    assert gs.is_game_over() is ai.identifier

def test_prevent_winning_move_horizontal():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([player, ai], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is player
    Insert.execute(gs, Location(0, 0), Piece.STANDING)
    Insert.execute(gs, Location(1, 0), Piece.STANDING)
    Insert.execute(gs, Location(2, 0), Piece.STANDING)
    Insert.execute(gs, Location(3, 0), Piece.STANDING)
    gs.next_round()
    assert gs.current_player is ai
    ai.perform_turn(gs)
    assert not gs.board.rows[0][4].is_empty and gs.board.rows[0][4].top.owner is ai

def test_prevent_winning_move_vertical():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([player, ai], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is player
    Insert.execute(gs, Location(0, 0), Piece.STANDING)
    Insert.execute(gs, Location(0, 1), Piece.STANDING)
    Insert.execute(gs, Location(0, 2), Piece.STANDING)
    Insert.execute(gs, Location(0, 3), Piece.STANDING)
    gs.next_round()
    assert gs.current_player is ai
    ai.perform_turn(gs)
    assert not gs.board.rows[4][0].is_empty and gs.board.rows[4][0].top.owner is ai

def test_winning_move_stack():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is ai
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    Insert.execute(gs, Location(0, 0), Piece.FLAT)
    # Larger stacks increase execution time exponentially
    Insert.execute(gs, Location(1, 0), Piece.FLAT)
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    ai.perform_turn(gs)
    assert gs.is_game_over() is ai.identifier

def test_two_moves_from_winning():
    ai = AI(1, 21)
    player = Player(2, 21)
    gs = GameState([ai, player], ALL_ACTIONS, SIZE, 2, 2)
    assert gs.current_player is ai
    Insert.execute(gs, Location(0, 0), Piece.STANDING)
    Insert.execute(gs, Location(1, 0), Piece.STANDING)
    Insert.execute(gs, Location(2, 0), Piece.STANDING)
    ai.perform_turn(gs)
    assert not gs.board.rows[0][3].is_empty and gs.board.rows[0][3].top.owner is ai \
        or not gs.board.rows[0][4].is_empty and gs.board.rows[0][4].top.owner is ai 

def run_ai_tests():
    test_different_players_eval()
    test_ai_game_over_no_move()
    test_perform_turn_improves_score()
    test_winning_move_horizontal_straight()
    test_winning_move_horizontal_curved()
    test_winning_move_vertical_straight()
    test_winning_move_vertical_curved()
    test_prevent_winning_move_horizontal()
    test_prevent_winning_move_vertical()
    test_longer_rows_is_better()
    test_winning_move_stack()
    test_two_moves_from_winning()

if __name__ == "__main__":
    run_ai_tests()