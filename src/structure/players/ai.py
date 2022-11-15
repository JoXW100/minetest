from __future__ import annotations
from structure import Player, Action, Piece, GameState
from structure.actions import Insert
import numpy as np
import random

class AI(Player):
    """
    The AI player in the game
    
    Methods
    -------
    perform_turn(state: GameState)
        Performs the AI's turn using minimax algorithm with alpha-beta pruning
    """
    
    WIN_SCORE = 1000000
    LOSE_SCORE = -WIN_SCORE

    @staticmethod
    def get_type() -> str:
        return "AI"
        
    def _evaluate(self, state: GameState) -> float:
        """
        Returns the current value of the board. 
        (+) is good for AI, (-) is good for player

        Points
        ------
        x points for each consecutive piece in a stack from the top of length x
        x points for each piece in a line of length x

        Parameters
        ----------
        state : GameState
            the current game state

        Returns
        -------
        float
            the value of the board
        """

        # ---- Check for lines ---- 
        score = 0

        #find how many pieces are left to connect sides for each color
        for player in state.players:
            #2d array with booleans.
            # player_pieces = [] 
            player_standing = []
            player_flat = []
            opponents_standing = []
            for row in state.board.rows:
                # player_pieces_row = []
                player_standing_row = []
                player_flat_row = []
                opponents_standing_row = []
                for stack in row:
                    # player_pieces_row.append(not stack.is_empty and stack.top.owner == player)
                    opponents_standing_row.append(not stack.is_empty and stack.top.owner != player and stack.top.state == Piece.STANDING)
                    player_standing_row.append(not stack.is_empty and stack.top.owner == player and stack.top.state == Piece.STANDING)
                    player_flat_row.append(not stack.is_empty and stack.top.owner == player and stack.top.state == Piece.FLAT)
                    
                # player_pieces.append(player_pieces_row)
                opponents_standing.append(opponents_standing_row)
                player_standing.append(player_standing_row)
                player_flat.append(player_flat_row)
                        
            # player_pieces = np.array(list(map(lambda row: np.array(row), player_pieces)))
            opponents_standing = np.array(list(map(lambda row: np.array(row), opponents_standing)))
            player_standing = np.array(list(map(lambda row: np.array(row), player_standing)))
            player_flat = np.array(list(map(lambda row: np.array(row), player_flat)))
            
            for left in range(state.board.size): ##horizontal lines
                for turn in range(1,state.board.size - 1):
                    line_start_segment_check = opponents_standing[left,0:turn]
                    if any(line_start_segment_check):
                        continue
                    for player_pieces in [player_standing, player_flat]: # Do once for standing, once for 
                        line_start_segment = player_pieces[left,0:turn]
                        for right in range(state.board.size):
                            line_turn_segment_check = opponents_standing[right:left+1, turn] \
                                if left >= right else opponents_standing[left:right+1, turn]
                            line_end_segment_check = opponents_standing[right,turn+1:]
                            
                            if(any(line_turn_segment_check) or any(line_end_segment_check)):
                                continue

                            line_turn_segment = player_pieces[right:left+1, turn] \
                                if left >= right else player_pieces[left:right+1, turn]
                            line_end_segment = player_pieces[right,turn+1:]

                            segments = [*line_start_segment, *line_turn_segment, *line_end_segment]
                            cumsum = len([t for t in segments if not t])
                            score += 1/(cumsum**3 + 1) * (1 if player is self else -1)

            for top in range(state.board.size): ##horizontal lines
                for turn in range(1,state.board.size - 1):
                    for player_pieces in [player_standing, player_flat]:
                        line_start_segment_check = opponents_standing[0:turn,top]
                        if(any(line_start_segment_check)):
                            continue
                        line_start_segment = player_pieces[0:turn,top]

                        for bottom in range(state.board.size):
                            line_turn_segment_check = opponents_standing[turn,bottom:top+1] \
                                if top >= bottom else opponents_standing[turn,top:bottom+1]
                            line_end_segment_check = opponents_standing[turn+1:,bottom]
                            
                            if(any(line_turn_segment_check) or any(line_end_segment_check)):
                                continue
                            
                            line_turn_segment = player_pieces[turn,bottom:top+1] \
                                if top >= bottom else player_pieces[turn,top:bottom+1]
                            line_end_segment = player_pieces[turn+1:,bottom]

                            segments = [*line_start_segment, *line_turn_segment, *line_end_segment]
                            cumsum = len([t for t in segments if not t])
                            score += (1/(cumsum**3 + 1) * (1 if player is self else -1))
        return score

    def _minimax(self, state: GameState, depth: int, alpha = float('-inf'), beta = float('inf'), maximize: bool = True) -> tuple[float, None|Action, list[any]]:
        """
        minimax algorithm with alpha-beta pruning.
        Returns the action the AI wants to make.

        Parameters
        ----------
        gs : GameState
            the current game state
        depth : int
            the depth of the search
        alpha : int
            the alpha value of the search
        beta : int
            the beta value of the search
        maximize : Boolean
            whether the AI is maximizing or minimizing
            
        RETURNS
        -------
        tuple[float, None|Action, list[any]]
            the value of the action, the action, and the arguments for the action
        """
        
        game_over_state = state.is_game_over()
        if game_over_state == self.identifier:
            return (self.WIN_SCORE, None, [])
        elif game_over_state >= 0:
            return (self.LOSE_SCORE, None, [])
        elif game_over_state == GameState.DRAW:
            return (0, None, [])
        elif depth == 0:
            return (self._evaluate(state), None, [])

        actions = state.get_all_valid_actions()
        if maximize: # AI turn
            best_action = [(float('-inf'), None, [])]
            for (action, args) in actions:
                
                # Perform Action
                action.unsafe_execute(state, *args)
                state.next_round()

                # Recurse and check next move (player's turn -> minimize)
                value = self._minimax(state, depth - 1, alpha, beta, False)[0] 
            
                # Is this action best for the AI?
                if value == best_action[0][0]:
                    best_action.append((value, action, args))
                elif value > best_action[0][0]:
                    best_action = [(value, action, args)]

                # Undo Action
                state.prev_round()
                action.undo(state, *args)

                # alpha-beta pruning
                alpha = max(value, alpha)
                
                # If this move for the player results in a possible better game 
                # state for the ai than a previous move. Stop since this move 
                # wont be selected by the player. (The player only selects the worst)
                if beta <= alpha: 
                    break

        else: # Player turn
            best_action = [(float('inf'), None, [])]
            for (action, args) in state.get_all_valid_actions():
                
                # Perform Action
                action.unsafe_execute(state, *args)
                state.next_round()

                # Recurse and check next move (AI's turn -> maximize)
                value = self._minimax(state, depth - 1, alpha, beta, True)[0] # New call to maximize
                
                # Is this action best for the Player?
                if value == best_action[0][0]:
                    best_action.append((value, action, args))
                elif value < best_action[0][0]:
                    best_action = [(value, action, args)]
                    
                # Undo Action
                state.prev_round()
                action.undo(state, *args)

                # alpha-beta pruning
                beta = min(value, beta)
                if beta >= alpha:
                    break

        return best_action[int(random.random() * len(best_action))]
    
    def first_turn(self, state : GameState) -> tuple[Action, list[any]]:
        """
        Places a flat piece in a random location for the other player

        Parameters
        ----------
        state : GameState
            the current game state

        Returns
        -------
        tuple[Action, list[any]]
            the action and the arguments for the action
        """
        # Randomize an insert of flat piece into a random valid cell
        state.next_round()
        args = Insert.get_args(state)
        valid_args = []
        for arg in args:
            if Insert.check(state, *arg):
                valid_args.append(arg)
        args = valid_args[int(random.random() * len(valid_args))]
        Insert.unsafe_execute(state, *args)
        print(str(self), ': ' + Insert.to_str(*args) + ' for ' + str(state.current_player))
        state.prev_round()

    def perform_turn(self, state : GameState):
        """
        Performs the AI's turn using minimax algorithm with alpha-beta pruning

        Parameters
        ----------
        state : GameState
            the current game state
        """
        print('\n', state.board)
        
        if state.round / len(state.players) < 1 and len(state.players) > 1:
            # Perform first turn
            self.first_turn(state)
            return
        
        if len(state.actions) < 1:
            print("No actions to perform")
            return
                
        print('\n----- ' + str(self) + ' is thinking... -----')

        if state.ai_difficulty == 0: # Easy
            # Do random move
            valid_actions = state.get_all_valid_actions()
            action, args = valid_actions[int(random.random() * len(valid_actions))]
        elif state.ai_difficulty == 1: # Medium
            # 50% chance of random move
            if random.random() < 0.5:
                valid_actions = state.get_all_valid_actions()
                action, args = valid_actions[int(random.random() * len(valid_actions))]
            else:            
                # Only consider AI move (i.e. depth = 1)
                (_, action, args) = self._minimax(state, 1)
        else: # Difficult
            # Consider both AI and Player move (i.e. depth = 2)
            (_, action, args) = self._minimax(state, 2)

        if action is None:
            raise Exception('AI failed to find action')
        action.unsafe_execute(state, *args)
        print('\n' + str(self), ': ' + action.to_str(*args) + ' \n')