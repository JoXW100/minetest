from structure import Action, GameState, ActionOutcome
import sys

class Exit(Action):
    """
    Exits the game
    """
    @staticmethod
    def get_name():
        return "Exit"
    
    @staticmethod
    def get_key() -> str:
        return 'Q'
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        sys.exit("Exiting...")
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Exits game"