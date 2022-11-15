from .exit import Exit
from .flip import Flip
from .insert import Insert
from .move import Move
from .save import Save
from .load import Load
from .inspect_stack import InspectStack

ALL_ACTIONS = [Exit(), Flip(), Insert(), Move(), InspectStack(), Save(), Load()]