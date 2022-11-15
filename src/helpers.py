import structure as st
import os, sys, re

def get_location(state: st.GameState):
    """
    Requests a Location from the user and returns it

    Attributes
    ----------
    state : GameState
        the current game state

    Returns
    -------
    location : Location
        a Location object representing the user's input
    """
    while True:
        try:
            text = input("Enter Position: ")
            res = re.search('([a-z])([0-9])$', text.lower())
            if res is None:
                raise Exception('Failed match')
            else:
                x = ord(res.group(1)) - 97
                y = int(res.group(2)) - 1
                if x < 0 or x >= state.board.size or y < 0 or y >= state.board.size:
                    print('Position is out of board range')
                else:
                    return st.Location(x, y)
        except:
            print("Position must be in the format [A-Z][1-9]")

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w', encoding="utf-8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        