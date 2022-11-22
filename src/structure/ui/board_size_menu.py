import structure.ui as ui
from structure import GameData

class Size5Item(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'A'
        self._title = '5x5'
    
    def start(self, data) -> bool:
        data.difficulty = 0
        raise ui.MenuEvent()

class Size12Item(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'S'
        self._title = '12x12'
    
    def start(self, data) -> bool:
        data.size = 12
        raise ui.MenuEvent()

class BoardSizeMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'C'
        self._title = 'Change Board Size'
        self._options = [
            Size5Item(),
            Size12Item(),
            ui.BackItem(),
            ui.QuitItem()
        ]
    
    def update(self, data: GameData):
        self._info = '    Size: ' \
            + str(data.size) + 'x' + str(data.size) + '\n---'