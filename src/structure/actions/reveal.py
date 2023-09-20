from pynput.keyboard import KeyCode
from structure import Action, GameState, ActionOutcome

class Reveal(Action):
    """
    Reveals cell at the current selection
    """
    @staticmethod
    def get_name():
        return "[D] Reveal cell"
    
    @staticmethod
    def get_key() -> str:
        return KeyCode.from_char('d')
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        res = state.reveal_and_distribute(state.selection, state.mines) \
            if state.round == 0 else state.reveal_cell(state.selection)
        return ActionOutcome.SUCCEEDED if res else ActionOutcome.FAILED
    
    @staticmethod
    def to_str():
        return "Reveal cell"