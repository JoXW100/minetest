from structure import Action, GameState
from file_handler import game_state_to_file

class Save(Action):
    """
    Saves the game
    """
    @staticmethod
    def get_name():
        return "Save"
    
    @staticmethod
    def check(state: GameState, path: str) -> bool:
        return False
        
    @staticmethod
    def execute(state: GameState, path: str) -> int:
        res = game_state_to_file(path, state)
        return Action.IGNORE if res else Action.FAILED
    
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
        return "Saves game at '" + path + "'"