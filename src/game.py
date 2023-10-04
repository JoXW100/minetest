import argparse
from structure import GameData
from structure.ui import MainMenu

def parse_args() -> argparse.Namespace:
    """
    Parses the arguments given to the program.

    Returns:
    --------
    args : argparse.Namespace
        Namespace containing the parsed arguments.   
    """
    parser = argparse.ArgumentParser(description='The minesweeper game.')
    parser.add_argument('--seed', required=False, 
                        default=None, 
                        type=int, 
                        help='An integer seed')
    parser.add_argument('--input', 
                        required=False, 
                        default='pynput', 
                        type=str, 
                        help='input mode')
    parser.add_argument('--ignore-size', 
                        dest='ignore_size', 
                        action=argparse.BooleanOptionalAction, 
                        default=False, 
                        type=bool, 
                        help='Terminal size is ignored, vertical mode is used')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    # Set the input mode to use in the game loop.
    data = GameData()
    data.input_mode = args.input
    data.seed = args.seed
    data.ignore_size = args.ignore_size
    MainMenu().open(data)
        
if __name__ == "__main__":
    main()