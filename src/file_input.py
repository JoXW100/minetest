import time
from subprocess import Popen, PIPE, STDOUT, CREATE_NEW_CONSOLE
from pynput.keyboard import Controller, Key

def convert_to_list(file_path: str) -> list:
    command_to_key = {
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right
    }
    
    converted_list = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line in command_to_key:
                converted_list.append(command_to_key[line])
            else:
                converted_list.append(line)
                
    return converted_list
    
def main():
    commands = convert_to_list("system_test.txt")
    
    MENU_COMMANDS = 2
    EXIT_COMMANDS = 2
    menu_commands = commands[:MENU_COMMANDS]
    game_commands = commands[MENU_COMMANDS:-EXIT_COMMANDS]
    exit_commands = commands[-EXIT_COMMANDS:]
    
    # Either open new console or write to file
    # TODO: Fix file encoding errors 
    p = Popen(["python", "game.py", "--seed", "1337"], stdin=PIPE, creationflags=CREATE_NEW_CONSOLE, stderr=STDOUT, text=True, bufsize=0, universal_newlines=True)
    # p = Popen(["python", "game.py", "--seed", "1337"], stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0, text=True, encoding="utf-8", shell=True)

    time.sleep(1)
    for command in menu_commands:
        p.stdin.write(str(command) + "\n")
        p.stdin.flush()
    
    time.sleep(0.5)
    kb = Controller()
    for command in game_commands:
        kb.press(command)
        kb.release(command)
        time.sleep(0.1)
    
    time.sleep(0.5)
    for command in exit_commands:
        p.stdin.write(str(command) + "\n")
        time.sleep(0.1)
    
    p.stdin.flush()
    
    # Save stdout to file
    # with open("out.txt", "w") as f:
        # f.write(p.stdout.read())
    
    time.sleep(3)
    p.kill()
    
if __name__ == "__main__":
    main()
