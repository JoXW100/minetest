"""Color scheme administration for printing to the terminal."""
import structure as st

class ColorScheme:
    """
    Static class for managing colors used when printing the game to the
    terminal.

    Methods
    -------
    def cycle_color_scheme():
        Cycles the current color scheme to the next one in order of the
        available color schemes. Useful for cycling color schemes in a menu
    def get_current_scheme() -> str:
        Retrieves the currently selected color scheme
    def get_color_schemes() -> list[str]:
        Gets a list of all available color schemes
    def get_color(element_name) -> str:
        Gets the color for element_name from the current color scheme
    """

    __DEFAULT_PRESET = 'default'

    __COLOR_MAP = st.Color.COLOR_MAP
    __CURRENT_SCHEME = __DEFAULT_PRESET
    __PRESETS = {
        __DEFAULT_PRESET: {
            'flag': __COLOR_MAP["red"],
            'number_1': __COLOR_MAP["blue"],
            'number_2': __COLOR_MAP["green"],
            'number_3': __COLOR_MAP["red"],
            'number_4': __COLOR_MAP["navy"],
            'number_5': __COLOR_MAP["magenta"],
            'number_6': __COLOR_MAP["cyan"],
            'number_7': __COLOR_MAP["black"],
            'number_8': __COLOR_MAP["white"],
            'bomb': __COLOR_MAP["red"],
            'selected': __COLOR_MAP["green"],
        },
        'boring': {
            'flag': __COLOR_MAP["black"],
            'number_1': __COLOR_MAP["blue"],
            'number_2': __COLOR_MAP["blue"],
            'number_3': __COLOR_MAP["blue"],
            'number_4': __COLOR_MAP["blue"],
            'number_5': __COLOR_MAP["blue"],
            'number_6': __COLOR_MAP["blue"],
            'number_7': __COLOR_MAP["blue"],
            'number_8': __COLOR_MAP["blue"],
            'bomb': __COLOR_MAP["red"],
            'selected': __COLOR_MAP["green"],
        },
        'wild': {
            'flag': __COLOR_MAP["magenta"],
            'bomb': __COLOR_MAP["white"],
            'selected': __COLOR_MAP["magenta"],
        }
    }

    @staticmethod
    def cycle_color_scheme():
        """
        Cycles the current color scheme to the next one in order of the
        available color schemes. Useful for cycling color schemes in a menu
        """
        presets = list(ColorScheme.__PRESETS.keys())

        # Calculate next idx (this loops around)
        next_idx = (presets.index(ColorScheme.__CURRENT_SCHEME) + 1) % len(presets)

        ColorScheme.__CURRENT_SCHEME = presets[next_idx]

    @staticmethod
    def get_current_scheme() -> str:
        """
        Retrieves the currently selected color scheme

        Returns
        -------
        scheme_name : str
            The name of the color scheme to set
        """
        return ColorScheme.__CURRENT_SCHEME

    @staticmethod
    def get_color_schemes() -> list[str]:
        """
        Retrieves a list of all available color schemes.

        Returns
        -------
        color_schemes : list[str]
            A list of all available color schemes.
        """
        return ColorScheme.__PRESETS.keys()

    @staticmethod
    def get_color(element_name) -> str:
        """
        Get the color for a specific element in the current color scheme. If the
        color is not supported by the current preset, fallback to the default
        color scheme.

        Attributes
        ----------
        element_name : str
            The name of the element (e.g., 'flag', 'number_1')

        Returns
        -------
        color : str | None
            The hexadecimal color code or None if the color is not defined in
            the currently selected color scheme or the default color scheme.
        """
        # Lookup the color in the current preset.
        preset_color = ColorScheme.__PRESETS[ColorScheme.__CURRENT_SCHEME].get(element_name, None)

        # If the color is defined in the current preset, return it.
        if preset_color is not None:
            return preset_color

        # Otherwise, try to get it from the default preset.
        return ColorScheme.__PRESETS[ColorScheme.__DEFAULT_PRESET].get(element_name, None)
