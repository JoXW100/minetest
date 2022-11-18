from structure import GameState
from structure.actions import ALL_ACTIONS

gs = GameState(ALL_ACTIONS, 5, 16)

if __name__ == "__main__":
    gs.print_board()