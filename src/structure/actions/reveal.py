from structure import Action, GameState, ActionOutcome
from pynput.keyboard import KeyCode

class Reveal(Action):
    """
    Reveals cell at the current selection
    """
    @staticmethod
    def get_name():
        return "[d] Reveal cell"
    
    @staticmethod
    def get_key() -> str:
        return KeyCode.from_char('d')
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        print("Reveal: round = " + str(state.round))
        res = False
        if state.round < 1:
            res = state.board.reveal_and_distribute(state.selection, state.mines)
        else:
            res = state.board.reveal_cell(state.selection)
        return ActionOutcome.SUCCEEDED if res else ActionOutcome.FAILED
    
    @staticmethod
    def to_str():
        return "Reveals cell"