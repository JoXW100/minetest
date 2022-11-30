from __future__ import annotations
import structure as st
from .actions import TogglePause, Exit

class Player:
    """
    Represents a player and handles how they process their turns
    
    Attributes
    ----------
    
    Methods
    -------
    perform_turn(state : GameState) -> None
        Performs a player turn
    """
    
    # Singleton
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    def perform_turn(self, state: st.GameState, key: str) -> bool:
        action = state.get_action(key)

        if action is not None:
            # If the action toggles paused state, return immediately
            if isinstance(action, TogglePause):
                action.execute(state)
                return True

            # Only perform turn if the game is unpaused or if exiting the game
            if not state.is_paused or isinstance(action, Exit):
                outcome = action.execute(state)
                if outcome is st.ActionOutcome.SUCCEEDED:
                    state.next_round()
                elif outcome is st.ActionOutcome.FAILED:
                    # Find better way, this is cleared instantly
                    print("Failed: " + action.to_str())
                return True
        return False