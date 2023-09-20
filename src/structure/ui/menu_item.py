from __future__ import annotations
from abc import ABCMeta
from structure import GameData
import structure.ui as ui

class MenuItem(metaclass = ABCMeta):
    """
    The base menu object handles transitions between menus and keeps a 
    persistent data object to store menu choices.
    """
    
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    def __init__(self):
        self._options: list[MenuItem] = []
        self._title = 'Menu'
        self._key = 'M'
        self._info = ''
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def key(self) -> str:
        return self._key
    
    def update(self, data: GameData):
        """
        Used to update the menu item from changes to the game state
        """
        pass
    
    def start(self, data: GameData) -> bool:
        """
        Used to set the initial menu item from values in the game state,
        returns true if the regular open shall be called
        """
        return True
    
    def open(self, data: GameData):
        """
        The menu was selected, defines how the selection is handled
        """
        if not self.start(data):
            return
        while len(self._options) > 0:
            self.update(data)
            try:
                print(self)
                x = input('Enter option: ').lower()
                for option in self._options:
                    if x == option.key.lower():
                        option.open(data)
                        break
                else: # if did not break
                    print("Invalid option...\n")
            except ui.MenuEvent as err:
                # Used to back multiple steps from the same event
                if err.value > 1:
                    raise ui.MenuEvent(err.value - 1)
                # Back to previous menu
                return
            except EOFError:
                print("Invalid option...\n")
                        
    def __str__(self) -> str:
        text = '\n--- ' + self.title + ' ---\n'
        if any(self._info):
            text += self._info + '\n'
        for option in self._options:
            text += '[' + option.key + '] ' + option.title + '\n'
        return text