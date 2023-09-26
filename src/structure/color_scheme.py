"""Color scheme administration for printing to the terminal."""
import structure as st

class ColorScheme:
    """
    Singleton class for managing colors used when printing the game to the
    terminal.

    Methods
    -------
    set_color_scheme(scheme_name : str) -> bool
        Sets the color scheme to one of the available presets
    get_color_schemes() -> [str]
        Gets a list of all available color schemes
    get_color(element_name : str) -> str
        Gets the color for element_name from the current color scheme
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ColorScheme, cls).__new__(cls)

            color_map = st.Color.color_map
            cls._instance._presets = {
                'default': {
                    'flag': color_map["red"],
                    'number_1': color_map["blue"],
                    'number_2': color_map["green"],
                    'number_3': color_map["red"],
                    'number_4': color_map["navy"],
                    'number_5': color_map["magenta"],
                    'number_6': color_map["cyan"],
                    'number_7': color_map["black"],
                    'number_8': color_map["white"],
                    'bomb': color_map["red"],
                    'selected': color_map["green"],
                },
                'boring': {
                    'flag': color_map["black"],
                    'number_1': color_map["blue"],
                    'number_2': color_map["blue"],
                    'number_3': color_map["blue"],
                    'number_4': color_map["blue"],
                    'number_5': color_map["blue"],
                    'number_6': color_map["blue"],
                    'number_7': color_map["blue"],
                    'number_8': color_map["blue"],
                    'bomb': color_map["red"],
                    'selected': color_map["green"],
                }
            }
            cls._instance._current_scheme = "default"

        return cls._instance

    def set_color_scheme(self, scheme_name):
        """
        Set the current color scheme. If the color scheme is not in the list
        of available color schemes (found from get_color_schemesl), nothing
        is changed.

        Attributes:
        -------
        scheme_name: str
            The name of the color scheme to set
        """
        if scheme_name in self._presets:
            self._current_scheme = scheme_name
    
    def cycle_color_scheme(self):
        """
        Sets the current color scheme to the next one in the presets list.
        Useful for cycling color schemes in a menu.
        """
        presets = list(self._presets.keys())
        self._current_scheme = presets[(presets.index(
            self._current_scheme) + 1) % len(presets)]

    def get_current_scheme(self) -> str:
        """
        Retrieves the currently selected color scheme

        Returns
        -------
        scheme_name: str
            The name of the color scheme to set
        """
        return self._current_scheme

    def get_color_schemes(self) -> [str]:
        """
        Retrieves a list of all available color schemes.

        Returns
        -------
        color_schemes: [str]
            A list of all available color schemes.
        """
        return self._presets.keys()

    def get_color(self, element_name) -> str:
        """
        Get the color for a specific element in the current color scheme. If the
        color is not supported by the current preset, fallback to the 'default'
        color scheme.

        Attributes
        ----------
            element_name (str): The name of the element (e.g., 'flag', 'number_1').

        Returns
        -------
        color: str
            The hexadecimal color code.
        """
        return self._presets[self._current_scheme].get(element_name, None)