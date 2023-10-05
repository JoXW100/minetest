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
    TestGameSystem().test_play_game_and_win,
    TestGameSystem().test_play_game_easy,
    TestGameSystem().test_play_game_medium,
    TestGameSystem().test_play_game_hard,
    TestGameSystem().test_play_custom_small,
    TestGameSystem().test_play_custom_large,
    TestGameSystem().test_play_custom_min_mines,
    TestGameSystem().test_play_custom_max_mines,
    TestGameSystem().test_play_pause_quit,
    TestGameSystem().test_play_reveal_revealed,
    TestGameSystem().test_invalid_mines,
    TestGameSystem().test_invalid_input,
    TestGameSystem().test_random_menu_navigation
]