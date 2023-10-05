import unittest as ut
import structure.ui as ui
from structure import *
from structure.actions import *


class TestGameRules(ut.TestCase):
    #T-RUL1-1
    def test_change_difficulty(self): 
        # Check that menu contains standard and custom game options
        menu = ui.MainMenu()
        contains_standard_game = False
        contains_custom_game = False
        
        for option in menu._options:
            if isinstance(option, ui.NewStandardGameMenu):
                contains_standard_game = True
            if isinstance(option, ui.NewCustomGameMenu):
                contains_custom_game = True
                
        self.assertTrue(contains_standard_game)
        self.assertTrue(contains_custom_game)  
        
        # Check that standard game menu contains difficulty options
        standard_game_menu = ui.NewStandardGameMenu()
        contains_difficulty_menu = False
        
        for option in standard_game_menu._options:
            if isinstance(option, ui.DifficultyMenu):
                contains_difficulty_menu = True
                
        self.assertTrue(contains_difficulty_menu)     
        
        # Check that difficulty menu contains easy/medium/hard
        difficulty_menu = ui.DifficultyMenu()
        contains_easy = False
        contains_medium = False
        contains_hard = False
        for option in difficulty_menu._options:
            if isinstance(option, ui.difficulty_menu.EasyDifficultyItem):
                contains_easy = True
            if isinstance(option, ui.difficulty_menu.MediumDifficultyItem):
                contains_medium = True
            if isinstance(option, ui.difficulty_menu.HardDifficultyItem):
                contains_hard = True
                
        self.assertTrue(contains_easy)
        self.assertTrue(contains_medium)
        self.assertTrue(contains_hard)
    
    # T-INT1-1
    def test_navigation_action(self):
        gs = GameState(ALL_ACTIONS, 4) # 4 is the board size, and can be changed (>1)
        lim = gs.board.size - 1
        assert(lim > 0)
        self.assertEqual(gs.selection, Location(0,0))
        # Cannot move left here, selection not altered
        NavigateLeft.execute(gs)
        self.assertEqual(gs.selection, Location(0,0))
        # move all the way to the top right
        for i in range(1, gs.board.size):
            NavigateRight.execute(gs)
            self.assertEqual(gs.selection, Location(i,0))
            
        # Cannot move up here, selection not altered
        NavigateUp.execute(gs)
        self.assertEqual(gs.selection, Location(lim,0))
        # move all the way to the bottom right
        for i in range(1, gs.board.size):
            NavigateDown.execute(gs)
            self.assertEqual(gs.selection, Location(lim,i))
            
        # Cannot move right here, selection not altered
        NavigateRight.execute(gs)
        self.assertEqual(gs.selection, Location(lim,lim))
        # move all the way to the bottom left
        for i in range(1, gs.board.size):
            NavigateLeft.execute(gs)
            self.assertEqual(gs.selection, Location(lim-i,lim))
        
        # Cannot move down here, selection not altered
        NavigateDown.execute(gs)
        self.assertEqual(gs.selection, Location(0,lim))
        # move all the way to the top left
        for i in range(1, gs.board.size):
            NavigateUp.execute(gs)
            self.assertEqual(gs.selection, Location(0,lim-i))
        # back at 0,0 
        self.assertEqual(gs.selection, Location(0,0))
            
        
    # T-INT2-1 
    def test_flag_on_hidden_cell(self):
        gs = GameState(ALL_ACTIONS, 4, 0)
        cell = gs.board.select(Location(0,0))
        cell.set_mined()
        gs.reveal_cell(Location(2,2))
        self.assertTrue(gs.set_selection(Location(0,0)))
        self.assertEqual(cell.state, CellState.Hidden)
        Flag.execute(gs)
        self.assertEqual(cell.state, CellState.Flagged)
        
    # T-INT2-2 
    def test_flag_on_flagged_cell(self):
        gs = GameState(ALL_ACTIONS, 4, 0)
        cell = gs.board.select(Location(0,0))
        cell.set_mined()
        cell.set_state(CellState.Flagged)
        gs.reveal_cell(Location(2,2))
        self.assertTrue(gs.set_selection(Location(0,0)))
        self.assertEqual(cell.state, CellState.Flagged)
        Flag.execute(gs)
        self.assertEqual(cell.state, CellState.Hidden)
        
             
    # T-INT2-3 
    def test_flag_on_revealed_cell(self):
        gs = GameState(ALL_ACTIONS, 4, 0)
        gs.board.select(Location(0,0)).set_mined()
        gs.reveal_cell(Location(2,2))
        cell = gs.board.select(Location(2,2))
        self.assertTrue(gs.set_selection(Location(2,2)))
        self.assertEqual(cell.state, CellState.Visible)
        Flag.execute(gs)
        self.assertEqual(cell.state, CellState.Visible)
