import structure as st

class GameData:
    """
    
    """
    def __init__(self):
        self.size:int = 5
        self.players:list[st.Player] = []
        self.difficulty:int = 1
        self.colors:list[str] = []
        self.data = {}