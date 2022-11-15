import structure.ui as ui

class BackItem(ui.MenuItem):
    def __init__(self, num:int = 1):
        super().__init__()
        self._num = num
        self._key = 'B'
        self._title = 'Back'
    
    def start(self, _) -> bool:
        raise ui.MenuEvent(self._num)