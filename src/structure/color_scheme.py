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

    DEFAULT_PRESET = 'default'
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ColorScheme, cls).__new__(cls)
            cls.__initialized = False
        return cls.__instance
    
    def __init__(self):
        if self.__initialized:
            return
        else:
            self.__initialized = True

        color_map = st.Color.color_map
        self.__presets = {
            ColorScheme.DEFAULT_PRESET: {
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
            },
            'wild': {
                'flag': color_map["magenta"],
                'bomb': color_map["white"],
                'selected': color_map["magenta"],
            }
        }
        self.__current_scheme = ColorScheme.DEFAULT_PRESET

    def set_color_scheme(self, scheme_name):
        """
        Set the current color scheme. If the color scheme is not in the list
        of available color schemes (found from get_color_schemes), nothing
        is changed.

        Attributes:
        -------
        scheme_name: str
            The name of the color scheme to set
        """
        if scheme_name in self.__presets:
            self.__current_scheme = scheme_name
    
    def cycle_color_scheme(self):
        """
        Sets the current color scheme to the next one in the presets list.
        Useful for cycling color schemes in a menu.
        """
        presets = list(self.__presets.keys())

        # Calculate next idx (this loops around )
        next_idx = (presets.index(self.__current_scheme) + 1) % len(presets)

        self.__current_scheme = presets[next_idx]

    def get_current_scheme(self) -> str:
        """
        Retrieves the currently selected color scheme

        Returns
        -------
        scheme_name: str
            The name of the color scheme to set
        """
        return self.__current_scheme

    def get_color_schemes(self) -> list[str]:
        """
        Retrieves a list of all available color schemes.

        Returns
        -------
        color_schemes: list[str]
            A list of all available color schemes.
        """
        return self.__presets.keys()

    def get_color(self, element_name) -> str:
        """
        Get the color for a specific element in the current color scheme. If the
        color is not supported by the current preset, fallback to the default
        color scheme.

        Attributes
        ----------
            element_name (str): The name of the element (e.g., 'flag', 'number_1').

        Returns
        -------
        color: str | None
            The hexadecimal color code or None if the color is not defined in
            the currently selected color scheme or the default color scheme.
        """
        # Lookup the color in the current preset.
        preset_color = self.__presets[self.__current_scheme].get(element_name, None)

        # If the color is defined in the current preset, return it.
        if preset_color is not None:
            return preset_color

        # Otherwise, try to get it from the default preset.
        return self.__presets[ColorScheme.DEFAULT_PRESET].get(element_name, None)
