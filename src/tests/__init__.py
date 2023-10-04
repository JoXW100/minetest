from .test_game_rules import TestGameRules
from .test_game_system import TestGameSystem

ALL_TESTS = [
    TestGameRules().test_change_difficulty,
    TestGameRules().test_flag_on_flagged_cell,
    TestGameRules().test_flag_on_hidden_cell,
    TestGameRules().test_change_difficulty,
    TestGameRules().test_navigation_action,
    TestGameSystem().test_quit,
    TestGameSystem().test_start_game,
    TestGameSystem().test_game_has_prompts,
    TestGameSystem().test_play_game_and_loose,
    TestGameSystem().test_play_game_and_win
]