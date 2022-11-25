from structure import GameState
from structure import GameData
from structure.actions import ALL_ACTIONS
import structure.ui as ui
import game_loop

class StartGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'S'
        self._title = 'Start Game'
    
    def start(self, data: GameData):
        state = GameState(ALL_ACTIONS, data.size, data.mines)
        game_loop.run(state)
        # Back to main menu
        raise ui.MenuEvent(2)