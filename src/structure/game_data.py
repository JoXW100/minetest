class GameData:
    """
    Persistent data when navigating between menus.
    
    Attributes
    ----------
    size : int
        the size of the board
    mines : int
        the number of mines on the board
    difficulty : int
        the difficulty index
    """
    def __init__(self):
        self.size:int = 5
        self.mines = 5
        self.difficulty:int = 1