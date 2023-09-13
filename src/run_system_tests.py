
import subprocess
import argparse
import pathlib
from pynput.keyboard import Controller, Key

def parse_args() -> int:
    parser = argparse.ArgumentParser(description='Minesweeper system tester.')
    parser.add_argument('--input', required=True, type=pathlib.Path, help='Path to the input data')
    parser.add_argument('--seed', required=False, default=None, type=int, help='An integer seed')
    args = parser.parse_args()
    return args.seed

def main():
    with open("./system_test.txt", "r", encoding="utf-8") as system_test:
        #output = subprocess.run(["python", "game.py", "--seed", "1337"], encoding="utf-8", stdin=system_test)
        p = subprocess.Popen(["python", "game.py", "--seed", "1337"])
        keyboard = Controller()
        while p.poll() is None:
            for c in system_test.read():
                print(c)
                keyboard.tap(c)
                keyboard.tap(Key.enter)


if __name__ == "__main__":
    main()