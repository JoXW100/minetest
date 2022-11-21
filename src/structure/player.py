from __future__ import annotations
import structure as st
from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

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
    
    def perform_turn(self, state : st.GameState):
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            listener.join()
        # TODO: Implement after board & BoardCell has been implemented
        raise NotImplementedError