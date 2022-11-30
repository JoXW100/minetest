from structure import Action, GameState, ActionOutcome
from pynput.keyboard import Key, KeyCode
import os

class TogglePause(Action):
    """
    Toggles paused state
    paused -> unpaused and unpaused -> paused
    """
    @staticmethod
    def get_name():
        return "[P] Pause/Unpause"
    
    @staticmethod
    def get_key() -> KeyCode:
        return KeyCode.from_char('p')
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        state.toggle_pause()
        return ActionOutcome.SUCCEEDED
    
    @staticmethod
    def to_str():
        return "Pause/Unpause"