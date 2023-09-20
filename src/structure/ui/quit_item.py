import sys
import structure.ui as ui
   
class QuitItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'Q'
        self._title = 'Quit'
    
    def start(self, _):
        sys.exit("Exiting..")