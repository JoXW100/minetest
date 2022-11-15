from structure import GameState, Action
from structure.actions import Load, ALL_ACTIONS
import structure.ui as ui
import game_loop

class LoadGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'L'
        self._title = 'Load Game'
    
    def open(self, data):
        state = GameState(data.players, ALL_ACTIONS, data.size, data.difficulty)
        args = Load.ask_args(state)
        if Load.execute(state, *args) != Action.FAILED:
            game_loop.run(state)
            raise ui.MenuEvent()