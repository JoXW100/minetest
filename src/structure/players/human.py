from __future__ import annotations
from structure import Player, Action, GameState
from structure.actions import Insert

class Human(Player):
    """
    The human player in the game
    """
    
    @staticmethod
    def get_type() -> str:
        return "Human"
    
    def _get_prompt(self, state : GameState):
        prompt = "Piece(s) left: " + str(state.current_player.pieces) +"\nAvailable actions:\n"
        for index in range(len(state.actions)):
            prompt += '[' + str(index + 1) + '] ' + state.actions[index].get_name() + '\n'
        prompt += 'Enter action: '
        return prompt

    def first_turn(self, state : GameState):
        state.next_round()
        while True:
            print('\n', state.board, '\n----- ' + str(self) + \
                ' Place initial piece for ' + str(state.current_player) + ' -----\n', sep='')

            args = Insert.ask_args(state)
            status = Insert.execute(state, *args)

            if status is Action.FAILED:
                print("Failed " + Insert.get_name())
            elif status is Action.SUCCEEDED:
                state.prev_round()
                return
    
    def perform_turn(self, state : GameState):
        if state.round / len(state.players) < 1 and len(state.players) > 1:
            # Perform first turn
            self.first_turn(state)
            return
        
        if len(state.actions) < 1:
            print("No actions to perform")
            return
        
        while True:
            print('\n', state.board, '\n----- ' + str(self) + ' -----\n', sep='') 
            
            index = 0
            try:
                index = int(input(self._get_prompt(state)))
                if index < 0 or index > len(state.actions):
                    raise Exception('Index out of range')
            except:
                print("Enter a valid index in range [0-" + str(len(state.actions)) +"]" )
                continue
            
            selected_action = state.actions[index - 1]
            args = selected_action.ask_args(state)
            status = selected_action.execute(state, *args)
            
            if status is Action.FAILED:
                print("Failed " + selected_action.get_name())
            elif status is Action.PASS:
                state.prev_round()
                return
            elif status is Action.SUCCEEDED:
                return
            
    
    