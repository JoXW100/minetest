from structure import Action, GameState, ActionOutcome, Direction
from pynput.keyboard import Key, KeyCode

class NavigateUp(Action):
    """
    Navigates up
    """
    @staticmethod
    def get_name():
        return "[↑] Navigate up"
    
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
        return "[→] Navigate right"
    
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
        return "[↓] Navigate down"
    
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
        return "[←] Navigate left"
    
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