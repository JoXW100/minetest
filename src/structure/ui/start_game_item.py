import random
import game_loop
import structure.ui as ui
from structure import GameState, GameData
from structure.actions import ALL_ACTIONS

class StartGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'S'
        self._title = 'Start Game'
    
    def start(self, data: GameData):
        state = GameState(ALL_ACTIONS,
                          data.size,
                          data.mines,
                          ignore_size=data.ignore_size)
        if data.seed is not None:
            random.seed(data.seed)
        game_loop.run(state, data.input_mode)
        # Back to main menu
        raise ui.MenuEvent(2)