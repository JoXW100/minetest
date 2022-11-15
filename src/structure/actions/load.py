from structure import Action, GameState
from file_handler import game_state_from_file

class Load(Action):
    """
    Loads the game from a saved game state
    """
    @staticmethod
    def get_name():
        return "Load"
    
    @staticmethod
    def check(state: GameState, path: str) -> bool:
        return False
        
    @staticmethod
    def execute(state: GameState, path: str) -> int:
        res = game_state_from_file(path)
        if res is None:
            return Action.FAILED
        state.overwrite(res)
        return Action.PASS
    
    @staticmethod
    def unsafe_execute(state: GameState, path: str):
        pass

    @staticmethod
    def undo(state: GameState, path: str):
        pass

    @staticmethod
    def ask_args(state: GameState) -> list[any]:
        value = input("Enter save path: ")
        return [value]
    
    @staticmethod
    def get_args(state: GameState) -> list[list[any]]:
        return []
    
    @staticmethod
    def to_str(path: str):
        return "Loads game at '" + path + "'"