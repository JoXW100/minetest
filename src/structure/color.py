import os

os.system('color')

class Color:
    """
    Contains functions related to printing to terminal with color
    
    Attributes
    ----------
    BLACK : str
    RED : str
    YELLOW : str
    BLUE : str
    PURPLE : str
    CYAN : str
    WHITE :
    
    Methods
    -------
    color_print(color: str, text: str)
        Prints the given text in the specified color
    
    color_print_sequence(color: list[str], text:  list[str])
        Prints a sequence in the given colors
    """
    
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    WHITE  = '\033[37m'
    
    @staticmethod
    def colored_text(color: str, text: str) -> str:
        """
        Prepares an input string for colored terminal printing

        Attributes
        ----------
        color : str
            The color to print the text in
        text : str
            The text to print in color
        Returns
        -------
        output : str
            Colored text output ready to be printed
        """
        return color + text + Color.WHITE
    
    @staticmethod
    def color_print(color: str, text: str):
        """
        Prints the given text in the specified color

        Attributes
        ----------
        color : str
            The color to print the text in
        text : str
            The text to print in color
        """
        print(Color.colored_text(color, text))
    
    @staticmethod
    def color_print_sequence(colors: list[str], text: list[str]):
        """
        Prints a sequence in the given colors

        Attributes
        ----------
        colors : list[str]
            the colors to use for the different sections
        text : list[str]
            the tests to print in different colors
        """
        if len(colors) != len(text):
            raise AssertionError
        result = ""
        for i in range(len(colors)):
            result += colors[i] + text[i]
            
        print(result + Color.WHITE)