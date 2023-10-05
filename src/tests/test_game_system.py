import unittest as ut
import os
import sys
import subprocess


class TestGameSystem(ut.TestCase):
    def __run_subprocess(
        self, file: str, seed: int = None, timeout: float = 5.0
    ) -> tuple[str, int]:
        # The absolute path to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        # the absolute path to the game executable in the parent directory
        game_path = os.path.join(parent_dir, "game.py")
        # the absolute path to the input file in the input subdirectory
        input_path = os.path.join(current_dir, "input", f"{file}.txt")
        cmd = [sys.executable, game_path, "--input=native", "--ignore-size"]
        # Set PYTHONIOENCODING environment variable to change default encoding
        # for all subprocess function
        environ = os.environ.copy()
        environ["PYTHONIOENCODING"] = "utf-8"

        # if a seed was specified, add the seed command line argument
        if seed is not None:
            cmd.append("--seed=" + str(seed))

        # open input file and route the content to the standard input of the
        # subprocess executing the game
        with open(input_path, encoding="utf-8") as input_file:
            result = subprocess.run(
                cmd,
                stdin=input_file,
                encoding="utf-8",
                capture_output=True,
                env=environ,
                timeout=timeout,
                check=False,
            )

            return (result.stdout, result.returncode)

    def test_quit(self):
        result, code = self.__run_subprocess("quit")
        self.assertEqual(0, code)
        self.assertIn("Exiting...", result)

    def test_start_game(self):
        _, code = self.__run_subprocess("start_game")
        self.assertEqual(0, code)

    def test_game_has_prompts(self):
        result, _ = self.__run_subprocess("start_game")
        self.assertIn("Navigate up", result)
        self.assertIn("Navigate right", result)
        self.assertIn("Navigate down", result)
        self.assertIn("Navigate left", result)
        self.assertIn("[D] Reveal cell", result)
        self.assertIn("[F] Flag cell", result)
        self.assertIn("[P] Pause/Unpause", result)
        self.assertIn("[Q] Exit", result)

    def test_play_game_and_loose(self):
        result, _ = self.__run_subprocess("play_game_loose_seed_1", seed=1)
        self.assertIn("You revealed a mine, you lost", result)

    def test_play_game_and_win(self):
        result, _ = self.__run_subprocess("play_game_win_seed_1", seed=1)
        self.assertIn("You Won!", result)

    def test_play_game_easy(self):
        result, _ = self.__run_subprocess("play_standard_easy_seed_1", seed=1)
        self.assertIn("Difficulty: Easy", result)
        self.assertIn("│ ■ ■ ■ ■ ■ │", result)

    def test_play_game_medium(self):
        result, _ = self.__run_subprocess("play_standard_medium_seed_1", seed=1)
        self.assertIn("Difficulty: Medium", result)
        self.assertIn("│ ■ ■ ■ ■ ■ ■ ■ ■ ■ │", result)

    def test_play_game_hard(self):
        result, _ = self.__run_subprocess("play_standard_hard_seed_1", seed=1)
        self.assertIn("Difficulty: Hard", result)
        self.assertIn("│ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ │", result)

    def test_play_custom_small(self):
        result, _ = self.__run_subprocess("play_custom_small_seed_1", seed=1)
        self.assertIn("Board Size: 4x4", result)
        self.assertIn("│ ■ ■ ■ ■ │", result)

    def test_play_custom_large(self):
        result, _ = self.__run_subprocess("play_custom_large_seed_1", seed=1)
        self.assertIn("Board Size: 12x12", result)
        self.assertIn("│ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ │", result)

    def test_play_custom_min_mines(self):
        result, _ = self.__run_subprocess("play_custom_min_mines_seed_1", seed=1)
        self.assertIn("Mines: 1", result)
        self.assertIn("You Won!", result)

    def test_play_custom_max_mines(self):
        result, _ = self.__run_subprocess("play_custom_max_mines_seed_1", seed=1)
        self.assertIn("Mines: 15", result)
        self.assertIn("You Won!", result)

    def play_pause_quit(self):
        result, _ = self.__run_subprocess("play_pause_quit")
        self.assertIn("Game is paused!", result)
        self.assertIn("Exiting...", result)

    def play_reveal_revealed(self):
        result, _ = self.__run_subprocess("play_reveal_revealed")
        self.assertIn("You revealed a mine, you lost.", result)

    def test_invalid_mines(self):
        result, _ = self.__run_subprocess("invalid_mines")
        count = result.count("Invalid value")
        self.assertGreaterEqual(count, 2)
        self.assertIn("Exiting...", result)

    def test_invalid_input(self):
        result, _ = self.__run_subprocess("invalid_input")
        count = result.count("Invalid option...")
        self.assertGreaterEqual(count, 22)
        self.assertIn("Exiting...", result)

    def random_menu_navigation(self):
        result, _ = self.__run_subprocess("random_menu_navigation")
        self.assertIn("Exiting...", result)
