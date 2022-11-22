import structure.ui as ui
from structure import GameData

class MineCountMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'M'
        self._title = 'Change Mine Count'
        self._options = [
            ui.BackItem(),
            ui.QuitItem()
        ]
    
    def start(self, data: GameData) -> bool:
        assert(data.size > 0)
        while True:
            try:
                x = input('Enter new mine count: ').lower()
                value = int(x)
                assert(value > 0)
                assert(value < data.size * data.size)
                data.mines = value
                return False
            except Exception:
                print("Invalid value, please enter an integer between 1 and " + str(data.size * data.size - 1))