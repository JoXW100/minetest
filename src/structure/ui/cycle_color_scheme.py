import structure.ui as ui
from structure import ColorScheme

class CycleColorScheme(ui.MenuItem):
    def __init__(self, num:int = 1):
        super().__init__()
        self._num = num
        self._key = 'C'
        self._title = 'Cycle'
    
    def start(self, _) -> bool:
        ColorScheme().cycle_color_scheme()