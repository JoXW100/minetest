import structure.ui as ui
from structure import GameData
    
class NewCustomGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'C'
        self._title = 'Start new custom game'
        self._options = [
            ui.StartGameMenu(),
            ui.MineCountMenu(),
            ui.BoardSizeMenu(),
            ui.BackItem(), 
            ui.QuitItem()
        ]
        
    def update(self, data: GameData):
        self._info = '    Board Size: ' \
            + str(data.size) + 'x' + str(data.size) + '\n' \
            + '    Mines: ' + str(data.mines) + '\n---'