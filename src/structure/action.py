from __future__ import annotations
from enum import Enum
from abc import ABCMeta, abstractmethod
from pynput.keyboard import KeyCode
import structure as st

class ActionOutcome(Enum):
    FAILED = 0
    SUCCEEDED = 1
    IGNORE = 2 # SUCCEEDED but do not end turn

# Abstract singleton with static methods
class Action(metaclass = ABCMeta):
    """
    Represent an executable action
    """
    
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
    def get_key() -> KeyCode:
        """
        Gets the name of the action
        
        Returns
        -------
        key : str
            The key used by the action
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def execute(state: st.GameState, *args: list[any]) -> ActionOutcome:
        """
        Executes the action if it is valid given the current game state

        Attributes
        ----------
        state: GameState
            The current game state to modify
        args : list[any]
            The appropriate arguments for the Action
        
        Returns
        -------
        outcome : ActionOutcome
            The outcome of the action
        """
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def to_str(*args: list[any]):
        """
        Returns a descriptive text of the action given the arguments
        
        Attributes
        ----------
        args : list[any]
        
        Returns
        -------
        text : str
            The descriptive text of the action
        """
        raise NotImplementedError

    @property
    def allowed_in_pause(self) -> bool:
        """
        Returns True if the action is allowed when the game is paused and False
        if not

        Returns
        -------
        allowed : bool
            If the action is allowed when the game is paused
        """
        return False
    