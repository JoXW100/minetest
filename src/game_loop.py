import os
from pynput import keyboard
from structure import GameState, GameStatus
from structure.actions import ALL_ACTIONS

def clear_terminal():
    """
    Clears the terminal screen.

    Uses 'cls' on Windows and 'clear' on other platforms.
    """
    if os.name == 'nt':  # Check if the operating system is Windows
        os.system('cls')
    else:
        os.system('clear')

def handle_game_state(state: GameState) -> bool:
    """
    Checks whether the game should continue or not. If not, the player has
    won/lost the game and an end screen is shown.
    
    Attributes
    ----------
    state : GameState
        The current state of the game.
    
    Returns
    -------
    should_continue : bool
        True if the game should continue, false if not.
    """
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

# Used for debug and testing
global listener

def run(state : GameState):
    """
    Game loop that runs the game. Prints the board, prints possible actions and
    listens for input from the user.
    
    Attributes
    ----------
    state : GameState
        The current state of the game.
    """
    def on_press(key):
        res = state.player.perform_turn(state, key)
        return not res
    
    # Keep looping while the player has not won/lost yet.
    while handle_game_state(state):
        clear_terminal()
        state.print_board()
        state.print_actions()
        with keyboard.Listener(on_press=on_press) as listener:
            # Block and listen for key press.
            keyboard.Listener.join(listener)