import os, re, types

os.system('color')

class Color:
    """
    Contains functions related to printing to terminal with color
    
    Attributes
    ----------
    COLOR_MAP : dict[str, str]
        Name to ANSI color string map
    
    Methods
    -------
    colored_text(color: str, text: str) -> str
        Prepares an input string for colored terminal printing

    remove_color(text: str) -> str
        Remove ANSI color codes from a string based on the provided color map

    color_print(color: str, text: str)
        Prints the given text in the specified color
    
    color_print_sequence(color: list[str], text:  list[str])
        Prints a sequence in the given colors
    """
    __COLOR_MAP = {
        'red': '\033[91m',
        'blue': '\033[94m',
        'navy': '\033[34m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'black': '\033[90m',
        'white': '\033[97m',
        'reset': '\033[0m',
    }

    # Using the MappingProxyType makes the dictionary unable to be modified by
    # anyone
    COLOR_MAP = types.MappingProxyType(__COLOR_MAP)

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
        return color + text + Color.__COLOR_MAP["reset"]

    @staticmethod
    def remove_color(text: str) -> str:
        """
        Remove ANSI color codes from a string based on the provided color map

        Attributes
        ----------
        input_string : str
            The input string containing ANSI color codes
        color_map : dict[str, str] 
            A dictionary mapping color names to ANSI color codes

        Returns
        -------
        text : str
            The input string with ANSI color codes removed
        """
        # Regular expression pattern to match ANSI color codes
        pattern = r'\033\[\d+m'

        for _, color_code in Color.__COLOR_MAP.items():
            pattern += fr'|\033\[\d+m{re.escape(color_code)}'

        return re.sub(pattern, '', text)

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

        for (t, c) in zip(text, colors):
            result += c + t
            
        print(result + Color.__COLOR_MAP["reset"])

    