from structure import Action, GameState, ActionOutcome
from pynput.keyboard import Key, KeyCode
import os

class Exit(Action):
    """
    Exits the game
    """
    @staticmethod
    def get_name():
        return "Exit"
    
    @staticmethod
    def get_key() -> KeyCode:
        return KeyCode.from_char('q')
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        print("Exiting...")
        os._exit(0)
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Exit game"