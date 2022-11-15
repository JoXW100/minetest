from structure import GameState, Player

def find_player_with_id(state: GameState, id: int) -> Player:
    for player in state.players:
        if player.identifier == id:
            return player
    return None

def handle_victory(state: GameState) -> bool:
    victory = state.is_game_over()
    if victory == state.PLAYING:
        return True
    print("\n====== Game Over ======\n", state.board, sep='')
    if victory == state.DRAW:
        print("There was a draw!")
    else:
        player = find_player_with_id(state, victory)
        if player is None:
            print("Player #" + str(victory) + " won!")
        else:
            print(str(player) + ' won!')
    return False
    
def run(state : GameState):
    while handle_victory(state):
        state.current_player.perform_turn(state)
        state.next_round()