from structure import GameData
import structure.ui as ui

class MainMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._title = 'Main Menu'
        self._options = [
            ui.NewGameMenu(), 
            # ui.NewTournamentMenu(), 
            ui.QuitItem()
        ]
    
    # Catch last menu events
    def open(self, data: GameData = GameData()):
        while True:
            try:
                super().open(data)
            except ui.MenuEvent:
                pass
            