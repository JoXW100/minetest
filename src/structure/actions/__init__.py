from .exit import Exit
from .navigate import NavigateUp, NavigateRight, NavigateDown, NavigateLeft

ALL_ACTIONS = [
    NavigateUp(), 
    NavigateRight(), 
    NavigateDown(), 
    NavigateLeft(), 
    Exit()
]