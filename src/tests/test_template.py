import unittest as ut

class TestTemplate(ut.TestCase):
    def test_template(self):
        self.assertTrue(True)
        
    def test_template2(self):
        self.assertFalse(False)
        
    def test_template3(self):
        self.assertEqual(1, 1)
        
    def test_template4(self):
        self.assertNotEqual(1, 2)
        
    def test_template5(self):
        self.assertIsNotNone(object())
        
    def test_template6(self):
        self.assertIsNone(None)