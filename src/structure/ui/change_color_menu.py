from structure import Player, COLOR_MAP
import structure.ui as ui

def next_color(player: Player):
    for i in range(len(COLOR_MAP)):
        if COLOR_MAP[i] == player.color:
            return COLOR_MAP[(i + 1) % len(COLOR_MAP)]
    return COLOR_MAP[0]

class NextPlayerItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'P'
        self._title = 'Next Player'

    def open(self, data) -> bool:
        data.data['change_color_selection'] += 1
        return False

class NextColorItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'N'
        self._title = 'Next Color'

    def start(self, data) -> bool:
        player = data.players[data.data['change_color_selection'] % len(data.players)]
        player.color = next_color(player)
        return False

class ChangeColorMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'C'
        self._title = 'Change Color'
        self._options = [
            NextPlayerItem(),
            NextColorItem(),
            ui.BackItem(),
            ui.QuitItem()
        ]
    
    def update(self, data):
        player = data.players[data.data['change_color_selection'] % len(data.players)]
        self._info = '    Changing: ' + str(player) + '\n---'
        
    def start(self, data) -> bool:
        data.data['change_color_selection'] = 0
        return True