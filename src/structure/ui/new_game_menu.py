import structure.ui as ui
    
class NewGameMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'N'
        self._title = 'Start new game'
        self._options = [
            ui.AVAMenu(),
            ui.PVPMenu(), 
            ui.PVAMenu(),
            ui.LoadGameMenu(),
            ui.BackItem(), 
            ui.QuitItem()
        ]