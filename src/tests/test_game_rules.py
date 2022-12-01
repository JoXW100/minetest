import unittest as ut
import structure.ui as ui


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
        
