from structure import GameState
from structure.actions import ALL_ACTIONS
import structure.ui as ui
import game_loop

class StartGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'S'
        self._title = 'Start Game'
    
    def start(self, data):
        state = GameState(data.players, ALL_ACTIONS, data.size, data.difficulty)
        game_loop.run(state)
        raise ui.MenuEvent(2)