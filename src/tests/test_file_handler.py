import os
from structure import Board, GameState, Location, Piece, Player
from structure.actions import Flip, Insert, Move
from file_handler import game_state_to_file, game_state_from_file

SIZE = 5
SERIALIZE_PATH = "test.json"

def test_game_state_serialize_deserialize_empty():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    assert game_state_to_file(SERIALIZE_PATH, gs) is True
    new_gs = game_state_from_file(SERIALIZE_PATH)
    assert new_gs == gs

def test_game_state_serialize_deserialize_with_moves():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    # Make some random moves
    Insert.execute(gs, Location(0, 0), 0)
    gs.next_round()
    Insert.execute(gs, Location(1, 0), 0)
    gs.next_round()
    Insert.execute(gs, Location(2, 0), 0)
    gs.next_round()

    assert game_state_to_file(SERIALIZE_PATH, gs) == True
    new_gs = game_state_from_file(SERIALIZE_PATH)
    assert new_gs == gs

def test_game_state_serialize_deserialize_with_stacked_moves():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    # Create a stack
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    gs.next_round()
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    gs.next_round()
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    gs.next_round()
    Insert.execute(gs, Location(2, 0), Piece.FLAT)
    gs.next_round()
    Insert.execute(gs, Location(2, 0), Piece.STANDING)
    gs.next_round()

    assert game_state_to_file(SERIALIZE_PATH, gs) == True
    new_gs = game_state_from_file(SERIALIZE_PATH)
    assert new_gs == gs

def test_game_state_serialize_deserialize_when_won():
    players = [Player(0, 21), Player(1, 21)]
    actions = [Flip(), Insert(), Move()]
    gs = GameState(players, actions, SIZE)

    # Straight line from left to right is a valid win
    Insert.execute(gs, Location(0, 0), 0)
    Insert.execute(gs, Location(1, 0), 0)
    Insert.execute(gs, Location(2, 0), 0)
    Insert.execute(gs, Location(3, 0), 0)
    Insert.execute(gs, Location(4, 0), 0)

    assert game_state_to_file(SERIALIZE_PATH, gs) == True
    new_gs = game_state_from_file(SERIALIZE_PATH)
    assert new_gs == gs
    
def cleanup():
    # Cleanup test files
    if os.path.exists(SERIALIZE_PATH):
        os.remove(SERIALIZE_PATH)
    
def run_file_handler_tests():
    test_game_state_serialize_deserialize_empty()
    cleanup()
    test_game_state_serialize_deserialize_with_moves()
    cleanup()
    test_game_state_serialize_deserialize_with_stacked_moves()
    cleanup()
    test_game_state_serialize_deserialize_when_won()
    cleanup()
    