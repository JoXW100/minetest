from pynput.keyboard import Key, KeyCode

navigation_keys = {
    "i": Key.up,
    "j": Key.left,
    "k": Key.down,
    "l": Key.right,
}

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

    if (len(str_key ) < 1):
        return Key.enter

    if (str_key in navigation_keys):
        return navigation_keys[str_key]

    return KeyCode.from_char(str_key)
