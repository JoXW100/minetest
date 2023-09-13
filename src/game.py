from structure.ui import MainMenu
import argparse
import random

def parse_args() -> int:
    parser = argparse.ArgumentParser(description='The minesweeper game.')
    parser.add_argument('--seed', required=False, default=None, type=int, help='An integer seed')
    args = parser.parse_args()
    return args.seed

def main():
    seed = parse_args()
    if (seed is not None):
        random.seed(seed)
    MainMenu().open()
        
if __name__ == "__main__":
    main()