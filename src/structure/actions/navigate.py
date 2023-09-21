from pynput.keyboard import Key, KeyCode
from structure import Action, GameState, ActionOutcome, Direction
import os

class NavigateUp(Action):
    """
    Navigates up
    """
    @staticmethod
    def get_name():
        return f"[{'I' if os.environ['INPUT_MODE'] == 'native' else '↑'}] Navigate up"
    
    @staticmethod
    def get_key() -> str:
        return Key.up
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        state.navigate(Direction.Up)
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Navigate up"

class NavigateRight(Action):
    """
    Navigates right
    """
    @staticmethod
    def get_name():
        return f"[{'L' if os.environ['INPUT_MODE'] == 'native' else '→'}] Navigate right"
    
    @staticmethod
    def get_key() -> str:
        return Key.right
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        state.navigate(Direction.Right)
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Navigate right"
   
class NavigateDown(Action):
    """
    Navigates down
    """
    @staticmethod
    def get_name():
        return f"[{'K' if os.environ['INPUT_MODE'] == 'native' else '↓'}] Navigate down"
    
    @staticmethod
    def get_key() -> str:
        return Key.down
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        state.navigate(Direction.Down)
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Navigate right"
    
class NavigateLeft(Action):
    """
    Navigates left
    """
    @staticmethod
    def get_name():
        return f"[{'J' if os.environ['INPUT_MODE'] == 'native' else '←'}] Navigate left"
    
    @staticmethod
    def get_key() -> KeyCode:
        return Key.left
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        state.navigate(Direction.Left)
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Navigate left"