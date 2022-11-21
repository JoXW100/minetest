from structure import GameState, GameStatus
from structure.actions import ALL_ACTIONS
from pynput import keyboard
import os

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
        res = state.player.perform_turn(state, key)
        return res and handle_victory(state)
    
    with keyboard.Listener(on_press=on_press) as listener:
        clear_terminal()
        state.print_board()

        # Block and listen for key press.
        listener.join()

if __name__ == "__main__":
    gs = GameState(ALL_ACTIONS, 5, 16)
    run(gs)