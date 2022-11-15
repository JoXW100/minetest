from structure.players import AI
import structure.ui as ui

class AVAMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'V'
        self._title = 'AI vs AI'
        self._options = [
            ui.StartGameMenu(), 
            ui.DifficultyMenu(),
            ui.ChangeColorMenu(),
            ui.BackItem(), 
            ui.QuitItem()
        ]
    
    def start(self, data) -> bool:
        data.players = [AI(1), AI(2)]
        return True
    
    def update(self, data):
        assert len(data.players) == 2
        self._info = '    Difficulty: ' \
            + ['Easy', 'Medium', 'Difficult'][data.difficulty] \
            + '\n    Players: ' + str(data.players[0]) \
            + '\n             ' + str(data.players[1]) \
            + '\n---'