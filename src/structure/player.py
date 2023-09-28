from __future__ import annotations
import structure as st

class Player:
    """
    Represents a player and handles how they process their turns
    
    Methods
    -------
    perform_turn(state : GameState) -> bool
        Performs a player turn
    """

    # Singleton
    _instances = {}
    def __call__(self, cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def perform_turn(self, state: st.GameState, key: str) -> bool:
        """
        Performs a player turn given a character representing the action to be
        taken.
        
        Attributes
        ----------
        state : GameState
            The current state of the game
        key : str
            The key (character) corresponding to the action to be played
        
        Returns
        -------
        success : bool
           If the action was performed successfully or not
        """
        action = state.get_action(key)

        if action is not None:
            # Only perform turn if the game is unpaused or the action is allowed
            # in pause.
            if not state.is_paused or action.allowed_in_pause:
                outcome = action.execute(state)
                if outcome is st.ActionOutcome.SUCCEEDED:
                    state.next_round()
                elif outcome is st.ActionOutcome.FAILED:
                    # Find better way, this is cleared instantly
                    print("Failed: " + action.to_str())
                return True
        return False
