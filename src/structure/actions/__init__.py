from .exit import Exit
from .navigate import NavigateUp, NavigateRight, NavigateDown, NavigateLeft
from .reveal import Reveal
from .flag import Flag

ALL_ACTIONS = [
    NavigateUp(), 
    NavigateRight(), 
    NavigateDown(), 
    NavigateLeft(), 
    Reveal(),
    Flag(),
    Exit()
]