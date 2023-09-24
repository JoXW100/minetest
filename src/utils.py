"""Module providing utility functions"""
from typing import List, TypeVar
from pynput.keyboard import Key, KeyCode

T = TypeVar("T")
def pad_list(lst: List[T], padding: T, pre_pad: int = 0, post_pad: int = 0) -> List[T]:
    """
    Create a new list by concatenating pre_pad copies of padding at the beginning,
    the original list, and post_pad copies of padding at the end.
    """
    return ([padding] * pre_pad) + lst + ([padding] * post_pad)

def translate_key(str_key: str) -> Key:
    """
    Converts user input to a pynput key.

    Parameters
    ----------
    str_key : str
        The user input.

    Returns
    -------
    key : Key
        The key corresponding to the user input.
    """
    navigation_keys = {
        "i": Key.up,
        "j": Key.left,
        "k": Key.down,
        "l": Key.right,
    }

    if (len(str_key ) < 1):
        return Key.enter

    if (str_key in navigation_keys):
        return navigation_keys[str_key]

    return KeyCode.from_char(str_key)
