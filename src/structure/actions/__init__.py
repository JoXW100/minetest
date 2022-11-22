from .exit import Exit
from .navigate import NavigateUp, NavigateRight, NavigateDown, NavigateLeft
from .reveal import Reveal

ALL_ACTIONS = [
    NavigateUp(), 
    NavigateRight(), 
    NavigateDown(), 
    NavigateLeft(), 
    Reveal(),
    Exit()
]