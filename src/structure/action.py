from __future__ import annotations
from abc import ABCMeta, abstractmethod
import structure.game_state as gs

# Abstract singleton with static methods
class Action(metaclass = ABCMeta):
    """
    Represent an executable action
    """
    
    FAILED = 0
    SUCCEEDED = 1
    PASS = 2
    IGNORE = 3
    
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """
        Gets the name of the action
        Returns
        -------
        name : str
            The name of the action
        """
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def check(state: gs.GameState, *args: list[any]) -> bool:
        """
        Checks if the action is valid given a game state and a set of argument

        Attributes
        ----------
        state: GameState
        args : list[any]
        
        Returns
        -------
        valid : bool
            True if the action was executed, False otherwise
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def execute(state: gs.GameState, *args: list[any]) -> int:
        """
        Executes the action if it is valid given the current game state

        Attributes
        ----------
        state: GameState
        args : any
        
        Returns
        -------
        status : int
            0 if the action failed, 1 of it succeeded, and 2 if the action should be ignored
        """
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def unsafe_execute(state: gs.GameState, *args: list[any]):
        """
        Executes the action unsafely

        Attributes
        ----------
        state: GameState
        args : list[any]
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def undo(state: gs.GameState, *args: list[any]):
        """
        Undoes the action

        Attributes
        ----------
        state: GameState
        args : list[any]
        """
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def ask_args(state: gs.GameState) -> list[any]:
        """
        Asks the user for arguments in the terminal

        Attributes
        ----------
        state: GameState
        
        Returns
        -------
        args : list[any]
            The arguments for the function
        """
    
    @staticmethod
    @abstractmethod
    def get_args(state: gs.GameState) -> list[list[any]]:
        """
        Gets all valid argument combinations for this action

        Attributes
        ----------
        state: GameState
        
        Returns
        -------
        args : list[list[any]]
            A list of all combinations of arguments
        """
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def to_str(*args: list[any]):
        raise NotImplementedError
        
    