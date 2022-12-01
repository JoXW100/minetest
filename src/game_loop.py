from structure import GameState, GameStatus
from structure.actions import ALL_ACTIONS
from pynput import keyboard
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_victory(state: GameState) -> bool:
    status = state.get_game_status()
    if status is GameStatus.Playing:
        return True
    if status is GameStatus.Won:
        clear_terminal()
        state.set_flag_on_mines()
        state.print_board()
        print("You Won!\n\n")
        input("Press enter to continue...")
    if status is GameStatus.Lost:
        clear_terminal()
        state.reveal_mines()
        state.print_board()
        print("You revelead a mine, you lost.\n\n")
        input("Press enter to continue...")
            
    return False

# use for debug and testing
global listener

def run(state : GameState):
    def on_press(key):
        res = state.player.perform_turn(state, key)
        return not res
    
    while handle_victory(state):
        clear_terminal()
        state.print_board()
        state.print_actions()
        with keyboard.Listener(on_press=on_press) as listener:
            # Block and listen for key press.
            keyboard.Listener.join(listener)

if __name__ == "__main__":
    gs = GameState(ALL_ACTIONS, 5, 8)
    run(gs)