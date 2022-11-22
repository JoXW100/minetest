import structure.ui as ui
from structure import GameData

class EasyDifficultyItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'E'
        self._title = 'Easy (5x5)'
    
    def start(self, data) -> bool:
        data.difficulty = 0
        data.size = 5
        data.mines = 4
        raise ui.MenuEvent()

class MediumDifficultyItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'M'
        self._title = 'Medium (9x9)'
    
    def start(self, data) -> bool:
        data.difficulty = 1
        data.size = 9
        data.mines = 15
        raise ui.MenuEvent()

class HardDifficultyItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'H'
        self._title = 'Hard (12x12)'
    
    def start(self, data) -> bool:
        data.difficulty = 2
        data.size = 12
        data.mines = 35
        raise ui.MenuEvent()

class DifficultyMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'D'
        self._title = 'Change Difficulty'
        self._options = [
            EasyDifficultyItem(),
            MediumDifficultyItem(),
            HardDifficultyItem(),
            ui.BackItem(),
            ui.QuitItem()
        ]
    
    def update(self, data: GameData):
        self._info = '    Difficulty: ' \
            + ['Easy', 'Medium', 'Hard'][data.difficulty] + '\n---'