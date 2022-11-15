from structure import Action, GameState, Piece, Location
import helpers

class Move(Action):
    """
    Moves a piece from one grid cell to another
    """
        
    @staticmethod
    def get_name():
        return "Move"
    
    @staticmethod
    def check(state: GameState, source: Location, dest: list[Location]) -> bool:
        if len(dest) == 0 \
        or not source.validate(state.board.size) \
        or any(source == d or not d.validate(state.board.size) for d in dest) \
        or Move._calc_num_movable(state, source) < len(dest):
            return False
        for d in dest:
            cell2 = state.board.rows[d.y][d.x]
            if not cell2.is_empty and cell2.top.state == Piece.STANDING:
                return False
        return True
    
    @staticmethod
    def execute(state: GameState, source: Location, dest: list[Location]) -> int:
        if Move.check(state, source, dest):
            Move.unsafe_execute(state, source, dest)
            return Action.SUCCEEDED
        return Action.FAILED
    
    @staticmethod
    def unsafe_execute(state: GameState, source: Location, dest: list[Location]):
        cell1 = state.board.rows[source.y][source.x]
        for d in dest:
            state.board.rows[d.y][d.x].put(cell1.pop())

    @staticmethod
    def undo(state: GameState, source: Location, dest: list[Location]):
        cell1 = state.board.rows[source.y][source.x]
        for d in dest:
            cell1.put(state.board.rows[d.y][d.x].pop())

    @staticmethod
    def _ask_loop_continue() -> bool:
        response = ""
        while True:
            response = input("Continue? (yes or no): ").lower()
            if response == "yes":
                return True
            elif response == "no":
                return False
    
    @staticmethod
    def ask_args(state: GameState)-> list[any]:
        print("Enter position of piece to move")
        source = helpers.get_location(state)
        num = Move._calc_num_movable(state, source)
        print("There are " + str(num) + " moveable pieces at the chosen location")
        dest = []
        for i in range(num):
            print("Enter destination position")
            dest.append(helpers.get_location(state))
            if i != num - 1 and not Move._ask_loop_continue():
                break
        return [source, dest]
    
    @staticmethod
    def _calc_num_movable(state: GameState, loc: Location) -> int:
        cell = state.board.rows[loc.y][loc.x]
        if not cell.is_empty and cell.top.owner is not state.current_player:
            return 0
        if cell.size > 1:
            count = 0
            for piece in cell:
                if count == cell.size - 1:
                    break
                if piece.owner is state.current_player:
                    count += 1
                else:
                    break
            return count
        return cell.size
    
    @staticmethod
    def _is_valid_destination(state: GameState, source: Location, loc: Location) -> bool:
        cell2 = state.board.rows[loc.y][loc.x]
        return loc != source and (cell2.is_empty or cell2.top.state != Piece.STANDING)
    
    @staticmethod
    def _get_combinations(options: list[Location], num: int) -> list[list[Location]]:
        if num <= 0:
            return []
        if num <= 1:
            return [[x] for x in options]
        res = []
        combinations = Move._get_combinations(options, num - 1)
        for combination in combinations:
            res.append(combination)
            for x in options:
                res.append([*combination, x])
        return res
    
    @staticmethod
    def get_args(state: GameState) -> list[list[any]]:
        args = []
        locations = state.board.get_all_locations()
        for location in locations:
            num = Move._calc_num_movable(state, location)
            if num > 0:
                valid_options = [x for x in locations if Move._is_valid_destination(state, location, x)]
                for comb in Move._get_combinations(valid_options, num):
                    args.append([location, comb])
        return args
    
    @staticmethod
    def to_str(source: Location, dest: list[Location]):
        test = "Move " + str(len(dest)) + " piece(s) at " + str(source) + ' to '
        for i in range(len(dest)):
            test += str(dest[i])
            if i < len(dest) - 1:
                test += ', '
        return test
