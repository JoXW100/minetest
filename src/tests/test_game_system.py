import unittest as ut
import os
import sys
import subprocess

class TestGameSystem(ut.TestCase):
    def __run_subprocess(self, file: str, seed: int = None, timeout: float = 5.0) -> tuple[str, int]:
        # The absolute path to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        # the absolute path to the game executable in the parent directory
        game_path = os.path.join(parent_dir, 'game.py')
        # the absolute path to the input file in the input subdirectory
        input_path = os.path.join(current_dir, 'input', f"{file}.txt")
        cmd = [sys.executable, game_path, '--input=native', '--ignore-size']
        # Set PYTHONIOENCODING environment variable to change default encoding
        # for all subprocess function
        environ = os.environ.copy()
        environ['PYTHONIOENCODING'] = 'utf-8'
        
        # if a seed was specified, add the seed command line argument
        if (seed != None):
            cmd.append('--seed=' + str(seed))
        
        # open input file and route the content to the standard input of the 
        # subprocess executing the game
        with open(input_path, encoding='utf-8') as input:
            result = subprocess.run(cmd, stdin=input, encoding='utf-8', capture_output=True, env=environ, timeout=timeout)
            return (result.stdout, result.returncode)
    
    def test_quit(self):
        result, code = self.__run_subprocess('quit')
        self.assertEqual(0, code)
        self.assertIn("Exiting...", result)
    
    def test_start_game(self):
        _, code = self.__run_subprocess('start_game')
        self.assertEqual(0, code)
    
    def test_game_has_prompts(self):
        result, _ = self.__run_subprocess('start_game')
        self.assertIn("Navigate up", result)
        self.assertIn("Navigate right", result)
        self.assertIn("Navigate down", result)
        self.assertIn("Navigate left", result)
        self.assertIn("[D] Reveal cell", result)
        self.assertIn("[F] Flag cell", result)
        self.assertIn("[P] Pause/Unpause", result)
        self.assertIn("[Q] Exit", result)
    
    def test_play_game_and_loose(self):
        result, _ = self.__run_subprocess('play_game_loose_seed_1', seed=1)
        self.assertIn("You revealed a mine, you lost", result)
    
    def test_play_game_and_win(self):
        result, _ = self.__run_subprocess('play_game_win_seed_1', seed=1)
        self.assertIn("You Won!", result)

TestGameSystem().test_start_game()