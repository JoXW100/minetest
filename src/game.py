import argparse
import random
import os
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
    parser.add_argument('--seed', required=False, default=None, type=int, help='An integer seed')
    parser.add_argument('--input', required=False, default='pynput', type=str, help='input mode')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    seed = args.seed
    os.environ['INPUT_MODE'] = args.input
    if (seed is not None):
        random.seed(seed)
    MainMenu().open()
        
if __name__ == "__main__":
    main()