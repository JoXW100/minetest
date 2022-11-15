from structure import Action, GameState, Color, Location
import helpers

class InspectStack(Action):
    """
    Inspects a specific stack by representing its content.
    """
    @staticmethod
    def get_name():
        return "Inspect Stack"

    @staticmethod
    def check(state: GameState, loc: Location) -> bool:
        if not loc.validate(state.board.size):
            return False
        cell = state.board.rows[loc.y][loc.x]
        return not cell.is_empty

    @staticmethod
    def execute(state: GameState, loc: Location, *args: list[any]) -> int:
        if InspectStack.check(state, loc):
            InspectStack.unsafe_execute(state, loc)
            return Action.IGNORE
        else:
            return Action.FAILED

    @staticmethod
    def unsafe_execute(state: GameState, loc: Location):
        cell = state.board.rows[loc.y][loc.x]
        title_string = "\nInspecting stack of size {ssize} at location {scoord}:".format(
            ssize = cell.size,
            scoord = str(loc)
        )
        print("\033[1m" + title_string + "\033[0m")     # prints in bold
        for piece in cell:
            state = "Standing" if piece.state else "Flat"
            piece_info = "{state} piece belonging to ".format(
                state = state,
            )
            Color.color_print_sequence(
                [piece.owner.color, Color.WHITE, piece.owner.color],
                ["—\t" if not piece.state else "|\t", piece_info, str(piece.owner)]
            )
        input("Press any button to continue...")

    @staticmethod
    def ask_args(state: GameState) -> list[any]:
        loc = helpers.get_location(state)
        return [loc]

    @staticmethod
    def get_args(state: GameState) -> list[any]:
        return []

    @staticmethod
    def undo(state: GameState, loc: Location):
        pass

    @staticmethod
    def to_str(loc: Location):
        return "Inspects stack at {}".format(str(loc))