from xml.etree.ElementTree import PI
from structure import GameState, Piece
import structure.players as players
import structure.actions as actions
import json

def game_state_to_file(path: str, state: GameState) -> bool:
    """
    Attempts to serialize and write the game state to a file

    Parameters
    ----------
    path : str
        File path to a JSON file to write serialized data to
    state: GameState
        The game state to serialize

    Returns
    -------
    success : bool
        True if the game state was serialized and written to file successfully,
        False otherwise
    """
    try:
        data = { 
            "board": [[[{ 
                "owner": p.owner.identifier, 
                "state": p.state 
            } for p in cell] for cell in row] for row in state.board.rows], 
            "players": [{ 
                "identifier": player.identifier, 
                "type": player.get_type(), 
                "pieces": player.pieces, 
                "color": player.color 
            } for player in state.players], 
            "difficulty": state.ai_difficulty, 
            "round": state.round 
        }
        # Open with w+ mode to ensure that file is created if it does not exist
        with open(path, "w+") as f:
            json.dump(data, f, indent = 4)
        return True
    except Exception as e:
        print(f"Could not write game state to file: {path}")
        return False

def game_state_from_file(path: str) -> GameState:
    """
    Deserializes a JSON file at path containing game state data, and
    tries to convert it into a GameState instance

    Parameters
    ----------
    path : str
        File path to a JSON file containing serialized game state

    Returns
    -------
    GameState : str
        The new game state based on the JSON data in path
    """
    try:
        with open(path) as f:
            data = json.load(f)
            player_list = []
            for p in data["players"]:
                x = players.AI(p["identifier"], p["pieces"]) \
                    if p["type"] == players.AI.get_type() \
                    else players.Human(p["identifier"], p["pieces"])
                x.color = p["color"]
                player_list.append(x)
            size = len(data["board"])
            state = GameState(player_list, actions.ALL_ACTIONS, size, data["difficulty"], data["round"])
            for y in range(size):
                for x in range(size):
                    # Insert pieces in reverse order
                    for p in reversed(data["board"][y][x]):
                        owner = next((player for player in player_list if player.identifier == p["owner"]), None)
                        if owner is not None and (p["state"] == Piece.FLAT or p["state"] == Piece.STANDING):
                            state.board.rows[y][x].put(Piece(owner, p["state"]))
            return state
    except Exception:
        print(f"Could not create game state from file or file did not exist: {path}")
        return None