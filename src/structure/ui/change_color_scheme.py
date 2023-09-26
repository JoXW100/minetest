import structure.ui as ui
from structure import GameData, ColorScheme
    
class ChangeColorScheme(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self.__color_scheme = ColorScheme()
        self._key = 'F'
        self._title = 'Select color scheme'
        self._options = [
            ui.CycleColorScheme(),
            ui.BackItem(), 
            ui.QuitItem()
        ]
        
    def start(self, data: GameData) -> bool:
        data.size = 4
        data.mines = 5
        return True
        
    def update(self, data: GameData):
        self._info = '    Available Color Schemes:\n'

        selected_color_scheme = self.__color_scheme.get_current_scheme()

        for scheme in self.__color_scheme.get_color_schemes():
            if scheme == selected_color_scheme:
                self._info += "    [*] "
            else:
                self._info += "        "

            self._info += scheme + "\n"
        
