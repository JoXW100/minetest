from structure import GameState, Player, GameStatus
from structure.actions import ALL_ACTIONS
from pynput import keyboard
import os

global user_input

def handle_victory(state: GameState) -> bool:
    status = state.get_game_status()
    if status is GameStatus.Playing:
        return True
    if status is GameStatus.Won:
        print("You Won!")
    if status is GameStatus.Lost:
        print("You Lost!")
    return False

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def run(state : GameState):
    def on_press(key):
        try:
            if key.char == "c":
                user_input = "c"
            elif key.char == "v":
                user_input == "v"
            state.player.perform_turn(state, key_input)
        except AttributeError:
            pass
        
    with keyboard.Listener(on_press=on_press) as listener:
        while handle_victory(state):
            clear_terminal()
            state.print_board()

            # Block and listen for key press.
            key_input = listener.join()
            state.player.perform_turn(state, key_input)

if __name__ == "__main__":
    gs = GameState(ALL_ACTIONS, 5, 16)
    run(gs)