import structure.ui as ui

class NextPlayerItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'N'
        self._title = 'Next Player'

    def start(self, data) -> bool:
        data.data['change_order_index'] += 1
        return False

class PrevPlayerItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'P'
        self._title = 'Previous Player'

    def start(self, data) -> bool:
        data.data['change_order_index'] -= 1
        return False

class MovePlayerItem(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'M'
        self._title = 'Move Player Down'

    def start(self, data) -> bool:
        index = data.data['change_order_index'] % len(data.players)
        swap_index = (index + 1) % len(data.players)
        player = data.players[index]
        data.players[index] = data.players[swap_index]
        data.players[swap_index] = player
        return False
        
class ChangePlayerOrderMenu(ui.MenuItem):
    def __init__(self):
        super().__init__()
        self._key = 'O'
        self._title = 'Change Player Order'
        self._options = [
            NextPlayerItem(),
            PrevPlayerItem(),
            MovePlayerItem(),
            ui.BackItem(),
            ui.QuitItem()
        ]
    
    def update(self, data):
        self._info = '    Players: '
        for i in range(len(data.players)):
            self._info += ('\n →  ' if data.data['change_order_index'] == i else '\n    ') \
                + str(data.players[i])
        self._info += '\n---'
    
    def start(self, data) -> bool:
        data.data['change_order_index'] = 0
        return True