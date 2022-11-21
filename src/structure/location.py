class Location:
    """
    A class used to represent an xy location in the game

    Attributes
    ----------
    x : int
        x position, starting from 0
    y : int
        y position, starting from 0

    Methods
    -------
    validate(limit: int)
        checks if the location is within bounds
    """
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        
    @property
    def x(self) -> int:
        return self.__x
        
    @property
    def y(self) -> int:
        return self.__y
    
    def validate(self, limit: int) -> bool:
        """
        Validates the location coordinates to be within a given limit
        
        Attributes
        ----------
        limit : int
            The limit to check if the coordinates are within (exclusive)

        Returns
        -------
        valid : bool
            True if the coordinates are within the limit, otherwise False
        """

        return self.__x >= 0 \
            and self.__x < limit \
            and self.__y >= 0 \
            and self.__y < limit
    
    def __str__(self) -> str:
        return '(' + str(self.x) + ', ' + str(self.y) + ')' 
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other):
        return isinstance(other, Location) \
            and self.x == other.x \
            and self.y == other.y
            
    def __hash__(self) -> int:
        return ((self.x + self.y) * (self.x + self.y + 1) >> 1) + self.y