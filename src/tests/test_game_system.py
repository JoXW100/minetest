import unittest as ut
from subprocess import STDOUT, check_output

class TestGameSystem(ut.TestCase):
    def __run_subprocess(self, file: str, seed: int = None, timeout: float = 5.0) -> str:
        cmd = ['python', 'src/game.py', '--input=native', '--ignore-size']
        
        if (seed != None):
            cmd.append('--seed=' + str(seed))
            
        with open('src/tests/input/' + file + '.txt') as res:
            result = check_output(cmd, stdin=res, stderr=STDOUT, timeout=timeout)
            return str(result)
    
    def test_quit(self):
        result = self.__run_subprocess('quit')
        self.assertIn("Exiting...", result)
    
    def test_start_game(self):
        result = self.__run_subprocess('start_game')
        self.assertIn("Exiting...", result)
    
    def test_game_has_prompts(self):
        result = self.__run_subprocess('start_game')
        self.assertIn("Navigate up", result)
        self.assertIn("Navigate right", result)
        self.assertIn("Navigate down", result)
        self.assertIn("Navigate left", result)
        self.assertIn("[D] Reveal cell", result)
        self.assertIn("[F] Flag cell", result)
        self.assertIn("[P] Pause/Unpause", result)
        self.assertIn("[Q] Exit", result)
    
    def test_play_game_and_loose(self):
        result = self.__run_subprocess('play_game_loose_seed_1', seed=1)
        self.assertIn("You revealed a mine, you lost", result)
    
    def test_play_game_and_win(self):
        result = self.__run_subprocess('play_game_win_seed_1', seed=1)
        self.assertIn("You Won!", result)