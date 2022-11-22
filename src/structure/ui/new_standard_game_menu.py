import structure.ui as ui
from structure import GameData
    
class NewStandardGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'S'
        self._title = 'Start new standard game'
        self._options = [
            ui.StartGameMenu(),
            ui.DifficultyMenu(),
            ui.BackItem(), 
            ui.QuitItem()
        ]
        
    def start(self, data: GameData) -> bool:
        data.difficulty = 1
        data.size = 9
        data.mines = 15
        return True
        
    def update(self, data: GameData):
        self._info = '    Difficulty: ' \
            + ['Easy', 'Medium', 'Hard'][data.difficulty] + '\n---'