import structure.ui as ui
from structure.players import Human, AI

class PVAMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'A'
        self._title = 'Player vs AI'
        self._options = [
            ui.StartGameMenu(), 
            ui.DifficultyMenu(),
            ui.ChangeColorMenu(),
            ui.ChangePlayerOrderMenu(),
            ui.BackItem(), 
            ui.QuitItem()
        ]
        
    def start(self, data) -> bool:
        data.players = [Human(1), AI(2)]
        return True
    
    def update(self, data):
        assert len(data.players) == 2
        self._info = '    Difficulty: ' \
            + ['Easy', 'Medium', 'Difficult'][data.difficulty] \
            + '\n    Players: ' + str(data.players[0]) \
            + '\n             ' + str(data.players[1]) \
            + '\n---'