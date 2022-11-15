from structure import Action, GameState
import sys

class Exit(Action):
    """
    Exits the game
    """
    @staticmethod
    def get_name():
        return "Exit"
    
    @staticmethod
    def check(state: GameState) -> bool:
        return False
        
    @staticmethod
    def execute(state: GameState) -> int:
        sys.exit("Exiting...")
        return Action.IGNORE
    
    @staticmethod
    def unsafe_execute(state: GameState):
        pass

    @staticmethod
    def undo(state: GameState):
        pass

    @staticmethod
    def ask_args(state: GameState) -> list[any]:
        return []
    
    @staticmethod
    def get_args(state: GameState) -> list[list[any]]:
        return []
    
    @staticmethod
    def to_str():
        return "Exits game"