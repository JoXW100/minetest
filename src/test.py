from structure import GameState, Location, Direction
from structure.actions import ALL_ACTIONS

gs = GameState(ALL_ACTIONS, 5, 16)

if __name__ == "__main__":
    gs.print_board()
    gs.board.reveal_and_distribute(Location(0,0), 16)
    gs.print_board()