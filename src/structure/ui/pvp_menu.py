import structure.ui as ui
from structure.players import Human
    
class PVPMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'P'
        self._title = 'Player vs Player'
        self._options = [
            ui.StartGameMenu(), 
            ui.ChangeColorMenu(),
            ui.ChangePlayerOrderMenu(),
            ui.BackItem(), 
            ui.QuitItem()
        ]
            
    def start(self, data) -> bool:
        data.players = [Human(1), Human(2)]
        return True
    
    def update(self, data):
        assert len(data.players) == 2
        self._info = '    Players: ' + str(data.players[0]) \
            + '\n             ' + str(data.players[1]) \
            + '\n---'