from __future__ import annotations
import structure as st

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
        # TODO: Implement after board & BoardCell has been implemented

        action = state.get_action(key)
        if action is not None:
            outcome = action.execute(state)
            if outcome is st.ActionOutcome.SUCCEEDED:
                state.next_round()
            elif outcome is st.ActionOutcome.FAILED:
                print("Failed: " + action.to_str())
        return action is not None