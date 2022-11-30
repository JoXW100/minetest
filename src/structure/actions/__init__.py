from .exit import Exit
from .navigate import NavigateUp, NavigateRight, NavigateDown, NavigateLeft
from .reveal import Reveal
from .flag import Flag
from .toggle_pause import TogglePause

ALL_ACTIONS = [
    NavigateUp(), 
    NavigateRight(), 
    NavigateDown(), 
    NavigateLeft(), 
    Reveal(),
    Flag(),
    TogglePause(),
    Exit()
]