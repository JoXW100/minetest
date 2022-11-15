from .test_game_state import run_game_state_tests
from .test_structure import run_structure_tests
from .test_ai import run_ai_tests
from .test_move import run_move_tests
from .test_insert import run_insert_tests
from .test_flip import run_flip_tests
from .test_file_handler import run_file_handler_tests

ALL_TESTS = [run_structure_tests,
             run_game_state_tests, 
             run_insert_tests,
             run_flip_tests,
             run_move_tests,
             run_file_handler_tests,
             run_ai_tests]