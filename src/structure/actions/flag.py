from pynput.keyboard import KeyCode
from structure import Action, GameState, ActionOutcome, CellState

class Flag(Action):
    """
    Flags cell at the current selection
    """
    @staticmethod
    def get_name():
        return "[F] Flag cell"
    
    @staticmethod
    def get_key() -> str:
        return KeyCode.from_char('f')
        
    @staticmethod
    def execute(state: GameState) -> ActionOutcome:
        cell = state.board.select(state.selection)
        if cell.state is CellState.Hidden:
            cell.set_state(CellState.Flagged)
        elif cell.state is CellState.Flagged:
            cell.set_state(CellState.Hidden)
        return ActionOutcome.IGNORE
    
    @staticmethod
    def to_str():
        return "Flag cell"