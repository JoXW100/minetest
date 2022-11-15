import structure.ui as ui

class NewTournamentMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'T'
        self._title = 'TODO: Start new tournament'
        self._options = []