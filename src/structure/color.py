import os, re

os.system('color')

class Color:
    """
    Contains functions related to printing to terminal with color
    
    Attributes
    ----------
    color_map : dict{str : str}
        Name to ANSI color string map
    
    Methods
    -------
    color_print(color: str, text: str)
        Prints the given text in the specified color
    
    color_print_sequence(color: list[str], text:  list[str])
        Prints a sequence in the given colors
    """
    color_map = {
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

    @staticmethod
    def ansi_translate(color_name: str) -> str:
        """
        Converts a color string to an ANSI color code string

        Attributes
        ----------
        color_name : str
            The name of the color

        Returns
        -------
        ansi_color : str
            The ANSI color code corresponding to color_name if available,
            otherwise the ANSI color code for white.
        """
        if color_name in Color.color_map:
            return Color.color_map[color_name]
        else:
            return Color.color_map["white"]

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
        return color + text + Color.color_map["reset"]

    @staticmethod
    def remove_color(text: str) -> str:
        """
        Remove ANSI color codes from a string based on the provided color map.

        Args:
            input_string (str): The input string containing ANSI color codes.
            color_map (dict): A dictionary mapping color names to ANSI color codes.

        Returns:
            str: The input string with ANSI color codes removed.
        """
        pattern = r'\033\[\d+m'  # Regular expression pattern to match ANSI color codes
        for _, color_code in Color.color_map.items():
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
            
        print(result + Color.color_map["reset"])

    