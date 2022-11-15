import structure.ui as ui

class EasyDifficultyItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'E'
        self._title = 'Easy'
    
    def start(self, data) -> bool:
        data.difficulty = 0
        raise ui.MenuEvent()

class MediumDifficultyItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'M'
        self._title = 'Medium'
    
    def start(self, data) -> bool:
        data.difficulty = 1
        raise ui.MenuEvent()

class DifficultDifficultyItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'D'
        self._title = 'Difficult'
    
    def start(self, data) -> bool:
        data.difficulty = 2
        raise ui.MenuEvent()

class DifficultyMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'D'
        self._title = 'Difficulty'
        self._options = [
            EasyDifficultyItem(),
            MediumDifficultyItem(),
            DifficultDifficultyItem(),
            ui.BackItem(),
            ui.QuitItem()
        ]
    
    def update(self, data):
        assert len(data.players) == 2
        self._info = '    Difficulty: ' \
            + ['Easy', 'Medium', 'Difficult'][data.difficulty] \
            + '\n---'