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
    input_mode : str
        board input mode
    seed : int|None
        random seed
    ignore_size : bool
        ignore board size (True/False)
    """
    def __init__(self):
        self.size:int = 5
        self.mines:int = 5
        self.difficulty:int = 1
        self.input_mode:str = 'pynput'
        self.seed:int = None
        self.ignore_size = False