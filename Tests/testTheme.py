import unittest
from Scripts.theme import Theme
from Scripts.user import User

class TestTheme(unittest.TestCase):

    def test(self):
        theme1 = Theme("Beyonce theme", "Beyonce", 5)
        #theme2 = Theme("","",-1) --> correctly raises ValueError
        #theme3 = Theme(None,None,None) --> correctly raises ValueError
        
        ## test constructor
        self.assertEqual(theme1.name, "Beyonce theme")
        self.assertEqual(theme1.theme, "Beyonce")
        self.assertEqual(theme1.numWorkouts, 5)

        ## test editThemeNumWorkouts
        theme1.editThemeNumWorkouts(20)
        self.assertFalse(theme1.editThemeNumWorkouts(-10))
        self.assertEqual(theme1.numWorkouts, 20)

if __name__ == '__main__':
    unittest.main()
